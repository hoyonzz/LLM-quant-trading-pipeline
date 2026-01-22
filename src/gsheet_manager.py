import os
import gspread
import datetime
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv


load_dotenv()



class GSheetManager:
    def __init__(self):
        # 1. 인증 설정
        self.key_path = "google_key.json"
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")

        # 구글 API 접근 범위(Scope) 설정
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # 2. 서비스 계정 인증
        try:
            self.creds = Credentials.from_service_account_file(self.key_path, scopes=self.scopes)
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open_by_key(self.sheet_id).sheet1
            print("✅ 구글 시트 연결 성공!")
        except Exception as e:
            print(f"❌ 구글 시트 연결 실패: {e}")

    def get_all_data(self):
        return self.sheet.get_all_records()
    
    def append_research(self, stock_name, content):
        # main.py에서 호출하는 결과 저장 함수
        try:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.sheet.append_row([now, stock_name, str(content)])
            print(f"✅ 구글 시트 기록 완료: {stock_name}")
        except Exception as e:
            print(f"❌ 시트 기록 실패: {e}")
    
if __name__ == "__main__":
    # 테스트 실행
    manager = GSheetManager()
    
    # 1. 조회 테스트
    data = manager.get_all_data()
    print(f"현재 시트 데이터: {data}")