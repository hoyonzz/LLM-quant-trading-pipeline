import os
import requests
import json
import time
from dotenv import load_dotenv


load_dotenv()



class MarketDataManager:
    def __init__(self, auth_manager):
        self.auth = auth_manager
        self.base_url = os.getenv("KIS_URL") if self.auth.mode == 'real' else os.getenv("KIS_MOCK_URL")

    def _get_headers(self, tr_id):
        # 기본 헤더 구성
        return {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.auth.get_access_token()}",
            "appkey" : self.auth.app_key,
            "appsecret": self.auth.app_secret,
            "tr_id" : tr_id,
            "custtype": "P"
        }
    
    def get_stock_price(self, ticker):
        # 현재가, 등락률, 체결강도 조회
        path = "/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = self._get_headers("FHKST01010100")
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": ticker
        }

        res = requests.get(f"{self.base_url}{path}", headers=headers, params=params)
        if res.status_code == 200:
            data = res.json().get('output')

            if data:
                raw_strength = data.get('vol_pwer') or data.get('w_vol_pwer') or "0.0"
                return {
                    "current_price" : int(data.get('stck_prpr', 0)), # 현재가
                    "change_rate" : float(data.get('prdy_ctrt', 0.0)), # 등락률
                    "volume_strength": float(raw_strength) # 체결강도
                }
        print(f"❌ 데이터 조회 실패: {res.text}")
        return None
    
    def get_market_breath(self):
        # 시장 등락 종목 수 조회
        # 코스피 또는 코스닥 지수 정보 조회
        path = "/uapi/domestic-stock/v1/quotations/inquire-index-price"
        headers = self._get_headers("FHKST01010300")
        params = {
            "fid_cond_mrkt_div_code": "U",
            "fid_input_iscd": "0001" # KOSPI 기준
        }

        res = requests.get(f"{self.base_url}{path}", headers=headers, params=params)
        if res.status_code == 200:
            result = res.json()
            data = result.get('output')

            if not data or len(data) == 0:
                print("⚠️ [주의] 현재 환경에서 지수 데이터를 제공하지 않습니다. (모의투자 제한)")
                return {"rising": "N/A", "falling": "N/A"}
            return {
                "rising": data.get('ascn_issu_cnt', "0"),
                "falling": data.get('down_issu_cnt', "0")
            }
        return None
    

if __name__ == "__main__":
    from src.auth import KISAuth  # 인증 모듈 불러오기
    
    # 1. 인증 객체 생성 (모의투자 모드)
    auth = KISAuth(mode="mock") 
    
    # 2. 마켓 데이터 매니저 생성
    md_manager = MarketDataManager(auth)
    
    # 3. 테스트 실행 (한올바이오파마: 009420)
    ticker = "009420"
    print(f"--- [{ticker}] 데이터 조회 테스트 ---")
    
    price_data = md_manager.get_stock_price(ticker)
    if price_data:
        print(f"현재가: {price_data['current_price']}원")
        print(f"등락률: {price_data['change_rate']}%")
        print(f"체결강도: {price_data['volume_strength']}%")
    else:
        print("❌ 가격 데이터 조회 실패")

    market_breath = md_manager.get_market_breath()
    if market_breath:
        print(f"--- 시장 등락 상황 ---")
        print(f"상승 종목 수: {market_breath['rising']}")
        print(f"하락 종목 수: {market_breath['falling']}")