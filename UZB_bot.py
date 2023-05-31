import telebot
import bot_bd
import buttonsbot
import config
from main import str_msg
from datetime import datetime
from pytz import timezone


token = ('5827149235:AAEpIzi0vS1YK781Cv9tW7HsEzwyhFaF2VE')
#Подключения бота
bot = telebot.TeleBot('5827149235:AAEpIzi0vS1YK781Cv9tW7HsEzwyhFaF2VE', skip_pending=True)

chanel_id = -1001833445663


@bot.message_handler(chat_types=['text'])
def str_msg1(message):
    user_id = message.from_user.id
    if message.text == '💵Пополнить счет':
        admin_id = 1819193668
        photo = bot_bd.view_system(admin_id, 'xid')
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_photo(user_id, photo[2], '💵* Введите свой 1XBET UZS ID *:', reply_markup=a, parse_mode='Markdown')
        bot.register_next_step_handler(message, get_id_pay)

    elif message.text == '📤Снять деньги':
        admin_id = 1819193668
        photo = bot_bd.view_system(admin_id, 'withdraw')
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_photo(user_id, photo[2], '*Наличные > Город: Нукус (Каракалпакстан) > Улица: Вечный огонь (24/7)*'
                       , reply_markup=a, parse_mode='Markdown')
        bot.send_message(user_id, '💵* Введите свой 1XBET UZS ID *:', parse_mode='Markdown')
        bot.register_next_step_handler(message, get_sum_withdraw)

    elif message.text == '☎️ Тех.поддержка':
        bot.send_message(user_id, '*Если возникли вопросы, или проблемы с использованием бота *👇',
                             reply_markup=buttonsbot.th_support(), parse_mode='Markdown')
        bot.send_message(user_id, '*Выберите нужный раздел *', reply_markup=buttonsbot.menu_button(),
                         parse_mode='Markdown')
        bot.register_next_step_handler(message, str_msg)

    elif message.text == '/admin':
        bot.register_next_step_handler(message, main.start_admin)

    elif message.text == '/start':
        bot.send_message(user_id, 'Еше раз /start')
        bot.register_next_step_handler(message, main.start_message)

    else:
        bot.send_message(user_id, 'Воспользуйтесь кнопкой')
        bot.register_next_step_handler(message, str_msg)

def bot_stop(message):
    user_id = message.from_user.id
    bot.send_message(user_id, config.bot_stop, parse_mode='Markdown')
    bot.register_next_step_handler(message, main.start_message)

def get_sum_withdraw(message):
    user_id = message.from_user.id
    if message.text:
        id_for_pay = message.text
        bot.send_message(user_id, '*Укажите сумму, которую вы хотите вывести* :',
                         reply_markup=buttonsbot.return_pay(), parse_mode='Markdown')
        bot.register_next_step_handler(message, get_id_withdraw, id_for_pay)

    elif message.text == 'Отменить ❌':
        bot.send_message(user_id, 'Снятие денег отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Не корректное ID')
        bot.register_next_step_handler(message, get_sum_withdraw)

def get_id_withdraw(message, id_for_pay):
    user_id = message.from_user.id
    if message.text:
        sum_for_pay = message.text
        admin_id = 1819193668
        photo = bot_bd.view_system(admin_id, 'withdraw_pass')
        bot.send_photo(user_id, photo[2], '*Пришлите код который вам выдал 1XBET*', parse_mode='Markdown')
        bot.register_next_step_handler(message, get_password_withdraw, id_for_pay, sum_for_pay)

    elif message.text == 'Отменить ❌':
        bot.send_message(user_id, 'Снятие денег отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Не корректная сумма')
        bot.register_next_step_handler(message, get_id_withdraw, id_for_pay)

def get_password_withdraw(message, id_for_pay, sum_for_pay):
    user_id = message.from_user.id
    if message.text:
        password = message.text
        bot.send_message(user_id, '*💳 Введите номер пластиковый карты :*', parse_mode='Markdown')
        bot.register_next_step_handler(message, fin_withdraw, id_for_pay, password, sum_for_pay)

    elif message.text == 'Отменить ❌':
        bot.send_message(user_id, 'Снятие денег отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Не корректно введен код')
        bot.register_next_step_handler(message, get_password_withdraw, id_for_pay, sum_for_pay)


def fin_withdraw(message, id_for_pay, password, sum_for_pay):
    user_id = message.from_user.id
    if message.text:
        card_number = message.text
        bot_bd.delete_sum_temporary(user_id)
        bot_bd.add_sum(user_id, sum_for_pay)
        bot_bd.add_sum_temporary(user_id, sum_for_pay)
        sum = bot_bd.view_withdraw_sum(user_id)
        bot_bd.add_withdraw(user_id, id_for_pay, password, card_number)
        bot_bd.delete_withdraw(user_id)
        bot_bd.add_withdraw_temporary(user_id, id_for_pay, password, card_number)
        bot.send_message(user_id, f'⏳*Ожидайте, ваша заявка находится на проверке*\n\n'
                                  f'*Ваша заявка под уникальным номером {user_id}*\n\n*'
                                  f'Если ваши средства не поступили в течении 24 часов, обратитесь в службу поддержки*️'
                         , reply_markup=buttonsbot.menu_button(), parse_mode='Markdown')
        chanel_id1 = -1001672272729
        dt_format = "%d-%m-%Y %H:%M:%S"
        a = datetime.now(timezone('Asia/Tashkent'))
        user_nik = message.from_user.first_name
        bot.send_message(chanel_id1, f'Ник : {user_nik}\nУникальный номер: {user_id}\nВремя : {a.strftime(dt_format)}')
        bot.send_message(user_id, '*Если возникли вопросы, или проблемы с использованием бота *👇',
                         reply_markup=buttonsbot.th_support(), parse_mode='Markdown')
        msg = bot_bd.view_withdraw(user_id)
        bot.send_message(chanel_id, f'Запрос на вывод средств:\n\nTelegram : {msg[0]}\n\n1xBet ID: `{msg[1]}`\n'
                                    f'Pay Amount : `{sum[-1]}`\nCod: `{msg[2]}`\nCard number: `{msg[3]}`\nTime : {a.strftime(dt_format)}', parse_mode='Markdown')
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Не корректна введена карта')
        bot.register_next_step_handler(message, fin_withdraw, id_for_pay, password, sum_for_pay)

def get_id_pay(message):
    user_id = message.from_user.id
    user_id_pay = message.text
    v = str(user_id_pay)
    if 8 <= len(v) <= 9:
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(user_id, config.pay_min, reply_markup=a, parse_mode='Markdown')
        bot.register_next_step_handler(message, get_payment_sum, user_id_pay)

    elif message.text == 'Отменить ❌':
        bot.send_message(user_id, 'Снятие денег отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Некорректное ID')
        bot.register_next_step_handler(message, get_id_pay)

def get_payment_sum(message, user_id_pay):
    user_id = message.from_user.id
    sum = message.text
    b = user_id_pay
    try:
        n = int(sum)
        if 10000 <= n <= 50000000:
            bot_bd.add_payment(user_id, user_id_pay, sum)
            bot.send_message(user_id, config.pay_info, parse_mode='Markdown',
                                 reply_markup=buttonsbot.ret_and_accept())
            bot.register_next_step_handler(message, get_check, user_id_pay, sum)

        elif message.text == 'Отменить ❌':
            bot.send_message(user_id, 'Снятие денег отменена', reply_markup=buttonsbot.menu_button())
            bot.register_next_step_handler(message, str_msg)

        else:
            bot.send_message(user_id, 'Введено некорректная сумма')
            bot.register_next_step_handler(message, get_payment_sum, user_id_pay)

    except ValueError:
        bot.send_message(user_id, 'Не корректная сумма')
        bot.register_next_step_handler(message, get_payment_sum, user_id_pay)

def get_check(message, user_id_pay, user_sum):
    user_id = message.from_user.id
    if message.text == 'Подтвердить✅':
        bot.send_message(user_id, '*Отпрате Чек [Скриншот или фото]*', reply_markup=buttonsbot.return_pay(), parse_mode='Markdown')
        bot.register_next_step_handler(message, get_payment_finish, user_sum, user_id_pay)

    elif message.text == 'Отменить ❌':
        bot.send_message(user_id, 'Покупка отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Вы прислали не фото или неизвестную команду\nНажмите кнопку поддтвердить'
                                  ' или отменить'
                                  , reply_markup=buttonsbot.ret_and_accept())
        bot.register_next_step_handler(message, get_check, user_id_pay, user_sum)


def get_payment_finish(message, user_sum, user_id_pay):
    user_id = message.from_user.id
    user_check = message.photo

    if user_check:

        bot.send_message(user_id, f'⏳*Ожидайте, ваша заявка находится на проверке*',
                         reply_markup=buttonsbot.menu_button(), parse_mode='Markdown')
        bot.send_message(user_id, f'*Ваша заявка под уникальным номером {user_id}\n\nЕсли ваши средства не поступили в течении 10 минут,*'
                                  '*обратитесь в службу поддержки*'
                                  , reply_markup=buttonsbot.th_support(), parse_mode='Markdown')
        chanel_id1 = -1001672272729
        dt_format = "%d-%m-%Y %H:%M:%S"
        a = datetime.now(timezone('Asia/Tashkent'))
        user_nik = message.from_user.first_name
        bot.send_message(chanel_id1, f'Ник : {user_nik}\nУникальный номер: {user_id}\nВремя : {a.strftime(dt_format)}')
        bot_bd.add_payment(user_id, user_id_pay, user_sum)
        bot_bd.add_check(user_id, user_check[-1].file_id)
        bot_bd.delete_upd(user_id)
        bot_bd.add_temporary(user_id, user_id_pay, user_sum, user_check[-1].file_id)
        msg = bot_bd.view_check(user_id)
        bot.send_photo(-1001833445663, msg[3], f'Telegram: {msg[0]}\n\n'
                                               f'1xBet ID: `{msg[1]}`\nPay Amount: `{msg[2]}`\nTime : {a.strftime(dt_format)}'
                       , parse_mode='Markdown')
        bot.register_next_step_handler(message, str_msg)

    elif message.text == 'Отменить ❌':
        bot.send_message(user_id, 'Покупка отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Вы прислали не фото или неизвестную команду', reply_markup=buttonsbot.return_pay())
        bot.register_next_step_handler(message, get_check)


