BLOCKED_WORDS = [
    "ignore previous instructions",
    "reveal system prompt",
    "show your prompt",
    "show api key",
    "give api key",
    "developer prompt",
    "system prompt",
    "hack",
    "bypass",
    "jailbreak"
]


def check_guardrails(user_message):

    text = user_message.lower()

    for word in BLOCKED_WORDS:

        if word in text:

            return False

    return True