import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()



class DiscordBot:
    def __init__(self):
        # 디스코드 웹훅 URL 로드
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send_text(self, message):
        # 기본적인 텍스트 메시지 전송
        payload = {"content": message}
        response = requests.post(self.webhook_url, json=payload)
        return response.status_code
    
    def send_embed(self, title, description, fields=None, color=0x00ff00):
        """
        전문가용 'Embed' 카드 메시지 전송
        - title: 제목
        - description: 내용
        - fields: [{name: "제목", value: "내용", inline: True}] 형태의 리스트
        - color : 왼쪽 바의 색상 (기본 초록색)
        """
        # 디스코드가 요구하는 Embed 규격에 맞춰 데이터 구성
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnot().isoformat(), # 메시지 발생 시각
            "footer": {"text": "LQSP Trading System"}
        }

        if fields:
            embed["fields"] = fields

        payload = {
            "username" : "LQSP_Strategist", # 봇 이름 설정
            "embeds": [embed]
        }

        response = requests.post(self.webhook_url, json=payload)

        if response.status_code == 204:
            print("✅ 디스코드 알림 전송 완료!")
        else:
            print(f"❌ 전송 실패: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # 테스트 실행
    bot = DiscordBot()

    # 1. 일반 텍스트 테스트
    bot.send_text("🚀 LQSP 시스템이 가동되었습니다.")

    # 2. 전문적인 Embed 메시지 테스트
    test_fields = [
        {"name": "종목명", "value": "한올바이오파마", "inline": True},
        {"name": "현재가", "value": "51,000원", "inline": True},
        {"name": "상태", "value": "관망중", "inline": False}
    ]
    bot.send_embed(
        title="🔔 장전 시장 브리핑",
        description="현재 시장 변동성이 큽니다. 리스크 관리에 유의하세요.",
        fields=test_fields,
        color=0xff0000 #발간색
    )