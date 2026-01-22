# src/config.py

SECTOR_CONFIGS = {
    "제약/바이오": {
        "index": "NBI(나스닥 바이오 지수), NYSE Arca Pharmaceutical Index",
        "keywords": ["FDA 승인", "임상 3상 데이터 발표", "Licensing-out", "생물보안법"],
        "global_peer": "Immunovant(IMVT), Argenx(ARGX), UCB",
        "risk_factors": ["임상 지연", "임상 중단", "금리 상단 유지", "경쟁 약물 출시"]
    },

    "반도체": {
        "index": "SOX(필라델피아 반도체 지수)",
        "keywords": ["수율", "HBM", "파운드리"],
        "global_peer": "NVIDIA, TSMC, ASML",
        "risk_factors": ["공급망 이슈", "수요 감소"]
    }
}

STOCK_DB = {
    "009420": {
        "name": "한올바이오파마",
        "sector": "제약/바이오",
        "ticker" : "009420",
        "us_peer_ticker": "IMVT",
        "key_pipeline": "HL161 (Batoclimab / IMVT-1401",
        "specific_queries": [
            "이뮤노반트(IMVT)의 간밤 뉴욕 증시 종가 및 거래량 특이사항",
            "FcRn 억제제 시장 내 아르젠엑스(ARGX) 대비 경쟁 우위 및 최신 뉴스",
            "HL161의 다음 임상 데이터 발표 예정 시점"
        ]
    },

    "237690": {
        "name": "에스티팜",
        "sector": "제약/바이오",
        "ticker": "237690",
        "key_pipeline": "올리고핵산 API, mRNA LNP",
        "specific_queries": [
            "미국 생물보안법(Biosecure Act) 입법 진행 상황 및 수혜 여부, 우시엡텍(WuXi AppTec) 동향",
            "글로벌 RNA 치료제 시장의 수주 트렌드",
            "올리고 공장 증설 관련 최신 리포트 요약"
        ]
    }
}

BRIEFING_TEMPLATES = {
    "morning_market": """
        [System: 현재 시간은 {datetime} (한국 시간)입니다.]
        [Mission: AI 트레이더를 위한 장전 매크로 및 시황 분석]

        지금까지 수집된 최신 데이터를 바탕으로 아래 항목을 분석하여 보고하세요.
        반드시, **JSON 형식**으로만 출력해야 합니다. (다른 설명 텍스트 금지)

        {{
            "us_market_summary": {{
                "indices": "다우, 나스닥, S&P500의 등략률 및 마감 수치",
                "vix": "VIX 지수 현재가 및 전일 대비 등락",
                "key_driver": "간밤 시장을 움직인 핵심 원인 (1문장 요약)"
            }},
            "korea_market_forecast": {{
                "expected_trend": "상승 / 하락 / 보합 중 택1",
                "reson": "미국 시장 및 야간 선물 지수를 기반으로 한 예측 근거",
            }},
            "sector_impact": {{
                "semiconductor": "필라델피아 반도체 지수 등락에 따른 국내 반도체 영향 (긍정/부정/중립)",
                "bio": "NBI 지수 및 금리 영향에 따른 국내 바이오 영향 (긍정/부정/중립)"
            }},
            "macro_key_variables" : {{
                "interest_rate" : "미국 10년물 국채 금리 변화",
                "exchange_rate" : "NDF 환율 추이"
            }}
        }}
    """,
    "specific_stock": """
        [System: 현재 시간은 {datetime} (한국 시간)입니다.]
        [Mission: 종목명 '{name}' {{ticker}}에 대한 딥 다이브(Deep Dive) 분석]

        해당 종목의 투자를 위해 다음 핵심 데이터를 리서치하여 **JSON형식**으로 보고하세요.

        {{
            "peer_status" : {{
                "global_peers" : "{peers}의 최근 주가 흐름 및 특이사항",
                "competitor_news" : "경쟁사의 임상, 실적, 악재 등 최신 뉴스"
            }},
            "catalyst_check" : {{
                "pipeline_status": "{pipeline} 관련 최신 업데이트 유무 및 내용",
                "upcoming_events": "가까운 시일 내 예정된 학회, 발표, 실적 공시 일정"
            }},
            "risk_factors":"현재 시장에서 우려하는 리스크 요인(없으면 '특이사항 없음')",
            "market_sentiment_score": "0 (공포/매도) ~ 100 (환호/매수) 사이의 정성적 점수",
            "summary_for_coptain": "AI Captain이 매매 판단을 내릴 수 있도록 3줄 요약"
        }}
    """
 }