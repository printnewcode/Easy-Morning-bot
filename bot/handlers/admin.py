import os

from functools import wraps

from bot import bot
from bot.models import User
from bot.utils import get_User
from bot.keyboards import ADMIN

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
    try:
        video = os.path.join("files", "video-note.mp4")
        with open(video, "rb") as video_note:
            bot.send_video_note(message.chat.id, video_note)
    except Exception as e:
        bot.send_message(
            text=e,
            chat_id=message.chat.id
        )
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