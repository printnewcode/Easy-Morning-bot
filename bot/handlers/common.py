import os

from datetime import datetime, timedelta
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
    InputFile
)

from bot import bot
from bot.models import User, Goods
from bot.texts import SUBSCRIBE_TEXT, NUMBER, SUBSCRIPTION_TEXT, FIRST_DAY, EASY_M_TEXT
from bot.keyboards import START_BUTTONS, OTHER_BUTTONS, back, BACK_BUTTON, SUBSCRIPTION_BUTTONS, LINK_MENU_BUTTONS, ENTER_BUTTONS, EASY_15, CONTACT_BUTTONS, BACK_PAY_BUTTON, BACK_EXAMPLE
from bot.utils import get_User, access_time
from bot.static.goods import goods, other_goods
from Transition.settings import LINK, CHAT_ID, REPLY_ID


def start(message: Message):
    user_id = message.from_user.id
    user = User.objects.filter(telegram_id=user_id)
    video = os.path.join(os.path.dirname(__file__), "..", "files", "enter.mp4")
    with open(video, "rb") as video_note:
        bot.send_video_note(message.chat.id, video_note)

    bot.send_message(
        text="Выбери, что тебя интересует!",
        chat_id=user_id,
        reply_markup=ENTER_BUTTONS,
    )
    
    """bot.send_message(
        text=SUBSCRIBE_TEXT,
        chat_id=user_id,
        reply_markup=START_BUTTONS,
    )"""
    selected_videos = [
        os.path.join(os.path.dirname(__file__), "..", "files", "videos.mp4"),
        os.path.join(os.path.dirname(__file__), "..", "files", "videos_2.mp4"),
        os.path.join(os.path.dirname(__file__), "..", "files", "videos_3.mp4"),
        os.path.join(os.path.dirname(__file__), "..", "files", "videos_4.mp4")
    ]
    if not user.exists():
        user = User.objects.create(
            telegram_id=user_id,
            access_time_end=(datetime.now() + timedelta(days=1)),
            username=message.from_user.username,
        )
        user.save()
        try:
            for video in selected_videos:
                bot.send_video(
                    chat_id=message.chat.id,
                    video=InputFile(video)
                )
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text=e
            )
        """bot.send_message(
            text=f"{FIRST_DAY}\n\n🎁  попробуй: {LINK}",
            chat_id=user_id,
        )"""
    else:
        user.first().username = message.from_user.username
        user.first().save()

def menu_buttons(call: CallbackQuery):
    """Обработка кнопок меню"""
    _, data = call.data.split("_")
    bot.delete_messages(
        message_ids=[call.message.id,call.message.id-1],
        chat_id=call.message.chat.id
        )
    if data == "project":
        video = os.path.join(os.path.dirname(__file__), "..", "files", "project.mp4")
        with open(video, "rb") as video_note:
            bot.send_video_note(call.message.chat.id, video_note)
        bot.send_message(
            text=EASY_M_TEXT,
            chat_id=call.message.chat.id,
            reply_markup=SUBSCRIPTION_BUTTONS,
        )
    if data == "course":
        video = os.path.join(os.path.dirname(__file__), "..", "files", "course.mp4")
        with open(video, "rb") as video_note:
            bot.send_video_note(call.message.chat.id, video_note)
        bot.send_message(
            text="Быстрее начинай курс!",
            chat_id=call.message.chat.id,
            reply_markup=EASY_15,
        )
    if data == "ind-exc":
        video = os.path.join(os.path.dirname(__file__), "..", "files", "contact.mp4")
        with open(video, "rb") as video_note:
            bot.send_video_note(call.message.chat.id, video_note)
        bot.send_message(
            text="Свяжись со мной и получи обратную связь!",
            chat_id=call.message.chat.id,
            reply_markup=CONTACT_BUTTONS,
        )
    
    """if data == "subscription":
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
        )"""

def pay_handler(call: CallbackQuery):
    _, data = call.data.split("_")
    bot.delete_message(
        message_id=call.message.id-1,
        chat_id = call.message.chat.id,
    )
    if data == "example":
        try:
            bot.delete_message(
                message_id=call.message.id,
                chat_id = call.message.chat.id,
                )
            bot.forward_messages(
                from_chat_id=CHAT_ID,
                chat_id=call.message.chat.id,
                message_ids=REPLY_ID,
            )
            bot.send_message(
                text="Вернуться в меню",
                chat_id = call.message.chat.id,
                reply_markup=BACK_EXAMPLE,
            )
        except Exception as e:
            bot.send_message(
                chat_id=call.message.chat.id,
                text=e,
                )
        
    if data == "7" or data == "14" or data == "30":
        price = goods.get(data)
        if data == "30":
            try:
                if get_User.get_user(id=call.message.chat.id).is_monthly:
                    price = goods.get("30_1")
            except:
                price = goods.get(data)
            
        msg = bot.edit_message_text(
            text=f"Для получения доступа на {data} дней необходимо оплатить {price} руб.\nПеревод по СБП на номер {NUMBER}\nПосле этого нужно отправить фото/чек перевода сюда, следующим сообщением!",
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            reply_markup=BACK_PAY_BUTTON,
        )
        
        bot.register_next_step_handler(msg, pay_sbp_handler, data)

    if data == "vip":
        price = goods.get("vip")
        msg = bot.edit_message_text(
            text=f"Для получения Ultimate-доступа необходимо оплатить {price} руб.\nПеревод по СБП на номер {NUMBER}\nПосле этого нужно отправить фото/чек перевода сюда, следующим сообщением!",
            message_id=call.message.id,
            chat_id=call.message.chat.id,
            reply_markup=BACK_PAY_BUTTON,
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
    if message.text == "/start":
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        start(message=message)
        return
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
    username = get_User.get_user(message.chat.id).username
    text=f"Новая оплата!\nПользователь @{username} оплатил {data}. Вот чек!" 
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
    bot.delete_messages(
        message_ids=[call.message.id, call.message.id-1],
        chat_id=call.message.chat.id,
    )
    video = os.path.join(os.path.dirname(__file__), "..", "files", "enter.mp4")
    with open(video, "rb") as video_note:
        bot.send_video_note(call.message.chat.id, video_note)
    bot.send_message(
        text="Выбери, что тебя интересует!",
        chat_id=call.message.chat.id,
        reply_markup=ENTER_BUTTONS,
    )
def back_pay_button(call: CallbackQuery):
    _, data = call.data.split("_")
    if data == "pay-1":
        # Удаление сообщения и 4 видео над ним
        bot.delete_messages(
            message_ids=[call.message.id, call.message.id-1, call.message.id-2, call.message.id-3, call.message.id-4],
            chat_id=call.message.chat.id
        )
    else:
        bot.delete_message(
            message_id=call.message.id,
            chat_id=call.message.chat.id,
        )
    video = os.path.join(os.path.dirname(__file__), "..", "files", "project.mp4")
    with open(video, "rb") as video_note:
        bot.send_video_note(call.message.chat.id, video_note)
    bot.send_message(
        text=EASY_M_TEXT,
        chat_id=call.message.chat.id,
        reply_markup=SUBSCRIPTION_BUTTONS,
        )



def unban_user(user):
    bot.unban_chat_member(chat_id=CHAT_ID, user_id=user.telegram_id)
