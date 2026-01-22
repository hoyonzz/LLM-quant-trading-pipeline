import os
from google import genai
from dotenv import load_dotenv
from src.context_manager import ContextManager


load_dotenv()



class AICaptainEngine:
    def __init__(self, context_manager: ContextManager):
        # 대화 이력 및 포트폴리오 상태를 관리하는 객체
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.ctx_manager = context_manager

        if not self.api_key:
            raise ValueError("❌ .env파일의 GEMINI_API_KEY 오류")
        
        self.client = genai.Client(api_key=self.api_key)

        self.model_name = 'gemini-2.5-pro'

        # AI의 정체성을 시스템 프롬프트로 고정
        self.system_persona = """
        당신은 최상위권 퀀트 투자 전문가 'AI Captain'입니다.
        당신의 임무는 제공된 리서치(Macro)와 실시간 수치(Micro) 데이터를 통합 분석하는 것입니다.
        - 결론은 [매수 / 매도 / 관망 / 손절] 중 하나를 반드시 선택할 것.
        - 어떤 상황에서도 손절가(SL)를 반드시 숫자로 제시할 것.
        -목표 : 리스크 관리를 최우선으로 하여 사용자의 수익을 극대화한다.
        - 감정적인 표현은 배제하고 오직 데이터와 논리로만 리포트를 작성할것.
        """

    def generate_strategy(self, stock_name, research_data, market_data):
        # 리서치와 수치를 통합하여 최종 전략 시나리오 생성
        # Step 1: ContextManager로부터 포트폴리오 요약과 이전 대화 이력(History) 수신
        system_state, history = self.ctx_manager.get_full_context()

        # Step 2: 현재 시점의 통합 데이터 구성
        input_data = f"""
        {system_state}
        
        [Market Research: {stock_name}]
        {research_data}
        
        [Real-time Market Data]
        - 현재가: {market_data.get('current_price', 0)}원
        - 등락률: {market_data.get('change_rate', 0.0)}%
        - 체결강도: {market_data.get('volume_strength', 0.0)}%
        - 시장 등락: 상승 {market_data.get('rising', 'N/A')} / 하락 {market_data.get('falling', 'N/A')}
        
        위 데이터를 기반으로 AI Captain의 최종 전략 리포트를 작성하라.
        분석을 시작하라. 리스크가 크다면 가차 없이 '손절' 또는 '관망'을 지시하라.
        
        결과는 반드시 정해진 양식(Signal, Diagnosis, Action Plan)에 맞춰 한국어로 보고하라.
        """
    
        # Step 3: Gemini Pro에게 질의
        full_prompt = f"{self.system_persona}\n\n{input_data}"

        current_message = {"role": "user", "parts": [{"text": full_prompt}]}

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=history + [current_message]
            )
            strategy_result = response.text


            # Step 4: 기억 업데이트
            self.ctx_manager.add_message("user", input_data)
            self.ctx_manager.add_message("model", strategy_result)

            return strategy_result
        except Exception as e:
            return f"❌ Gemini API 오류 발생: {str(e)}"