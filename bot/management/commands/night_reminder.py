from django.core.management.base import BaseCommand, CommandError

from bot import bot
from bot.keyboards import SUBSCRIPTION_BUTTONS
from bot.utils import access_time
from bot.models import User


class Command(BaseCommand):
    help = "Remind for user at the end of the day"

    def handle(self, *args, **options):
        users = User.objects.filter(is_paid = False)
        for user in users:
            is_active = access_time.is_active(user)
            if is_active:
                bot.send_message(
                    text="Понравился наш канал? Оплати подписку и получи полный доступ!",
                    chat_id=user.telegram_id,
                    reply_markup=SUBSCRIPTION_BUTTONS,
                )
