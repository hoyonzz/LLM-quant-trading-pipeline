import os
import sys
import time
from dotenv import load_dotenv

from src.auth import KISAuth
from src.researcher import PerplexityResearcher
from src.market_data import MarketDataManager
from src.discord_bot import DiscordBot
from src.context_manager import ContextManager
from src.captain_engine import AICaptainEngine
from src.gsheet_manager import GSheetManager
from src.config import STOCK_DB


load_dotenv()



def run_single_ticker(ticker, auth, bot, researcher, md_manager, ctx_manager, engine, gs_manager):
    # 단일 종목에 대한 분석 파이프라인 실행 함수
    stock_name = STOCK_DB[ticker]['name']
    print(f"🏁 [{stock_name} ({ticker})] 분석 프로세스 시작...")

    try:
        # Step 1: 데이터 수집
        print(f"📡 [{stock_name}] 리서치 데이터 수집 중...")
        research_report = researcher.get_report("specific_stock", ticker=ticker)

        print(f"📊 [{stock_name}] 실시간 시세 수집 중...")
        market_stats = md_manager.get_stock_price(ticker)
        market_breath = md_manager.get_market_breath()

        if market_breath:
            market_stats.update(market_breath)

        if not research_report or not market_stats:
            error_msg = f"❌ [{stock_name}] 데이터 수집 실패. 해당 종목 스킵."
            print(error_msg)
            bot.send_text(error_msg)
            return
        
        # Step 2: 전략 수립
        print(f"🧠 [{stock_name}] AI Captain 전략 수립 중...")
        final_strategy = engine.generate_strategy(stock_name, research_report, market_stats)

        # Step 3: 결과 저장 및 전송
        gs_manager.append_research(stock_name, final_strategy)

        color = 0x00ff00 if "매수" in final_strategy else 0xff0000

        bot.send_embed(
            title=f"🎖️ AI Captain 전략 보고서 : {stock_name} ({ticker})",
            description=final_strategy,
            fields = [
                {"name": "현재가", "value": f"{market_stats.get('current_price')}원", "inline": True},
                {"name": "체결강도", "value" : f"{market_stats.get('volume_strength')}%", "inline": True},
                {"name": "시장등락", "value": f"⬆️{market_stats.get('rising')} / ⬇️{market_stats.get('falling')}", "inline" : True}
            ],
            color=color
        )
        print(f"✅ [{stock_name}] 분석 완료.")

    except Exception as e:
        print(f"❗ [{stock_name}] 처리 중 에러 발생: {e}")

def main():
    print("🚀 LQSP v0.3.0 전체 파이프라인 가동")

    # 1. 공통 모듈 초기화
    try:
        auth = KISAuth(mode="mock")
        bot = DiscordBot()
        researcher = PerplexityResearcher()
        md_manager = MarketDataManager(auth)
        ctx_manager = ContextManager(api_key=os.getenv("GEMINI_API_KEY"))
        engine = AICaptainEngine(ctx_manager)
        gs_manager = GSheetManager()
    except Exception as e:
        print(f"❌ 초기화 단계에서 치명적 오류: {e}")
        return
        
    # 2. Config에 등록된 모든 종목 순회
    target_tickers = list(STOCK_DB.keys())

    print(f"📋 분석 대상 종목: {len(target_tickers)}개")

    for ticker in target_tickers:
        run_single_ticker(
            ticker, auth, bot, researcher, md_manager, ctx_manager, engine, gs_manager
        )
        print("⏳ 5초 대기 중...")
        time.sleep(5)
    print("✅ 모든 종목에 대한 분석이 종료되었습니다.")

if __name__ == "__main__":
        main()

