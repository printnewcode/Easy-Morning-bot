from bot.models import User

def get_user(id):
    user = User.objects.filter(telegram_id=id).first()
    return user
