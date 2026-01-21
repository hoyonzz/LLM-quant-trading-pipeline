import os
import requests
import json
import time
from dotenv import load_dotenv


load_dotenv()


class KISAuth:
    def __init__(self, mode="mock"):
        self.mode = mode
        if self.mode == "real":
            self.app_key = os.getenv("KIS_APP_KEY")
            self.app_secret = os.getenv("KIS_APP_SECRET")
            self.url = os.getenv("KIS_URL")
        else:
            self.app_key = os.getenv("KIS_MOCK_APP_KEY")
            self.app_secret = os.getenv("KIS_MOCK_APP_SECRET")
            self.url = os.getenv("KIS_MOCK_URL")

    def get_access_token(self):
        path = "/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type" : "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }

        response = requests.post(f"{self.url}{path}", headers=headers, data=json.dumps(body))

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Error: {response.json()}")
            return None
        
if __name__ == "__main__":
    # 테스트 실행
    auth = KISAuth(mode="mock")
    token = auth.get_access_token()
    print(f"발급된 토큰: {token}")