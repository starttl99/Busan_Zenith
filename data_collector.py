import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os
from datetime import datetime
import logging
import schedule

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_collection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("real_estate_data_collector")

# 데이터 디렉토리 생성
os.makedirs("data", exist_ok=True)

# 아파트 정보
APARTMENTS = [
    {
        "name": "두산위브더제니스",
        "location": "부산 해운대구 우동",
        "naver_id": "129401",  # 예시 ID (실제 ID로 대체 필요)
        "sizes": ["30-40평대", "50-60평대", "70평대 이상"]
    },
    {
        "name": "해운대아이파크",
        "location": "부산 해운대구 우동",
        "naver_id": "129402",  # 예시 ID (실제 ID로 대체 필요)
        "sizes": ["30-40평대", "50-60평대", "70평대 이상"]
    },
    {
        "name": "해운대경동제이드",
        "location": "부산 해운대구 우동",
        "naver_id": "129403",  # 예시 ID (실제 ID로 대체 필요)
        "sizes": ["50-60평대", "70평대 이상"]
    },
    {
        "name": "더샵센텀파크",
        "location": "부산 해운대구 우동",
        "naver_id": "129404",  # 예시 ID (실제 ID로 대체 필요)
        "sizes": ["30-40평대", "50-60평대"]
    }
]

# 법정동 코드 (부산 해운대구 우동)
LEGAL_DONG_CODE = "2635010500"

# 네이버 부동산 데이터 수집 함수
def collect_naver_real_estate_data():
    logger.info("네이버 부동산 데이터 수집 시작")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://land.naver.com/"
    }
    
    all_data = []
    
    for apt in APARTMENTS:
        logger.info(f"{apt['name']} 데이터 수집 중...")
        
        try:
            # 네이버 부동산 API URL (예시 - 실제 API URL로 대체 필요)
            url = f"https://land.naver.com/api/articles/complex/{apt['naver_id']}"
            
            response = requests.get(url, headers=headers)
            
            # 요청 제한 방지를 위한 대기
            time.sleep(random.uniform(1.0, 3.0))
            
            if response.status_code == 200:
                data = response.json()
                
                # 데이터 파싱 (예시 - 실제 응답 구조에 맞게 수정 필요)
                for item in data.get("articleList", []):
                    area = float(item.get("area", 0))
                    price = float(item.get("price", 0))
                    
                    # 평형대 분류
                    size_category = ""
                    pyeong = area / 3.3
                    
                    if 30 <= pyeong < 40:
                        size_category = "30-40평대"
                    elif 50 <= pyeong < 60:
                        size_category = "50-60평대"
                    elif pyeong >= 70:
                        size_category = "70평대 이상"
                    else:
                        continue  # 관심 없는 평형대는 건너뜀
                    
                    # 해당 아파트에 존재하는 평형대인지 확인
                    if size_category not in apt["sizes"]:
                        continue
                    
                    all_data.append({
                        "날짜": datetime.now().strftime("%Y-%m-%d"),
                        "아파트": apt["name"],
                        "평형대": size_category,
                        "최저가(억)": price,
                        "최고가(억)": price
                    })
            else:
                logger.error(f"{apt['name']} 데이터 수집 실패: {response.status_code}")
                
        except Exception as e:
            logger.error(f"{apt['name']} 데이터 수집 중 오류 발생: {str(e)}")
    
    # 데이터 집계 (같은 아파트, 같은 평형대의 최저가/최고가 계산)
    if all_data:
        df = pd.DataFrame(all_data)
        
        # 날짜, 아파트, 평형대별로 그룹화하여 최저가/최고가 계산
        aggregated_data = df.groupby(["날짜", "아파트", "평형대"]).agg({
            "최저가(억)": "min",
            "최고가(억)": "max"
        }).reset_index()
        
        # 결과 저장
        today = datetime.now().strftime("%Y-%m-%d")
        aggregated_data.to_csv(f"data/naver_real_estate_data_{today}.csv", index=False)
        
        # 누적 데이터 업데이트
        update_cumulative_data(aggregated_data)
        
        logger.info(f"네이버 부동산 데이터 수집 완료: {len(aggregated_data)}개 항목")
        return aggregated_data
    else:
        logger.warning("수집된 데이터가 없습니다.")
        return pd.DataFrame()

# 공공데이터 포털 API를 통한 실거래가 데이터 수집 함수
def collect_public_data():
    logger.info("공공데이터 포털 실거래가 데이터 수집 시작")
    
    # 공공데이터 포털 API 키 (실제 API 키로 대체 필요)
    API_KEY = "YOUR_API_KEY_HERE"
    
    # 국토교통부 아파트매매 실거래자료 API URL
    url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    
    # 현재 년월 계산 (YYYYMM 형식)
    current_date = datetime.now().strftime("%Y%m")
    
    all_data = []
    
    try:
        # API 요청 파라미터
        params = {
            "serviceKey": API_KEY,
            "LAWD_CD": LEGAL_DONG_CODE[:5],  # 지역코드 (시군구코드)
            "DEAL_YMD": current_date  # 계약년월
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # XML 응답 파싱
            soup = BeautifulSoup(response.text, "xml")
            items = soup.find_all("item")
            
            for item in items:
                # 우동 지역만 필터링
                if item.find("법정동").text.strip() != "우동":
                    continue
                
                # 관심 있는 아파트만 필터링
                apt_name = item.find("아파트").text.strip()
                target_apt = None
                
                for apt in APARTMENTS:
                    if apt["name"] in apt_name:
                        target_apt = apt
                        break
                
                if not target_apt:
                    continue
                
                # 데이터 추출
                try:
                    area = float(item.find("전용면적").text.strip())
                    price = float(item.find("거래금액").text.strip().replace(",", "")) / 10000  # 만원 -> 억원 변환
                    
                    # 평형대 분류
                    size_category = ""
                    pyeong = area / 3.3
                    
                    if 30 <= pyeong < 40:
                        size_category = "30-40평대"
                    elif 50 <= pyeong < 60:
                        size_category = "50-60평대"
                    elif pyeong >= 70:
                        size_category = "70평대 이상"
                    else:
                        continue  # 관심 없는 평형대는 건너뜀
                    
                    # 해당 아파트에 존재하는 평형대인지 확인
                    if size_category not in target_apt["sizes"]:
                        continue
                    
                    all_data.append({
                        "날짜": datetime.now().strftime("%Y-%m-%d"),
                        "아파트": target_apt["name"],
                        "평형대": size_category,
                        "최저가(억)": price,
                        "최고가(억)": price
                    })
                except Exception as e:
                    logger.error(f"데이터 파싱 중 오류 발생: {str(e)}")
        else:
            logger.error(f"공공데이터 API 요청 실패: {response.status_code}")
            
    except Exception as e:
        logger.error(f"공공데이터 수집 중 오류 발생: {str(e)}")
    
    # 데이터 집계 (같은 아파트, 같은 평형대의 최저가/최고가 계산)
    if all_data:
        df = pd.DataFrame(all_data)
        
        # 날짜, 아파트, 평형대별로 그룹화하여 최저가/최고가 계산
        aggregated_data = df.groupby(["날짜", "아파트", "평형대"]).agg({
            "최저가(억)": "min",
            "최고가(억)": "max"
        }).reset_index()
        
        # 결과 저장
        today = datetime.now().strftime("%Y-%m-%d")
        aggregated_data.to_csv(f"data/public_real_estate_data_{today}.csv", index=False)
        
        # 누적 데이터 업데이트
        update_cumulative_data(aggregated_data)
        
        logger.info(f"공공데이터 포털 데이터 수집 완료: {len(aggregated_data)}개 항목")
        return aggregated_data
    else:
        logger.warning("수집된 데이터가 없습니다.")
        return pd.DataFrame()

# 누적 데이터 업데이트 함수
def update_cumulative_data(new_data):
    cumulative_file = "data/real_estate_data.csv"
    
    try:
        # 기존 누적 데이터 로드 (없으면 새로 생성)
        if os.path.exists(cumulative_file):
            cumulative_data = pd.read_csv(cumulative_file)
            
            # 새 데이터와 병합
            combined_data = pd.concat([cumulative_data, new_data])
            
            # 중복 제거 (같은 날짜, 아파트, 평형대)
            combined_data = combined_data.drop_duplicates(subset=["날짜", "아파트", "평형대"], keep="last")
            
            # 날짜 기준 정렬
            combined_data = combined_data.sort_values("날짜")
            
            # 최근 6개월 데이터만 유지 (선택 사항)
            # 날짜를 datetime으로 변환
            combined_data["날짜"] = pd.to_datetime(combined_data["날짜"])
            
            # 최근 6개월 필터링
            six_months_ago = datetime.now() - pd.DateOffset(months=6)
            combined_data = combined_data[combined_data["날짜"] >= six_months_ago]
            
            # 다시 문자열로 변환
            combined_data["날짜"] = combined_data["날짜"].dt.strftime("%Y-%m-%d")
            
            # 저장
            combined_data.to_csv(cumulative_file, index=False)
            logger.info(f"누적 데이터 업데이트 완료: {len(combined_data)}개 항목")
        else:
            # 새 파일 생성
            new_data.to_csv(cumulative_file, index=False)
            logger.info(f"새 누적 데이터 파일 생성: {len(new_data)}개 항목")
    except Exception as e:
        logger.error(f"누적 데이터 업데이트 중 오류 발생: {str(e)}")

# 데이터 수집 실행 함수
def run_data_collection():
    logger.info("데이터 수집 작업 시작")
    
    try:
        # 네이버 부동산 데이터 수집
        naver_data = collect_naver_real_estate_data()
        
        # 공공데이터 포털 데이터 수집
        public_data = collect_public_data()
        
        # 데이터 수집 시간 기록
        with open("data/last_update.txt", "w") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        logger.info("데이터 수집 작업 완료")
        
        return True
    except Exception as e:
        logger.error(f"데이터 수집 작업 중 오류 발생: {str(e)}")
        return False

# 스케줄러 설정 함수
def setup_scheduler():
    # 매일 오전 9시 실행
    schedule.every().day.at("09:00").do(run_data_collection)
    
    # 매일 저녁 9시 실행
    schedule.every().day.at("21:00").do(run_data_collection)
    
    logger.info("스케줄러 설정 완료: 매일 오전 9시, 저녁 9시에 데이터 수집")

# 메인 함수
def main():
    logger.info("부동산 데이터 수집 프로그램 시작")
    
    # 초기 데이터 수집 실행
    run_data_collection()
    
    # 스케줄러 설정
    setup_scheduler()
    
    # 스케줄러 실행 (무한 루프)
    logger.info("스케줄러 실행 중...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 스케줄 확인
    except KeyboardInterrupt:
        logger.info("프로그램 종료")

if __name__ == "__main__":
    main()
