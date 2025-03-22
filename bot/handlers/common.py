from datetime import datetime, timedelta
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

from bot import bot
from bot.models import User, Goods
from bot.texts import SUBSCRIBE_TEXT, NUMBER, SUBSCRIPTION_TEXT, FIRST_DAY
from bot.keyboards import START_BUTTONS, OTHER_BUTTONS, back, BACK_BUTTON, SUBSCRIPTION_BUTTONS, LINK_MENU_BUTTONS
from bot.utils import get_User, access_time
from bot.static.goods import goods, other_goods
from Transition.settings import LINK, CHAT_ID


def start(message: Message):
    user_id = message.from_user.id
    user = User.objects.filter(telegram_id=user_id)

    bot.send_message(
        text=SUBSCRIBE_TEXT,
        chat_id=user_id,
        reply_markup=START_BUTTONS,
    )
    
    if not user.exists():
        user = User.objects.create(
            telegram_id=user_id,
            access_time_end=(datetime.now() + timedelta(days=1)),
            username=message.from_user.username,
        )
        user.save()
        bot.send_message(
            text=f"{FIRST_DAY}\n\n🎁  попробуй: {LINK}",
            chat_id=user_id,
        )
    else:
        user.first().username = message.from_user.username
        user.first().save()

def menu_buttons(call: CallbackQuery):
    """Обработка кнопок меню"""
    _, data = call.data.split("_")
    if data == "subscription":
        bot.edit_message_text(
            message_id=call.message.id,
            text=SUBSCRIPTION_TEXT,
            chat_id=call.message.chat.id,
            reply_markup=SUBSCRIPTION_BUTTONS
        )
    if data == "link":
        bot.edit_message_text(
            message_id=call.message.id,
            text=FIRST_DAY,
            chat_id=call.message.chat.id,
            reply_markup=LINK_MENU_BUTTONS
        )

def pay_handler(call: CallbackQuery):
    _, data = call.data.split("_")
    if data == "7" or data == "14" or data == "30":
        
        price = goods.get(data)
        if data == "30":
            try:
                if get_User.get_user(id=call.message.chat.id).is_monthly:
                    price = price[1]
            except:
                price = price[0]
        msg = bot.edit_message_text(
            text=f"Для получения доступа на {data} дней необходимо оплатить {price} руб.\nПеревод по СБП на номер {NUMBER}\nПосле этого нужно отправить фото/чек перевода сюда, следующим сообщением!",
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            reply_markup=BACK_BUTTON,
        )
        
        bot.register_next_step_handler(msg, pay_sbp_handler, data)

    if data == "vip":
        price = goods.get("vip")
        msg = bot.edit_message_text(
            text=f"Для получения VIP-доступа необходимо оплатить {price} руб.\nПеревод по СБП на номер {NUMBER}\nПосле этого нужно отправить фото/чек перевода сюда, следующим сообщением!",
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            reply_markup=BACK_BUTTON,
        )
        
        bot.register_next_step_handler(msg, pay_sbp_handler, data)

    if data == "other":
        
        bot.edit_message_text(
            text="Вот дополнительные услуги, которые мы можем вам оказать",
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            reply_markup=OTHER_BUTTONS,
        )
        


def pay_sbp_handler(message: Message, data: str):
    bot.send_message(
        text="Чек принят! Ожидайте его проверки администратором. Если все хорошо, бот пришлет вам сообщение.",
        chat_id=message.chat.id
    )
    admin = User.objects.filter(is_admin=True).first()

    ADMIN_PAY = InlineKeyboardMarkup()
    pay_accept = InlineKeyboardButton(text="Принять", callback_data=f"admin-pay_accept-{message.chat.id}-{data}")
    pay_decline = InlineKeyboardButton(text="Отказать", callback_data=f"admin-pay_decline-{message.chat.id}-{data}")
    ADMIN_PAY.add(pay_accept, pay_decline)

    data = data + " дней" if data == "7" or data == "14" or data == "30" else "VIP-доступ"
    bot.forward_message(
        chat_id=int(admin.telegram_id),
        message_id=message.id,
        from_chat_id=message.chat.id
    )

    text=f"Новая оплата!\nПользователь @{message.from_user.username} оплатил {data}. Вот чек!" 
    bot.send_message(
        text=text,
        chat_id=int(admin.telegram_id),
        reply_markup=ADMIN_PAY
    )
    


def other_callback_handler(call: CallbackQuery):
    _, goods = call.data.split("_")
    good = other_goods.get(goods)
    bot.send_message(
        text="Ожидайте! Мы передали ваш контакт администратору, скоро с вами свяжутся",
        chat_id=call.message.chat.id,
    )
    admin = User.objects.filter(is_admin=True).first()

    bot.send_message(
        text=f"Пользователь @{call.from_user.username} выбрал **{good}**. Свяжитесь с ним!",
        chat_id=int(admin.telegram_id),
        parse_mode="Markdown"
    )


def admin_pay_handler(call: CallbackQuery):
    _, answer = call.data.split("_")
    answer, id, days = answer.split("-")
    user = get_User.get_user(id)
    admin = User.objects.filter(is_admin=True).first()
    is_active = access_time.is_active(user)
    if answer == "accept":
        user.is_paid = True
        if days == "7" or days == "14" or days == "30":
            if days == "30":
                user.is_monthly = True
            else:
                user.is_monthly = False
            if not is_active:
                user.access_time_end = (datetime.now().replace(tzinfo=None) + timedelta(days=int(days)))
            else:
                user.access_time_end += timedelta(days=int(days))
        else:
            user.access_time_end += timedelta(days=30)
            user.is_vip = True
            bot.send_message(
                text=f"Пользователь @{call.message.from_user.username} оплатил Ultimate. Свяжитесь с ним! (Посмотреть список приобретших можно в /admin)",
                chat_id=int(admin.telegram_id)
            )
        user.save()
        try:
            unban_user(user)
        except:
            pass
        bot.send_message(
            text=f"Чек одобрен!",
            chat_id=int(user.telegram_id),
        )
    else:
        bot.send_message(
            text="Ваш чек не одобрен! Проверьте все и отправьте еще раз",
            chat_id=int(user.telegram_id),
        )
    bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
    bot.delete_message(message_id=call.message.id-1, chat_id=call.message.chat.id)

def back_button(call: CallbackQuery):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    bot.edit_message_text(
        text=SUBSCRIBE_TEXT,
        message_id=call.message.id,
        chat_id=call.message.chat.id,
        reply_markup=START_BUTTONS,
    )


def unban_user(user):
    bot.unban_chat_member(chat_id=CHAT_ID, user_id=user.telegram_id)
