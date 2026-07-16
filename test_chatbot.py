import uuid

from chatbot import get_ai_response
from history import save_chat
from memory import get_chat_history
from guardrails import check_guardrails

session_id = str(uuid.uuid4())

print("🤖 AI Chatbot Started")
print("Type 'exit' to quit.\n")

while True:

    question = input("You : ")

    if question.lower() == "exit":
        break

    # Guardrails Check
    if not check_guardrails(question):

        answer = "❌ Sorry, I can't process that request."

    else:

        history = get_chat_history(session_id)

        answer = get_ai_response(question, history)

    print("\nAI :", answer)

    # Save chat to database
    save_chat(
        session_id,
        question,
        answer
    )