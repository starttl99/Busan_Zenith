# 부산 해운대구 우동 아파트 실거래가 자동 수집 설정 가이드

이 문서는 부산 해운대구 우동 지역 아파트 실거래가 데이터를 자동으로 수집하고 Streamlit 애플리케이션에 반영하는 방법을 안내합니다.

## 1. 자동 데이터 수집 스크립트 개요

`data_collector.py` 스크립트는 다음 기능을 제공합니다:

- 네이버 부동산에서 아파트 실거래가 데이터 수집
- 공공데이터 포털 API를 통한 실거래가 데이터 수집
- 매일 오전 9시와 저녁 9시에 자동 실행
- 수집된 데이터를 CSV 파일로 저장 및 관리

## 2. 필요 사항

- Python 3.10 이상
- 필요한 패키지: requests, beautifulsoup4, pandas, schedule
- 공공데이터 포털 API 키 (선택 사항)

## 3. 설치 방법

```bash
# 필요한 패키지 설치
pip install requests beautifulsoup4 pandas schedule
```

## 4. 스크립트 설정

### 4.1 API 키 설정

공공데이터 포털 API를 사용하려면 `data_collector.py` 파일에서 API 키를 설정해야 합니다:

```python
# 공공데이터 포털 API 키 (실제 API 키로 대체 필요)
API_KEY = "YOUR_API_KEY_HERE"
```

공공데이터 포털(https://www.data.go.kr/)에서 회원가입 후 '국토교통부 아파트매매 실거래자료' API 활용 신청을 통해 API 키를 발급받을 수 있습니다.

### 4.2 아파트 정보 설정

수집할 아파트 정보를 `data_collector.py` 파일에서 설정할 수 있습니다:

```python
# 아파트 정보
APARTMENTS = [
    {
        "name": "두산위브더제니스",
        "location": "부산 해운대구 우동",
        "naver_id": "129401",  # 네이버 부동산 아파트 ID
        "sizes": ["30-40평대", "50-60평대", "70평대 이상"]
    },
    # 다른 아파트 정보...
]
```

네이버 부동산 아파트 ID는 네이버 부동산 사이트에서 해당 아파트 페이지 URL에서 확인할 수 있습니다.

## 5. 실행 방법

### 5.1 직접 실행

```bash
python data_collector.py
```

스크립트를 직접 실행하면 즉시 데이터 수집을 시작하고, 이후 매일 오전 9시와 저녁 9시에 자동으로 실행됩니다.

### 5.2 서버에서 백그라운드로 실행

서버에서 백그라운드로 실행하려면 다음 명령어를 사용합니다:

```bash
nohup python data_collector.py > data_collector.log 2>&1 &
```

이 명령어는 스크립트를 백그라운드에서 실행하고 로그를 `data_collector.log` 파일에 저장합니다.

### 5.3 서버 재시작 시 자동 실행 설정

#### Linux (systemd)

1. 서비스 파일 생성:

```bash
sudo nano /etc/systemd/system/real-estate-collector.service
```

2. 다음 내용 입력:

```
[Unit]
Description=Real Estate Data Collector
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/real_estate_project
ExecStart=/usr/bin/python3 /path/to/real_estate_project/data_collector.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. 서비스 활성화 및 시작:

```bash
sudo systemctl enable real-estate-collector.service
sudo systemctl start real-estate-collector.service
```

4. 서비스 상태 확인:

```bash
sudo systemctl status real-estate-collector.service
```

## 6. Streamlit Cloud에서의 예약 작업 설정

Streamlit Cloud는 직접적인 예약 작업 기능을 제공하지 않습니다. 대신 다음 방법을 사용할 수 있습니다:

### 6.1 GitHub Actions를 통한 자동화

1. GitHub 저장소에 `.github/workflows/update_data.yml` 파일 생성:

```yaml
name: Update Real Estate Data

on:
  schedule:
    - cron: '0 0,12 * * *'  # UTC 기준 매일 0시, 12시 (한국 시간 9시, 21시)
  workflow_dispatch:  # 수동 실행 옵션

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4 pandas
          
      - name: Run data collector
        run: |
          python data_collector.py
          
      - name: Commit and push if changed
        run: |
          git config --global user.email "github-actions@github.com"
          git config --global user.name "GitHub Actions"
          git add data/
          git commit -m "Update real estate data" || exit 0
          git push
```

2. GitHub 저장소 설정에서 Secrets에 필요한 API 키 추가 (필요한 경우)

3. GitHub Actions가 저장소에 쓰기 권한을 가지도록 설정

이 방법을 사용하면 GitHub Actions가 매일 지정된 시간에 데이터를 수집하고, 변경 사항이 있으면 저장소에 커밋합니다. Streamlit Cloud는 저장소 변경을 감지하여 애플리케이션을 자동으로 업데이트합니다.

### 6.2 외부 서버 활용

1. 별도의 서버(VPS, AWS EC2 등)에서 데이터 수집 스크립트 실행
2. 수집된 데이터를 GitHub 저장소에 자동으로 커밋하도록 설정
3. Streamlit Cloud는 저장소 변경을 감지하여 애플리케이션을 자동으로 업데이트

## 7. 데이터 파일 구조

데이터 파일은 다음과 같은 구조로 저장됩니다:

- `data/real_estate_data.csv`: 누적 데이터 파일 (Streamlit 애플리케이션이 사용)
- `data/naver_real_estate_data_YYYY-MM-DD.csv`: 네이버 부동산에서 수집한 일별 데이터
- `data/public_real_estate_data_YYYY-MM-DD.csv`: 공공데이터 포털에서 수집한 일별 데이터
- `data/last_update.txt`: 마지막 데이터 수집 시간

## 8. 문제 해결

### 8.1 데이터 수집 실패

- `data_collection.log` 파일을 확인하여 오류 메시지 확인
- 네트워크 연결 상태 확인
- API 키가 유효한지 확인
- 아파트 ID가 올바른지 확인

### 8.2 스케줄러 작동 안 함

- 서버 시간이 올바르게 설정되어 있는지 확인
- 스크립트가 백그라운드에서 실행 중인지 확인:
  ```bash
  ps aux | grep data_collector.py
  ```
- 로그 파일에서 오류 확인

## 9. 유지 관리

- 정기적으로 로그 파일 확인
- 데이터 파일 크기 모니터링 (장기간 실행 시 파일 크기가 커질 수 있음)
- 필요에 따라 오래된 일별 데이터 파일 정리

---

이 가이드를 따라 부산 해운대구 우동 아파트 실거래가 데이터를 자동으로 수집하고 Streamlit 애플리케이션에 반영할 수 있습니다. 추가 질문이나 도움이 필요하면 언제든지 문의하세요.
