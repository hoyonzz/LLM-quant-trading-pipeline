import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import pytz
from config import SECTOR_CONFIGS, STOCK_DB, BRIEFING_TEMPLATES


load_dotenv()



class PerplexityResearcher:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar"

    def _generate_prompt(self, type, ticker=None):
        # 설정파일을 기반으로 프롬프트 조립하는 함수
        # 한국 시간 구하기
        korea_tz = pytz.timezone('Asia/Seoul')
        now = datetime.now(korea_tz)
        current_date = now.strftime("%Y년 %m월 %d일 %H시 %M분") # 예: 2026년 1월 22일 09시 00분

        if type == "morning_market":
            sectors = ", ".join(SECTOR_CONFIGS.keys())
            return BRIEFING_TEMPLATES["morning_market"].format(sector_list=sectors, datetime=current_date)
        
        elif type == "specific_stock" and ticker:
            stock = STOCK_DB.get(ticker)
            sector = SECTOR_CONFIGS.get(stock['sector'])
            return BRIEFING_TEMPLATES["specific_stock"].format(
                name = stock["name"],
                ticker=ticker,
                peers=sector['global_peer'],
                pipeline=stock['key_pipeline'],
                specific_queries=" / ".join(stock['specific_queries']),
                datetime=current_date)
            
        
        elif type == "evening_review" and ticker:
            stock = STOCK_DB.get(ticker)
            return BRIEFING_TEMPLATES["evening_review"].format(name=stock['name'], datetime=current_date)
            
        return None
            
    def get_report(self, type, ticker=None):
        # 프롬프트 생성, API로 전송후 분석 결과를 받아오는 함수
        prompt = self._generate_prompt(type, ticker)
        return self.get_custom_report(prompt)
    
    def get_custom_report(self, prompt):
        # Scanner 및 직접 호출용 범용 메서드
        if not prompt: return "Invalid Prompt"

        data = {
            "model" : self.model,
            "messages": [
                {"role" : "system", "content" : "너는 AI Captain에게 정보를 공급하는 최고의 퀀트 리서치 에이전트다. 반드시 JSON 형식으로만 답변하며 감정을 배제하고 숫자를 기반으로 가장 깊이 있는 리서치를 수행하라."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
        }
        try:
            response =  requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=data,
                timeout=45
            )

            if response.status_code == 200:
                res_json = response.json()
                # 초큰 추적, 이후에 TokenTracker와 연동
                return res_json['choices'][0]['message']['content']
            return f"❌ API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ Request Error: {str(e)}"
    
if __name__ == "__main__":
    researcher = PerplexityResearcher()
    # 테스트: 한올바이오파마 상세 분석 (가장 중요한 데이터)
    print(researcher.get_report("specific_stock", ticker="009420"))