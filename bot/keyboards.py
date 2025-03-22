from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Transition.settings import LINK

"User"
back = InlineKeyboardButton(text="Назад", callback_data="back")
START_BUTTONS = InlineKeyboardMarkup()
subscription = InlineKeyboardButton(text="Покупка доступа к чату", callback_data="menu_subscription")
other = InlineKeyboardButton(text="Другое", callback_data="pay_other")
link = InlineKeyboardButton(text="🎁  попробуй", callback_data="menu_link")
START_BUTTONS.add(subscription).add(other).add(link)

SUBSCRIPTION_BUTTONS = InlineKeyboardMarkup()
seven_days = InlineKeyboardButton(text="7 дней", callback_data="pay_7")
fourteen_days = InlineKeyboardButton(text="14 дней", callback_data="pay_14")
month = InlineKeyboardButton(text="1 месяц", callback_data="pay_30")
vip_access = InlineKeyboardButton(text="🔥 Ultimate", callback_data="pay_vip")
SUBSCRIPTION_BUTTONS.add(seven_days, fourteen_days, month).add(vip_access).add(back)

LINK_MENU_BUTTONS = InlineKeyboardMarkup()
link_url = InlineKeyboardButton(text="Перейти в чат", url=LINK)
LINK_MENU_BUTTONS.add(link_url).add(back)


OTHER_BUTTONS = InlineKeyboardMarkup()
other_easy_15 = InlineKeyboardButton(text="Купить курс EASY 15 (дисциплина и тренировки для всего тела)",
                                     url="https://tvorimtelom.ru/easy15")
other_individual_exc = InlineKeyboardButton(text="Купить индивидуальные занятия", url="https://tvorimtelom.ru/go")
other_contact = InlineKeyboardButton(text="Связаться со мной", url = "https://tvorimtelom.ru/go")
OTHER_BUTTONS.add(other_easy_15).add(other_individual_exc).add(other_contact).add(back)

BACK_BUTTON = InlineKeyboardMarkup()
BACK_BUTTON.add(back)

"Admin"

ADMIN_PAY = InlineKeyboardMarkup()
pay_accept = InlineKeyboardButton(text="Принять", callback_data="admin-pay_accept")
pay_decline = InlineKeyboardButton(text="Отказать", callback_data="admin-pay_decline")
ADMIN_PAY.add(pay_accept, pay_decline)

ADMIN = InlineKeyboardMarkup()
check_vip = InlineKeyboardButton(text="Посмотреть список Ultimate-пользователей", callback_data="admin_vip")
ADMIN.add(check_vip)