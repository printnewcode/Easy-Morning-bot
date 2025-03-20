from functools import wraps

from Transition.settings import CHAT_ID

def is_chat(func):
    @wraps(func)
    def wrapped(message) -> None:
        if message.chat.id == int(CHAT_ID):
            return True
        else:
            return False
        return func(message)
    return wrapped

