import os
import requests
import json
import time
from dotenv import load_dotenv


load_dotenv()


class KISAuth:
    def __init__(self, mode="mock"):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.token_file = os.path.join(base_path, "data", f"token_{mode}.json")
        os.makedirs(os.path.join(base_path, "data"), exist_ok=True)
        self.mode = mode
        self.base_url = os.getenv("KIS_URL") if mode == "real" else os.getenv("KIS_MOCK_URL")
        self.app_key = os.getenv("KIS_APP_KEY") if mode == "real" else os.getenv("KIS_MOCK_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET") if mode == "real" else os.getenv("KIS_MOCK_APP_SECRET")

    def _save_token(self, token_data):
        # 새로 받은 토큰 데이터를 파일로 저장(현재시간 + 만료시간을 더해 절대 시각으로 저장)
        # 증권사에서 제공하는 expires_in을 현재시간에 더해서 계산
        token_data['expiry'] = time.time() + int(token_data['expires_in'])

        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def _load_token(self):
        # 1 저장된 파일에서 토큰 유효성 검사(파일이 없다면 토큰이 없는 것으로 간주)
        if not os.path.exists(self.token_file):
            return None
        
        with open(self.token_file, 'r') as f:
            token_data = json.load(f)

            # 2. 유효기간 검사(현재 시간이 만료 시각보다 지났는지 확인- 버퍼(60초)를 두어 만료 직전에도 새로 받도록 설계)
            if time.time() > token_data['expiry'] - 60:
                print("⚠️ 저장된 토큰이 만료되었습니다.")
                return None
        
            return token_data.get("access_token")

    def get_access_token(self):
        # Step 1: 저장된 토큰이 있는지 확인
        token = self._load_token()
        if token:
            print("💾 유효한 기존 토큰을 재사용합니다.")
            return token
        
        # Step 2: 캐싱된 토큰이 없거나 만료되었다면 새로 발급
        print("🆕 새 토큰을 서버에서 발급받습니다...")
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        data = {
            "grant_type" : "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            res_data = response.json()
            self._save_token(res_data)
            return res_data.get("access_token")
        else:
            print(f"❌ 토큰 발급 실패: {response.text}")
            return None


        
if __name__ == "__main__":
    # 테스트 실행
    auth_manager = KISAuth(mode="mock")
    token = auth_manager.get_access_token()
    print(f"발급된 토큰: {token[:20]}")