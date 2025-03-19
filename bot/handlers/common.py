from datetime import datetime, timedelta
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

from bot import bot
from bot.models import User, Goods
from bot.texts import SUBSCRIBE_TEXT, NUMBER
from bot.keyboards import START_BUTTONS, OTHER_BUTTONS, ADMIN_PAY
from bot.static.goods import goods

def start(message: Message):
    user_id = message.from_user.id
    user = User.objects.filter(telegram_id=user_id)

    if not user.exists():
        user = User.objects.create(
                telegram_id=user_id,
                access_time_end=(datetime.now() + timedelta(days=1)),
            )
        user.save()
       
    bot.send_message(
        text = SUBSCRIBE_TEXT,
        chat_id = user_id,
        reply_markup = START_BUTTONS,
    )

def pay_handler(call: CallbackQuery):
    _, data = call.data.split("_")
    if data == "7" or data == "14" or data == "30":
        price = goods.get(data) # Получаем цену
        msg = bot.edit_message_text(
            text = f"Для получения доступа на {data} дней необходимо оплатить {price} руб.\nПеревод по СБП на номер {NUMBER}\nПосле этого нужно отправить фото/чек перевода сюда, следующим сообщением!",
            message_id = call.message.id,
            chat_id = call.message.chat.id,
        )
        bot.register_next_step_handler(msg, pay_sbp_handler, data)
    
    if data == "vip":
        price = goods.get("vip")
        msg = bot.edit_message_text(
            text = f"Для получения VIP-доступа необходимо оплатить {price} руб.\nПеревод по СБП на номер {NUMBER}\nПосле этого нужно отправить фото/чек перевода сюда, следующим сообщением!",
            message_id = call.message.id,
            chat_id = call.message.chat.id,
        )
        bot.register_next_step_handler(msg, pay_sbp_handler, data)

    if data == "other":
        bot.edit_message_text(
            text = "Вот дополнительные услуги, которые мы можем вам оказать",
            message_id = call.message.id,
            chat_id = call.message.chat.id,
            reply_markup = OTHER_BUTTONS
        )
        

def pay_sbp_handler(message: Message, data: str):
    bot.send_message(
        text = "Чек принят! Ожидайте его проверки администратором. Если все хорошо, бот пришлет вам сообщение.",
        chat_id = message.chat.id
    )
    admin = User.objects.filter(is_admin=True).first()
    data = data + " дней" if data == "7" or data == "14" or data == "30" else "VIP-доступ"
    bot.forward_message(
        chat_id = int(admin.telegram_id),
        message_id = message.id,
        from_chat_id = message.chat.id
    )
    bot.send_message(
        text = f"Новая оплата!\nПользователь {message.chat.id} оплатил {data}. Вот чек!",
        chat_id = int(admin.telegram_id),
        reply_markup = ADMIN_PAY
    )