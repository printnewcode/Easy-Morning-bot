from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Transition.settings import LINK

"User"
other_easy_15 = InlineKeyboardButton(text="Курс EASY 15",
                                     url="https://tvorimtelom.ru/easy15")
ENTER_BUTTONS = InlineKeyboardMarkup()
project_button = InlineKeyboardButton(text="🧘🏻‍♀️ Easy Morning", callback_data="enter_project")
course_button = InlineKeyboardButton(text="Курс Easy 15", callback_data="enter_course")
individual_exc = InlineKeyboardButton(text="Индивидуальные занятия", callback_data="enter_ind-exc")
ENTER_BUTTONS.add(project_button).add(course_button).add(individual_exc)


BACK_PAY_BUTTON = InlineKeyboardMarkup()
back_pay_button = InlineKeyboardButton(text="Назад", callback_data="back_pay")
BACK_PAY_BUTTON.add(back_pay_button)

BACK_EXAMPLE = InlineKeyboardMarkup()
back_example = InlineKeyboardButton(text="Назад", callback_data="back_pay-1")
BACK_EXAMPLE.add(back_example)

back = InlineKeyboardButton(text="Назад", callback_data="back")
START_BUTTONS = InlineKeyboardMarkup()
subscription = InlineKeyboardButton(text="Покупка доступа к чату", callback_data="menu_subscription")
other = InlineKeyboardButton(text="Другое", callback_data="pay_other")
link = InlineKeyboardButton(text="🎁  попробуй", url=LINK)
START_BUTTONS.add(subscription).add(other).add(link)

SUBSCRIPTION_BUTTONS = InlineKeyboardMarkup()
seven_days = InlineKeyboardButton(text="7 дней", callback_data="pay_7")
fourteen_days = InlineKeyboardButton(text="14 дней", callback_data="pay_14")
month = InlineKeyboardButton(text="1 месяц", callback_data="pay_30")
vip_access = InlineKeyboardButton(text="🔥 PRO", callback_data="pay_vip")
example = InlineKeyboardButton(text="Отзывы", callback_data = "pay_example")
SUBSCRIPTION_BUTTONS.add(seven_days, fourteen_days, month).add(vip_access).add(example).add(link).add(course_button).add(individual_exc).add(back)

LINK_MENU_BUTTONS = InlineKeyboardMarkup()
link_url = InlineKeyboardButton(text="Перейти в чат", url=LINK)
LINK_MENU_BUTTONS.add(link_url).add(back)


OTHER_BUTTONS = InlineKeyboardMarkup()

other_individual_exc = InlineKeyboardButton(text="Купить индивидуальные занятия", url="https://tvorimtelom.ru/go")
other_contact = InlineKeyboardButton(text="Связаться со мной", url = "https://t.me/valeri_zhara")
OTHER_BUTTONS.add(other_easy_15).add(other_individual_exc).add(other_contact).add(back)

BACK_BUTTON = InlineKeyboardMarkup()
BACK_BUTTON.add(back)



CONTACT_BUTTONS = InlineKeyboardMarkup()
CONTACT_BUTTONS.add(other_contact).add(course_button).add(project_button).add(back)



EASY_15 = InlineKeyboardMarkup()
EASY_15.add(other_easy_15).add(individual_exc).add(project_button).add(back)
"Admin"

ADMIN_PAY = InlineKeyboardMarkup()
pay_accept = InlineKeyboardButton(text="Принять", callback_data="admin-pay_accept")
pay_decline = InlineKeyboardButton(text="Отказать", callback_data="admin-pay_decline")
ADMIN_PAY.add(pay_accept, pay_decline)

ADMIN = InlineKeyboardMarkup()
check_vip = InlineKeyboardButton(text="Посмотреть список PRO-пользователей", callback_data="admin_vip")
ADMIN.add(check_vip)