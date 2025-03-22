from django.core.management.base import BaseCommand, CommandError

from bot import bot
from bot.utils import access_time
from bot.models import User


class Command(BaseCommand):
    help = "Remind for user during the day"

    def handle(self, *args, **options):
        users = User.objects.filter(is_paid = False)
        for user in users:
            is_active = access_time.is_active(user)
            if is_active:
                bot.send_message(
                    text="Как ощущения после первой практики?",
                    chat_id=user.telegram_id,
                )
