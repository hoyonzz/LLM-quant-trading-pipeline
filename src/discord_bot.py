import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()



class DiscordBot:
    def __init__(self):
        # 디스코드 웹훅 URL 로드