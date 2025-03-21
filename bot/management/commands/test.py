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
        bot.send_message(
            text="yes",
            chat_id=OWNER_ID
        )
