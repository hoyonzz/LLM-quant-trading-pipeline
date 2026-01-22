import json
import os
from datetime import datetime



class TokenTracker:
    def __init__(self, log_file="data/token_usage.json"):
        self.log_file = log_file
        # data 폴더가 없으면 생성
        if not os.path.exists("data"):
            os.makedirs("data")

        # 로그 파일이 없으면 초기화
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_usage(self, service, model, prompt_tokens, completion_tokens):
        # 토큰 사용량 기록
        # service: 'Perplexity', 'Gemini_Pro', 'Gemini_Flash등
        entry = {
            "time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "service": service,
            "model":model,
            "p_tokens": prompt_tokens,
            "c_tokens": completion_tokens,
            "total": prompt_tokens + completion_tokens
        }

        try:
            with open(self.log_file, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=4)

            # 터미널 실시간 모니터링용 출력
            print(f"💰 [{service}] 토큰 사용: {entry['total']} (누적 확인은 {self.log_file})")
        except Exception as e:
            print(f"❌ 토큰 로깅 실패: {e}")

    def get_weekly_summary(self):
        # 주간 사용량 합산 - 비용 최적화 판단용 이 데이터를 기반으로 AI가 컨텍스트 초기화 시점을 결정
        pass