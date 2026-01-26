from google import genai
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


print(" 사용가능한 목록 모델: ")
for model in client.models.list():
    print(f"Model: {model.name}")
    print(f"Display Name: {model.display_name}")
    print(f"Version: {model.version}")
    print(f"Token Limit: Input={model.input_token_limit}, Output={model.output_token_limit}")
    print(f"Supported Actions: {model.supported_actions}")
    print("---")