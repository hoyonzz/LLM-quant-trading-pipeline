import os
import requests
import json
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