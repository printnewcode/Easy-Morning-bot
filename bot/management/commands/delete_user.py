from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from pytz import tzinfo

from bot import bot
from bot.utils import access_time
from bot.models import User
from bot.keyboards import START_BUTTONS
from Transition.settings import CHAT_ID, OWNER_ID


class Command(BaseCommand):
    help = "Deleting user from chat"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            is_active = access_time.is_active(user)
            if not is_active:
                try:
                    bot.ban_chat_member(chat_id=CHAT_ID, user_id=int(user.telegram_id), revoke_messages=False)
                except Exception as exc_:
                    bot.send_message(chat_id=OWNER_ID, text=exc_)
                try:
                    bot.send_message(
                        chat_id=int(user.telegram_id),
                        text="Ваш доступ к нашей беседе закончился. Продлите его, оплатив подписку",
                        reply_markup=START_BUTTONS,
                    )
                except:
                    pass
                user.is_paid = False
                user.save()
