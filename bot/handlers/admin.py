import os

from functools import wraps

from bot import bot
from bot.models import User
from bot.utils import get_User, access_time
from bot.keyboards import ADMIN
from Transition.settings import CHAT_ID

def admin_permission(func):
    """
    Checking user for admin permission to access the function.
    """

    @wraps(func)
    def wrapped(message) -> None:
        user_id = message.from_user.id
        user = User.objects.get(telegram_id=user_id)
        if not user.is_admin:
            bot.send_message(user_id, '⛔ У вас нет администраторского доступа')
            return
        return func(message)

    return wrapped

@admin_permission
def admin_panel(message):
    bot.send_message(
        text="Добро пожаловать в Админ-панель!",
        chat_id=message.chat.id,
        reply_markup=ADMIN
    )

def check_ultimate(call):
    vip_users = User.objects.filter(is_vip=True)
    text=""
    for vip in vip_users:
        name = get_User.get_user(vip.telegram_id)
        text += f"@{name.username}\n"
    bot.send_message(
        text=text,
        chat_id=call.message.chat.id,
    )

def check_free_trial(call):
    free_trial_users = User.objects.filter(is_paid=False)
    for user in free_trial_users:
        if bot.get_chat_member(chat_id=CHAT_ID, user_id=int(user.telegram_id)).status == "member":
            text += f"@{user.username}\n"
    bot.send_message(
        text=text,
        chat_id=call.message.chat.id
    )