from huggingface_hub import login
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

# 환경 변수에서 Hugging Face 토큰을 가져옵니다.
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# Hugging Face에 로그인합 니다.
async def authenticate() -> bool:
    print("Trying huggingface login")
    if huggingface_token:
        try:
            await login(token=huggingface_token)
            print("Login succeed")
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    else:
        # Hugging Face token이 없을 경우 Snackbar로 경고 메시지 출력
        print("no token")
        return False
