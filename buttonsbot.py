from telebot import types


def get_number():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Отправить контакт', request_contact=True)
    kb.add(button)
    return kb


def menu_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('💵Пополнить счет')
    button1 = types.KeyboardButton('📤Снять деньги')
    button2 = types.KeyboardButton('☎️ Тех.поддержка')
    button3 = types.KeyboardButton('Выбрать язык 🇷🇺 🇺🇿')
    kb.add(button, button1, button2, button3, row_width=2)
    return kb


def return_pay():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Отменить 🚫')
    kb.add(button)
    return kb


def ret_and_accept():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Оплатил ✅')
    button2 = types.KeyboardButton('Отменить 🚫')
    kb.add(button1, button2, row_width=1)
    return kb


def th_support():
    kb1 = types.InlineKeyboardMarkup()
    button12 = types.InlineKeyboardButton('Support', url='https://t.me/FlamePaySupport')
    # button = types.InlineKeyboardButton('Отследить заявку', url='https://t.me/FlamePayRequest')
    kb1.add(button12)
    return kb1


def bot_unsuported():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('технические неполадки⛔️')
    kb.add(button)
    return kb


def admin_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Добавить фото')
    button1 = types.KeyboardButton('Удалить фото')
    button2 = types.KeyboardButton('Разблокировка')
    button3 = types.KeyboardButton('Блокировка')
    button4 = types.KeyboardButton('Пользователь')
    button5 = types.KeyboardButton('Рассылка')
    button6 = types.KeyboardButton('Удалить USER')
    button7 = types.KeyboardButton('Проверка')
    button8 = types.KeyboardButton('Счет кассы')
    kb.add(button, button1, button2, button3, button4, button5, button6, button7, button8, row_width=2)
    return kb


def type_all():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Фото/Текст')
    button1 = types.KeyboardButton('Файл/Текст')
    button2 = types.KeyboardButton('В меню')
    kb.add(button, button1, button2, row_width=2)
    return kb


def set_language():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('🇷🇺Руский')
    button1 = types.KeyboardButton('🇺🇿Uzbek tili')
    kb.add(button, button1, row_width=2)
    return kb


###############################
#UZB
def menu_button_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('💵Hisobni toldirish')
    button1 = types.KeyboardButton('📤Pulni yechib olish')
    button2 = types.KeyboardButton('☎️ Texnik yordam')
    button3 = types.KeyboardButton('Tilni tanglash 🇷🇺 🇺🇿')
    kb.add(button, button1, button2, button3, row_width=2)
    return kb


def return_pay_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Bekor qilish 🚫')
    kb.add(button)
    return kb


def ret_and_accept_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('bekor qilish ❌')
    button1 = types.KeyboardButton('Tasdiqlang✅')
    kb.add(button1, button, row_width=1)
    return kb


def th_support_uz():
    kb1 = types.InlineKeyboardMarkup()
    button12 = types.InlineKeyboardButton('Support', url='https://t.me/FlamePaySupport')
    button = types.InlineKeyboardButton('Ilovani kuzatib boring', url='https://t.me/FlamePayRequest')
    kb1.add(button, button12)
    return kb1


def bot_unsuported_uz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('texnik qiyinchiliklar⛔️')
    kb.add(button)
    return kb


def support_unsucceful():
    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Support', url='https://t.me/FlamePaySupport')
    kb.add(button)
    return kb


def accept_with():
    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Подтвердить', callback_data='accepted')
    kb.add(button)
    return kb


def get_contact():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(button)
    return kb
