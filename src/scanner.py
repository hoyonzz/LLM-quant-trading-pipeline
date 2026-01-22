import json
import re

class MarketScanner:
    def __init__(self, researcher):
        self.researcher = researcher

    def scan_leading_sectors(self):
        # Step 1: 현재 시장을 주도하는 TOP 3 섹터, 근거 발굴
        prompt = """
        [Mission: Find Today's Leading Sectors]
        현재 한국 및 미국 증시의 실시간 수급과 뉴스 데이터를 분석하여, 현재 자금 유입이 강하고 주가 상승률이 높은 'TOP 3 섹터'를 찾아라.
        반드시 아래 JSON 형식으로만 답변하라:
        {
            "sectors": [
                {"name": "섹터명1", "reason":"상승 이유 요약"},
                {"name": "섹터명2", "reason":"상승 이유 요약"},
                {"name": "섹터명3", "reason":"상승 이유 요약"},
            ]
        }
        """

        response = self.researcher.get_custom_report(prompt)
        return self._parse_json(response)
    
        
    def get_top_picks(self, sector_name):
        # Step 2: 특정 섹터 내 대장주 발굴 및 시스템 등록용 정보 추출
        prompt = """
        [Mission: Find Top Picks in '{sector_name}']
        '{sector_name}' 섹터에서 다음 조건을 만족하는 대장주 2개와 유망주 1개를 선정하라.
        조건 : 거래 대금이 충분하며 외인/기관 수급이 유입되는 종목.

        결과는 반드시 아래 리스트 형식을 포함한 JSON으로만 답변하라:
        [
            {
                "ticker" : "종목코드",
                "name" : "종목명",
                "sector" : "섹터명",
                "key_pipeline" : "핵심 재료/제품",
                "global_peer": "관련 글로벌 기업",
                "specific_queries":["리서치 시 강조할 질문1", "질문2"]
            },
            {
                "ticker" : "종목코드",
                "name" : "종목명",
                "sector" : "섹터명",
                "key_pipeline" : "핵심 재료/제품",
                "global_peer": "관련 글로벌 기업",
                "specific_queries":["리서치 시 강조할 질문1", "질문2"]
            },
            {
                "ticker" : "종목코드",
                "name" : "종목명",
                "sector" : "섹터명",
                "key_pipeline" : "핵심 재료/제품",
                "global_peer": "관련 글로벌 기업",
                "specific_queries":["리서치 시 강조할 질문1", "질문2"]
            },
        ]
        """

        response = self.researcher.get_custom_report(prompt)
        return self._parse_json(response)
    
    def _parse_json(self, text):
        # AI 답변에서 JSON블록만 추출하여 파이썬 객체로 반환
        try:
            # ```json ... ``` 형태나 순수 {} 형태에서 json만 추출
            match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(text)
        except Exception as e:
            print(f"❌ JSON 파싱 에러: {e}")
            return None