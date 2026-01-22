import json
import os
from datetime import datetime



class TokenTracker:
    def __init__(self, log_file="data/token_usage.json"):
        self.log_file = log_file
        if not os.path.exists(log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def log_usage(self, model, prompt_tokens, completion_tokens):
        # 토큰 사용량 기록
        log_entry = {
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model":model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }

        with open(self.log_file, 'r+') as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4)

        print(f"📊  Token Usage Update: {log_entry['total_token']} tokens used ({model})")

        def get_weekly_summary(self):
            # 주간 사용량 합산 - 비용 최적화 판단용 이 데이터를 기반으로 AI가 컨텍스트 초기화 시점을 결정
            pass