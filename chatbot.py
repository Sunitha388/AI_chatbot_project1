import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer clearly and politely.
"""


def get_ai_response(user_message, history=None):

    if not HF_TOKEN:
        return "Error: HF_TOKEN is missing. Check your .env file."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": "Qwen/Qwen3-4B-Instruct-2507",
        "messages": messages,
        "max_tokens": 300
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=20  # <-- important: fail fast instead of hanging
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "Error: Hugging Face API timed out."
    except requests.exceptions.HTTPError as e:
        return f"Error: Hugging Face API returned {response.status_code} — {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Hugging Face API."
    except Exception as e:
        return f"Error: {e}"