from fastapi import FastAPI
from pydantic import BaseModel

from chatbot import get_ai_response
from history import save_chat
from memory import get_chat_history
from guardrails import check_guardrails

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.get("/")
def home():
    return {
        "message": "AI Chatbot API is Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if not check_guardrails(request.message):
        answer = "❌ Sorry, I can't process that request."
    else:
        history = get_chat_history(request.session_id)
        answer = get_ai_response(request.message, history)

    save_chat(request.session_id, request.message, answer)

    return {
        "response": answer
    }