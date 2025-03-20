from datetime import datetime
from pytz import tzinfo

from bot.models import User
from Transition.settings import TZ

def is_active(user):
    access_time = user.access_time_end
    if datetime.now().replace(tzinfo=None) < access_time.replace(tzinfo=None):
        return True
    else:
        return False