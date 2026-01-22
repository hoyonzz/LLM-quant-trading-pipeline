import json
import os
from google import genai
from datetime import datetime


class ContextManager:
    def __init__(self, history_file="data/chat_history.json", portfolio_file="data/portfolio.json", api_key=None):
        self.history_file = history_file
        self.portfolio_path = portfolio_file # 계좌 상태 파일 추가
        self.max_target_tokens = 50000
        self.api_key = api_key

        # 요약 기능 위해 API 설정
        if api_key:
            self.client = genai.Client(api_key=self.api_key)

        # 데이터 로드
        self.history = self._load_json(self.history_file, default=[])
        self.portfolio = self._load_json(self.portfolio_path, default={"cash": 3000000, "holdings": {}})
        
        # 파일 초기화 확인
        if not os.path.exists(self.portfolio_path):
            self._save_portfolio()
        if not os.path.exists(self.history_file):
            self.save_history()

    def _load_json(self, filepath, default):
        if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    return default
        return default
    
    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
    
    def _save_portfolio(self):
        with open(self.portfolio_path, 'w', encoding='utf-8') as f:
            json.dump(self.portfolio, f, indent=4, ensure_ascii=False)
    
    def add_message(self, role, content):
        # 대화 추가 및 자동 토큰 관리
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_entry = {
            "role" : role,
            "parts": [{"text" : f"[{timestamp}] {content}"}]
        }
        self.history.append(message_entry)

        # 토큰 관리 - 매번 체크하기보다 하루 한번 체크
        if len(self.history) > 20 and self.api_key:
            self.summarize_context()
        
        self.save_history

    def get_full_context(self):
        # 현재까지의 모든 대화 이력 반환
        system_state = f"""
        [Current Portfolio State]
        - Cash : {self.portfolio.get('cash')} KRW
        - Holadings: {self.portfolio.get('holdings')}
        ----------------------------------------------------
        """
        return system_state, self.history
     
    def summarize_context(self):
        # 토큰이 너무 많아지면 오래된 기억을 압축
        if not self.client: return

        # 전체 대화의 50% 앞쪽 자르기
        cut_index = len(self.history) // 2
        old_conversations = self.history[:cut_index]
        recent_conversations = self.history[cut_index:]

        prompt = f"""
        아래는 과거의 투자 대화 내역이다.
        이 대화에서 '매매 근거', '매수/매도 가격', '투자에 대한 교훈' 위주로 핵심만 요약해줘.
        
        [대화 내역]
        {json.dumps(old_conversations, ensure_ascii=False)}
        """
        
        try:
            response = self.client.models.generate_content(
                model = "gemini-2.5-flash",
                contents =prompt
            )
            summary_text = response.text

            # 요약된 내용을 시스템 메시지로 변환하여 앞단에 붙임
            summary_message = {
                "role" : "user", 
                "parts" : [{"text": f"[과거 대화 요약]: {summary_text}"}]
            }

            # 히스토리 재구성 : [요약본] + 최근 대화
            self.history = [summary_message] + recent_conversations
            self.save_history()
            print(f"✅ 대화 내용이 요약되었습니다. (길이 축소: {cut_index}개 메시지 삭제됨)")
        except Exception as e:
            print(f"⚠️ 요약 실패: {e}")

    def update_portfolio(self, ticker, quantity, avg_price, current_cash):
        # 매수/매도 시 포트폴리오 파일 업데이트
        if quantity == 0:
            if ticker in self.portfolio['holdings']:
                del self.portfolio['holdings'][ticker]
        else:
            self.portfolio['holdings'][ticker] = {
                "quantity": quantity,
                "avg_price": avg_price
            }

        self.portfolio['cash'] = current_cash
        self._save_portfolio()


if __name__ == "__main__":
    cm = ContextManager()
    state, hist = cm.get_full_context()
    print("--- [ContextManager Test] ---")
    print(f"1. System State:\n{state}")
    print(f"2. History Count: {len(hist)}")

    # 포트폴리오 파일 생성 확인
    if os.path.exists("data/portfolio.json"):
        print("✅ data/portfolio.json 파일 확인됨")
    else:
        print("❌ data/portfolio.json 파일 생성 실패")