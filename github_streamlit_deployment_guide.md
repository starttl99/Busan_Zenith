# 부산 해운대구 우동 아파트 실거래가 분석 - GitHub 및 Streamlit Cloud 배포 가이드

이 문서는 부산 해운대구 우동 지역 아파트 실거래가 분석 Streamlit 애플리케이션을 GitHub에 업로드하고 Streamlit Cloud에 배포하는 방법을 안내합니다.

## 1. GitHub 저장소 생성 및 파일 업로드

### 1.1 GitHub 저장소 생성

1. GitHub 계정에 로그인합니다.
2. 오른쪽 상단의 '+' 버튼을 클릭하고 'New repository'를 선택합니다.
3. 저장소 이름을 'busan-real-estate-analysis'로 입력합니다.
4. 설명(Description)에 '부산 해운대구 우동 아파트 실거래가 분석 애플리케이션'을 입력합니다.
5. 저장소를 Public으로 설정합니다.
6. 'Create repository' 버튼을 클릭합니다.

### 1.2 파일 업로드

다음 파일들을 GitHub 저장소에 업로드합니다:

1. `streamlit_app.py` - Streamlit 애플리케이션 메인 파일
2. `requirements.txt` - 필요한 패키지 목록
3. `data/` 디렉토리 (필요한 경우)
4. `README.md` - 프로젝트 설명

GitHub 웹 인터페이스를 통해 파일을 업로드하는 방법:
1. 생성된 저장소 페이지에서 'Add file' > 'Upload files' 버튼을 클릭합니다.
2. 파일을 드래그 앤 드롭하거나 '파일 선택' 버튼을 클릭하여 업로드할 파일을 선택합니다.
3. 'Commit changes' 버튼을 클릭하여 업로드를 완료합니다.

Git 명령어를 사용하는 방법:
```bash
git clone https://github.com/your-username/busan-real-estate-analysis.git
cd busan-real-estate-analysis
# 파일 복사
cp /path/to/streamlit_app.py .
cp /path/to/requirements.txt .
cp -r /path/to/data .
# Git에 추가 및 커밋
git add .
git commit -m "Initial commit: Busan real estate analysis app"
git push origin main
```

## 2. Streamlit Cloud에 배포

### 2.1 Streamlit Cloud 계정 생성

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속합니다.
2. 'Sign up' 버튼을 클릭합니다.
3. GitHub 계정으로 로그인합니다.

### 2.2 애플리케이션 배포

1. Streamlit Cloud 대시보드에서 'New app' 버튼을 클릭합니다.
2. 저장소 선택: 'busan-real-estate-analysis'를 선택합니다.
3. 브랜치 선택: 'main'을 선택합니다.
4. 메인 파일 경로: 'streamlit_app.py'를 입력합니다.
5. 앱 이름 설정: 'busan-real-estate-analysis'를 입력합니다.
6. 'Deploy!' 버튼을 클릭합니다.

배포가 완료되면 다음과 같은 URL로 애플리케이션에 접근할 수 있습니다:
```
https://busan-real-estate-analysis.streamlit.app/
```

### 2.3 애플리케이션 업데이트

GitHub 저장소에 변경 사항을 푸시하면 Streamlit Cloud가 자동으로 애플리케이션을 업데이트합니다. 다음 단계를 따르세요:

1. 로컬에서 파일을 수정합니다.
2. 변경 사항을 커밋하고 푸시합니다:
```bash
git add .
git commit -m "Update: 설명"
git push origin main
```
3. Streamlit Cloud가 자동으로 변경 사항을 감지하고 애플리케이션을 재배포합니다.

## 3. 추가 설정 및 팁

### 3.1 비공개 데이터 관리

민감한 데이터나 API 키는 Streamlit Cloud의 Secrets 관리 기능을 사용하세요:

1. Streamlit Cloud 대시보드에서 앱을 선택합니다.
2. 'Settings' > 'Secrets' 메뉴로 이동합니다.
3. 필요한 비밀 값을 추가합니다.
4. 애플리케이션에서 `st.secrets`를 통해 접근합니다:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

### 3.2 성능 최적화

1. `@st.cache_data` 데코레이터를 사용하여 데이터 로딩 함수를 캐싱합니다.
2. 대용량 데이터는 압축하거나 효율적인 형식(parquet 등)으로 저장합니다.
3. 무거운 계산은 사전에 처리하고 결과만 저장하여 로드합니다.

### 3.3 사용자 인증 추가

Streamlit Cloud Community 플랜에서는 기본 인증 기능을 제공합니다:

1. Streamlit Cloud 대시보드에서 앱을 선택합니다.
2. 'Settings' > 'Sharing' 메뉴로 이동합니다.
3. 'Viewer access' 설정에서 'Restricted to specific users'를 선택합니다.
4. 접근 권한을 부여할 이메일 주소를 추가합니다.

## 4. 문제 해결

### 4.1 배포 실패

1. 로그 확인: Streamlit Cloud 대시보드에서 앱을 선택하고 'Logs' 탭을 확인합니다.
2. requirements.txt 확인: 필요한 모든 패키지가 올바른 버전으로 명시되어 있는지 확인합니다.
3. 파일 경로 확인: 상대 경로가 올바르게 설정되어 있는지 확인합니다.

### 4.2 성능 이슈

1. 메모리 사용량 확인: 대용량 데이터를 효율적으로 처리하는지 확인합니다.
2. 캐싱 활용: 반복적인 계산에 `@st.cache_data` 또는 `@st.cache_resource`를 사용합니다.
3. 이미지 최적화: 이미지 크기를 줄이고 웹에 최적화된 형식을 사용합니다.

## 5. 유지 관리

1. 정기적으로 데이터를 업데이트합니다.
2. 사용자 피드백을 수집하고 UI/UX를 개선합니다.
3. 새로운 Streamlit 기능을 활용하여 애플리케이션을 개선합니다.
4. 패키지 의존성을 최신 상태로 유지합니다.

---

이 가이드를 따라 부산 해운대구 우동 아파트 실거래가 분석 애플리케이션을 GitHub에 업로드하고 Streamlit Cloud에 배포할 수 있습니다. 추가 질문이나 도움이 필요하면 언제든지 문의하세요.
