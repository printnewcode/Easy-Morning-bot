from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Transition.settings import LINK

"User"

START_BUTTONS = InlineKeyboardMarkup()
seven_days = InlineKeyboardButton(text="7 дней", callback_data="pay_7")
fourteen_days = InlineKeyboardButton(text="14 дней", callback_data="pay_14")
month = InlineKeyboardButton(text="1 месяц", callback_data="pay_30")
vip_access = InlineKeyboardButton(text="🔥 VIP-доступ", callback_data="pay_vip")
other = InlineKeyboardButton(text="Другое", callback_data="pay_other")
link = InlineKeyboardButton(text="Наш чат", url=LINK)
START_BUTTONS.add(seven_days, fourteen_days, month).add(vip_access).add(other).add(link)

OTHER_BUTTONS = InlineKeyboardMarkup()
other_easy_15 = InlineKeyboardButton(text="Купить курс EASY 15 (дисциплина и тренировки для всего тела)",
                                     callback_data="pay-other_easy15")
other_individual_exc = InlineKeyboardButton(text="Купить индивидуальные занятия", callback_data="pay-other_ind")
other_training = InlineKeyboardButton(text="Купить пакет тренировки + питание", callback_data="pay-other_training")
OTHER_BUTTONS.add(other_easy_15).add(other_individual_exc).add(other_training)

BACK_BUTTON = InlineKeyboardMarkup()
back = InlineKeyboardButton(text="Назад", callback_data="back")
BACK_BUTTON.add(back)

"Admin"

ADMIN_PAY = InlineKeyboardMarkup()
pay_accept = InlineKeyboardButton(text="Принять", callback_data="admin-pay_accept")
pay_decline = InlineKeyboardButton(text="Отказать", callback_data="admin-pay_decline")
ADMIN_PAY.add(pay_accept, pay_decline)
