# 부산 해운대구 우동 아파트 실거래가 분석

이 프로젝트는 부산 해운대구 우동 지역의 주요 아파트(두산위브더제니스, 해운대아이파크, 해운대경동제이드, 더샵센텀파크 1차)의 실거래가 정보를 분석하고 시각화하는 Streamlit 애플리케이션입니다.

## 기능

- 아파트별 실거래가 추이 분석
- 평수별(30-40평대, 50-60평대, 70평대 이상) 가격 비교
- 가격 상승률 및 분포 분석
- 평당 가격 분석
- 아파트별 상세 정보 제공
- 시장 분석 및 전망 제공

## 설치 및 실행

### 필요 조건
- Python 3.10 이상
- pip 패키지 관리자

### 설치 방법
```bash
# 저장소 클론
git clone https://github.com/your-username/busan-real-estate-analysis.git
cd busan-real-estate-analysis

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 로컬에서 실행
```bash
streamlit run streamlit_app.py
```

## Streamlit Cloud 배포

이 애플리케이션은 Streamlit Cloud에 배포할 수 있습니다. 자세한 배포 방법은 [github_streamlit_deployment_guide.md](github_streamlit_deployment_guide.md) 파일을 참조하세요.

## 데이터 소스

이 애플리케이션은 다음 데이터 소스를 활용합니다:
- 네이버 부동산
- 공공데이터 포털

## 프로젝트 구조

```
busan-real-estate-analysis/
├── streamlit_app.py     # Streamlit 애플리케이션 메인 파일
├── requirements.txt     # 필요한 패키지 목록
├── data/                # 데이터 파일 디렉토리
├── README.md            # 프로젝트 설명
└── github_streamlit_deployment_guide.md  # 배포 가이드
```

## 사용 방법

1. 애플리케이션을 실행합니다.
2. 사이드바에서 메뉴를 선택합니다:
   - 개요: 전체 시장 개요 및 주요 지표
   - 가격 추이: 아파트별 실거래가 추이 분석
   - 평수별 비교: 평수별 가격 비교 분석
   - 아파트 상세: 아파트별 상세 정보
   - 시장 분석: 시장 분석 및 전망
3. 필터 옵션을 사용하여 특정 아파트나 평형대를 선택할 수 있습니다.

## 라이선스

© 2025 부산 해운대구 우동 아파트 실거래가 분석. All rights reserved.
