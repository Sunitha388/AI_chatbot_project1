import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "model": "Qwen/Qwen3-4B-Instruct-2507",
    "messages": [
        {"role": "user", "content": "hello"}
    ],
    "max_tokens": 50
}

try:
    r = requests.post(
        "https://router.huggingface.co/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=20
    )
    print("STATUS:", r.status_code)
    print("BODY:", r.text)
except Exception as e:
    print("EXCEPTION:", e)