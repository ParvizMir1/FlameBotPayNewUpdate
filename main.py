import time

import telebot
import bot_bd
import buttonsbot
import config
import requests
from threading import Thread
from datetime import datetime
from pytz import timezone
import json


token = '6061662953:AAFLdR-ihJY8seooDIjIzuHZU8InAEVoUbk'
# Подключения бота
bot = telebot.TeleBot('6061662953:AAFLdR-ihJY8seooDIjIzuHZU8InAEVoUbk', skip_pending=True)
chanel_id = -1001833445663


# Запуск админ панель
@bot.message_handler(commands=['admin'])
def start_admin(message):
    user_id = message.from_user.id
    admin_id = 1819193668
    admin_id1 = 5225418097
    if admin_id == user_id:
        bot.send_message(user_id, 'Добро пожаловать Админ', reply_markup=buttonsbot.admin_menu())
        bot.register_next_step_handler(message, admin_commands)

    elif admin_id1 == user_id:
        bot.send_message(user_id, 'Добро пожаловать Админ', reply_markup=buttonsbot.admin_menu())
        bot.register_next_step_handler(message, admin_commands)

    else:
        bot.send_message(user_id, 'Ошибка')


def admin_commands(message):
    user_id = message.from_user.id
    if message.text == 'Добавить фото':
        bot.send_message(user_id, 'Отправте название только доступных из списка :\n\n[`xid` = ID 1xbet инструкция]\n'
                                  '[`withdraw` = это инструкция вывода выбор города]\n'
                                  '[`withdraw_pass` = это инструкция вывода по вписанию кода]', parse_mode='Markdown')
        bot.register_next_step_handler(message, get_photo_name)

    elif message.text == 'Удалить фото':
        bot.send_message(user_id, 'Отправте название')
        bot.register_next_step_handler(message, delete_photo)

    elif message.text == 'Разблокировка':
        bot_bd.add_admin_id(user_id)
        bot.send_message(user_id, 'Бот разблокирован')
        bot.register_next_step_handler(message, admin_commands)

    elif message.text == 'Блокировка':
        all_user = bot_bd.check_user_rass()

        for i in all_user:
            bot.send_message(i[0],
                             'Бот временно отключен все действия будут отменены\nОбязательно введите команду /start')
            break
        bot_bd.unblock_admin(user_id)
        bot.send_message(user_id, 'Бот заблокирован')
        bot.register_next_step_handler(message, admin_commands)

    elif message.text == 'Пользователь':
        bot.send_message(user_id, 'Вы вошли как пользователь', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    elif message.text == 'Рассылка':
        bot.send_message(user_id, 'Выберите тип', reply_markup=buttonsbot.type_all())
        bot.register_next_step_handler(message, set_type)

    elif message.text == 'Проверка':
        thwt = Thread(target=proverka, args=(message,))
        thwt.start()
        bot.register_next_step_handler(message, admin_commands)

    elif message.text == 'Удалить USER':
        bot.send_message(user_id, 'Отправте id')
        bot.register_next_step_handler(message, delete_user)

    elif message.text == 'Счет кассы':
        request = requests.post('http://ck83858.tw1.ru/api/balans.php').text
        bot.send_message(user_id, f'{request} UZS')
        bot.register_next_step_handler(message, admin_commands)

    elif message.text == 'Запрос':
        bot.send_message(user_id, 'Отправте ID')
        bot.register_next_step_handler(message, get_id_for_check)

    else:
        bot.send_message(user_id, 'Используйте кнопки')
        bot.register_next_step_handler(message, admin_commands)


def get_id_for_check(message):
    user_id = message.from_user.id
    id = message.text
    check = bot_bd.view_checks(id)
    dt_format = "%d-%m-%Y %H:%M:%S"
    a = datetime.now(timezone('Asia/Tashkent'))
    chanel_id12 = -1001913028408
    bot.send_message(id, f'🆔 {id}\n⬆Выплата: {check[1]} UZS\n⬇Получения: {check[1]} UZS\n💳CARD UZS: {check[2]}\n'
                         f'📅Дата: {a.strftime(dt_format)}\n📝Статус: Успешно прошло✅', parse_mode='MarkDown')
    bot.send_message(chanel_id12, f'Запрос на вывод средств:\n\nTelegram : {user_id}\n\n1xBet ID: {check[3]}\n'
                                    f'Pay Amount : `{check[1]}`\nCard number: `{check[2]}`\nTime :'
                                  f' {a.strftime(dt_format)}\nСтатус: Успешно прошло✅', parse_mode='MarkDown')
    bot.send_message(user_id, 'Успешно')
    bot.register_next_step_handler(message, admin_commands)


def proverka(message):
    ADM_ID = 1819193668
    all_user = bot_bd.check_user_rass()
    for i in all_user:
        try:
            r = requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                              data={'chat_id': i[0], 'text': 'Желаем вам прибыльных ставок 🍀'})
            if r.status_code == 200:
                pass
            else:
                requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                              data={'chat_id': ADM_ID,
                                    'text': 'Ошибка отправки' + '\n' + 'id: ' + str(i[0]) + '\n' + str(
                                        r.json()['description'])})
        except Exception as error:
            requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                          data={'chat_id': ADM_ID, 'text': 'Exception отправки' + '\n' + str(error)})


def delete_user(message):
    user_id = message.from_user.id
    id = message.text
    bot_bd.delete_user(id)
    bot.send_message(user_id, 'Успешно удалено', reply_markup=buttonsbot.admin_menu())
    bot.register_next_step_handler(message, admin_commands)


def set_type(message):
    user_id = message.from_user.id
    if message.text == 'Файл/Текст':
        bot.send_message(user_id, 'Отправте текст который хотите опубликовать')
        bot.register_next_step_handler(message, recursiy1)

    elif message.text == 'Фото/Текст':
        bot.send_message(user_id, 'Отправте текст который хотите опубликовать')
        bot.register_next_step_handler(message, get_photo_1)

    else:
        bot.send_message(user_id, 'Вернулись', reply_markup=buttonsbot.admin_menu())
        bot.register_next_step_handler(message, admin_commands)


def get_photo_1(message):
    user_id = message.from_user.id
    text_op1 = message.text
    bot.send_message(user_id, 'Отправте фото который хотите опубликовать', reply_markup=buttonsbot.admin_menu())
    bot.register_next_step_handler(message, get_photo_3, text_op1)


def get_photo_2(message, text1, text_op1):
    user_id = message.from_user.id
    bot_bd.delete_photo(user_id)
    bot_bd.add_photo_text(user_id, text_op1, text1)
    msg = bot_bd.view_photo_text(user_id)
    all_user = bot_bd.check_user_rass()
    print(all_user)
    try:
        for i in all_user:
            print(i)
            bot.send_photo(i[0], msg[-1], msg[1])
            continue
    except:
        bot.send_message(user_id, 'Не удалось отправить удалите заблокированного пользователя')


def get_photo_3(message, text_op1):
    text1 = message.photo[-1].file_id
    try:
        thw = Thread(target=get_photo_2, args=(message, text1, text_op1))
        thw.start()
        bot.register_next_step_handler(message, admin_commands)
    except:
        bot.send_message(message.from_user.id, 'Не удалось отправить удалите заблокированного пользователя')
        bot.register_next_step_handler(message, admin_commands)


def recursiy1(message):
    user_id = message.from_user.id
    text_op = message.text
    bot.send_message(user_id, 'Отправте файл который хотите опубликовать', reply_markup=buttonsbot.admin_menu())
    bot.register_next_step_handler(message, th1, text_op)


def recursiy(message, text, text_op):
    user_id = message.from_user.id
    bot_bd.delete_document(user_id)
    bot_bd.add_document_text(user_id, text_op, text)
    msg = bot_bd.view_document_text(user_id)
    all_user = bot_bd.check_user_rass()
    print(all_user)
    try:
        for i in all_user:
            print(i)
            bot.send_document(i[0], msg[-1], msg[1])
    except:
        bot.send_message(user_id, 'Не удалось отправить удалите заблокированного пользователя')


def th1(message, text_op):
    text = message.document.file_id
    try:
        th = Thread(target=recursiy, args=(message, text, text_op))
        th.start()
        bot.register_next_step_handler(message, admin_commands)
    except:
        bot.send_message(message.from_user.id, 'Не удалось отправить удалите заблокированного пользователя')
        bot.register_next_step_handler(message, admin_commands)


# Удаление фото
def delete_photo(message):
    user_id = message.from_user.id
    photo_name = message.text
    bot_bd.delete_system(photo_name)
    bot.send_message(user_id, 'Успешно удалено')
    bot.register_next_step_handler(message, admin_commands)


# Добавление фото в бд
def get_photo_name(message):
    user_id = message.from_user.id
    photo_name = message.text
    bot.send_message(user_id, 'Отправте фото')
    bot.register_next_step_handler(message, get_photo, photo_name)


def get_photo(message, photo_name):
    user_id = message.from_user.id
    photo = message.photo
    if message.photo:
        bot_bd.add_for_system(user_id, photo_name, photo[-1].file_id)
        bot.send_message(user_id, f'Успешно добавлено\nВы добавили : {photo_name}')
        bot.register_next_step_handler(message, admin_commands)

    else:
        bot.send_message(user_id, 'Это не фото')
        bot.register_next_step_handler(message, get_photo)
#################################


# Запуск бота
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    checker = bot_bd.check_user(user_id)
    admin_id = 5225418097
    adm_id = 1819193668
    checker1 = bot_bd.check_id_admin(admin_id)
    print(checker)
    if checker1 == True:
        if checker:
            bot.send_message(user_id, text=f'*FlamePayBot* - _пополняем UZS счет 1XBET\n\nДля_ '
                                           f'_взаимодействия с ботом выберите нужный раздел 👇_', parse_mode='Markdown',
                             reply_markup=buttonsbot.menu_button())
            bot.register_next_step_handler(message, str_msg)

        elif message.text == '/admin':
            bot.register_next_step_handler(message, start_admin)

        else:
            bot_bd.add_user(user_id)
            print(1)
            bot.send_message(user_id, text=f'*FlamePayBot* - _пополняем UZS счет 1XBET\n\nДля_ '
                                      f'_взаимодействия с ботом отправте номер телефона_\n', parse_mode='Markdown',
                             reply_markup=buttonsbot.get_contact())
            bot.register_next_step_handler(message, get_contact)

    elif message.text == '/start':
        bot.send_message(user_id, 'Бот перезапушен введите /start')
        bot.register_next_step_handler(message, start_message)

    elif message.text == '/admin':
        bot.register_next_step_handler(message, start_admin)

    else:
        bot.send_message(user_id, 'Бот временно отключен', reply_markup=buttonsbot.bot_unsuported())
        bot.register_next_step_handler(message, bot_stop)


def get_contact(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f'*FlamePayBot* - _пополняем UZS счет 1XBET\n\nДля_'
                              f'\n_взаимодействия с ботом выберите нужный раздел 👇_',
                     reply_markup=buttonsbot.menu_button(), parse_mode='MarkDown')
    number = message.contact.phone_number
    bot_bd.add_number(user_id, number)
    bot.register_next_step_handler(message, str_msg)


def select_language(message):
    user_id = message.from_user.id
    if message.text == '🇷🇺Руский':
        bot.send_message(user_id, 'Выбран русский', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    elif message.text == '🇺🇿Uzbek tili':
        bot.send_message(user_id, 'Ozbek tili tanlandi', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)

    else:
        bot.send_message(user_id, 'Не известная команда')
        bot.register_next_step_handler(message, select_language)


@bot.message_handler(chat_types=['text'])
def str_msg(message):
    user_id = message.from_user.id
    if message.text == '💵Пополнить счет':
        admin_id = 1819193668
        photo = bot_bd.view_system(admin_id, 'xid')
        chat = bot.send_photo(user_id, photo[2], '💵* Введите свой 1XBET UZS ID *:',
                              reply_markup=buttonsbot.return_pay(), parse_mode='Markdown')
        bot.register_next_step_handler(message, get_id_pay, chat)

    elif message.text == '📤Снять деньги':
            admin_id = 1819193668
            photo = bot_bd.view_system(admin_id, 'withdraw')
            chat = bot.send_photo(user_id, photo[2], '*Адрес кассы* :\n*Город: Нукус (Каракалпакстан)*\n'
                                                     '*Улица: Вечный огонь (24/7)*',
                                  reply_markup=buttonsbot.return_pay(), parse_mode='Markdown')
            chat1 = bot.send_message(user_id, '💵* Введите свой 1XBET UZS ID *:', parse_mode='Markdown')
            bot.register_next_step_handler(message, get_sum_withdraw, chat, chat1)

    elif message.text == 'Выбрать язык 🇷🇺 🇺🇿':
        user_id = message.from_user.id
        bot.send_message(user_id, 'Выберите нужный для вас язык', reply_markup=buttonsbot.set_language())
        bot.register_next_step_handler(message, select_language)

    elif message.text == '☎️ Тех.поддержка':
        bot.send_message(user_id, '*Если возникли вопросы, или проблемы с использованием бота:* @FlamePaySupport',
                         reply_markup=buttonsbot.menu_button(), parse_mode='Markdown')
        bot.register_next_step_handler(message, str_msg)

    elif message.text == '/admin':
        bot.register_next_step_handler(message, start_admin)

    elif message.text == '/start':
        bot.send_message(user_id, 'Еше раз /start')
        bot.register_next_step_handler(message, start_message)

    elif message.text == '/xbet':
        bot.register_next_step_handler(message, xbet)

    elif message.text == '/uz':
        bot.send_message(user_id, 'Uzbek tili tanlandi', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)

    else:
        bot.send_message(user_id, 'Воспользуйтесь кнопкой')
        bot.register_next_step_handler(message, str_msg)


def bot_stop(message):
    user_id = message.from_user.id
    bot.send_message(user_id, config.bot_stop, parse_mode='Markdown')
    bot.register_next_step_handler(message, start_message)


def get_sum_withdraw(message, chat, chat1):
    user_id = message.from_user.id
    if message.text:
        id_for_pay = message.text
        bot.delete_message(user_id, chat.message_id)
        bot.delete_message(user_id, chat1.message_id)
        bot.delete_message(user_id, message.message_id)
        try:
            select = requests.post(f'http://ck83858.tw1.ru/api/without.php?user_id={id_for_pay}').text
            select = json.loads(select)
            print(select)
            select_data = select['Data'][0][3]
            print(select)
            sum = select['Data'][0][5]
            print(sum)
            if message.text:
                if select_data == 'Операция выполнена успешно':
                    id = 1819193668
                    photo = bot_bd.view_system(id, 'withdraw_pass')
                    chat = bot.send_photo(user_id, photo[2], '*Укажите карту UZCARD или HUMO*',
                                   reply_markup=buttonsbot.return_pay(), parse_mode='Markdown')
                    bot.register_next_step_handler(message, fin_withdraw, id_for_pay, sum, chat)

                elif select_data == 'Запрос на выплату не подтвержден, находится на рассмотрении':
                    bot.send_message(user_id, 'Запрос на выплату не подтвержден, находится на рассмотрении',
                                     reply_markup=buttonsbot.menu_button())
                    bot.register_next_step_handler(message, str_msg)

                elif select_data == 'Валюта пользователя отличается от валюты кассы. Операция невозможна':
                    bot.send_message(user_id, 'Валюта пользователя отличается от валюты кассы. Операция невозможна')
                    bot.register_next_step_handler(message, str_msg)

                else:
                    bot.send_message(user_id, 'Ошибка, мы не нашли вашу заявку на вывод средств !',
                                     reply_markup=buttonsbot.menu_button())
                    bot.register_next_step_handler(message, str_msg)

            elif message.text == 'Отменить 🚫':
                bot.send_message(user_id, 'Снятие денег отменена', reply_markup=buttonsbot.menu_button())
                bot.register_next_step_handler(message, str_msg)

            else:
                bot.send_message(user_id, 'Не корректное ID')
                bot.register_next_step_handler(message, get_sum_withdraw, chat, chat1)

        except:
            bot.send_message(user_id, '*Операция отменена*', reply_markup=buttonsbot.menu_button(),
                             parse_mode='MarkDown')
            bot.register_next_step_handler(message, str_msg)

    elif message.text == 'Отменить 🚫':
        bot.send_message(user_id, 'Операция отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Операция отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)


def fin_withdraw(message, id_for_pay, sum, chat):
    user_id = message.from_user.id
    card = message.text
    bot.delete_message(user_id, chat.message_id)
    dt_format = "%d-%m-%Y %H:%M:%S"
    a = datetime.now(timezone('Asia/Tashkent'))
    number = bot_bd.view_number(user_id)
    if message.text:
            bot.send_message(user_id, f'🆔 {user_id}\nNumber: {number[1]}\n⬆Выплата: {sum} UZS\n⬇Получения: {sum} UZS'
                                      f'\n💳CARD UZS: {card}\n📅Дата: {a.strftime(dt_format)}\n📝Статус: Ожидайте⏳',
                             reply_markup=buttonsbot.menu_button(), parse_mode='Markdown')
            chanel_id12 = -1001913028408
            bot.send_message(chanel_id12, f'Запрос на вывод средств:\n\nTelegram : {user_id}\n\n1xBet ID:'
                                          f' {id_for_pay}\n'
                                        f'Pay Amount : `{sum}`\nCard number: `{card}`\nTime : {a.strftime(dt_format)}'
                                          f'\nСтатус: В ожидании⏳',
                             parse_mode='Markdown')
            bot_bd.delete_check(user_id)
            print(card)
            bot_bd.save_check(user_id, sum, card, id_for_pay)
            bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Не корректна введена карта')
        bot.register_next_step_handler(message, fin_withdraw, id_for_pay)


def get_id_pay(message, chat):
    user_id = message.from_user.id
    bot.delete_message(user_id, chat.message_id)
    bot.delete_message(user_id, message.message_id)
    user_id_pay = message.text
    v = str(user_id_pay)
    if 8 <= len(v) <= 9:
        result = requests.get(f'http://ck83858.tw1.ru/api/check.php?user_id={user_id_pay}').text
        result = json.loads(result)
        for i in result['Data']:
            chat = bot.send_message(user_id, f'*🆔Account ID: *`{i[0]}`\n👤*Ф.И.О*: {i[2]} {i[3]} {i[4]}\n💰Баланс*:'
                                             f' {i[15]}*', parse_mode='Markdown')
            chat1 = bot.send_message(user_id, config.pay_min, parse_mode='Markdown', reply_markup=buttonsbot.return_pay())
            bot.register_next_step_handler(message, get_payment_sum, user_id_pay, chat, chat1)

    elif message.text == 'Отменить 🚫':
        bot.send_message(user_id, 'Операция отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    elif message.photo:
        bot.send_message(user_id, 'Нельзя отправить фото', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        bot.send_message(user_id, 'Некорректное ID', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)


def get_payment_sum(message, user_id_pay, chat, chat1):
    user_id = message.from_user.id
    if message.text == 'Отменить 🚫':
        bot.send_message(user_id, 'Операция отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        try:
            sum = message.text
            n = int(sum)
            if 1000 <= n <= 50000000:
                bot.delete_message(user_id, chat.message_id)
                bot.delete_message(user_id, chat1.message_id)
                bot.delete_message(user_id, message.message_id)
                headers = {
                    'device': '6Fk1rB',
                    'user-agent': 'Mozilla/57.36'
                }
                sum1 = int(sum) * 100

                data = {
                    "method": "p2p.create",
                    "params": {
                        "card_id": '6374d26a65f23ea1d3c687f2',
                        "amount": sum1,
                        "description": 'Спасибо'
                    }
                }

                response = requests.post('https://payme.uz/api/p2p.create', headers=headers, json=data)
                res = response.json()
                print(res)

                csv = {
                    '_id': res['result']['cheque']['_id'],
                    '_url': 'https://checkout.paycom.uz',
                    '_pay_amount': str(sum) + ' UZS',
                    '_pay_url': 'https://checkout.paycom.uz/' + str(res['result']['cheque']['_id'])
                }

                ec = {
                    '_details': csv
                }

                ec2 = {
                    '_result': ec
                }

                print(json.dumps(csv, indent=4))
                link = csv['_pay_url']
                id = csv['_id']
                try:
                    result = requests.get(f'http://ck83858.tw1.ru/api/check.php?user_id={user_id_pay}').text
                    result = json.loads(result)
                    # bot_bd.add_payment(user_id, user_id_pay, sum)
                    for i in result["Data"]:
                        kbi = telebot.types.InlineKeyboardMarkup()
                        button = telebot.types.InlineKeyboardButton('💸 Оплатить', url=link)
                        kbi.add(button)
                        name = (i[2])
                        name1 = (i[3])
                        name2 = (i[4])
                        balance = (i[15])
                        text_info = f'*🆔Account ID*: `{i[0]}`\n*👤Ф.И.О*: *{i[2]} {i[3]} {i[4]}*\n*💰Баланс*:' \
                                    f' *{i[15]}*\n===============\n💵*Сумма: {sum} UZS' \
                                    f'\n💸Услуга: 0 UZS\n💰К оплате: {sum} UZS*'
                        chat = bot.send_message(user_id, text_info, parse_mode='Markdown', reply_markup=kbi)
                        chat1 = bot.send_message(user_id,
                                         f'1️⃣ Для оплаты: Вам необходимо перевести {sum} сумов на наш счет,'
                                         f' нажав кнопку ниже *( 💸 Оплатить )* в приложении PayMe!\n\n2️⃣ В течение'
                                         f' 10 минут после оплаты необходимо нажать кнопку *( Оплатил ✅ )*',
                                         reply_markup=buttonsbot.ret_and_accept(), parse_mode='MarkDown')
                        bot.register_next_step_handler(message, check_payme, id, sum, user_id_pay, chat, name, name1, name2, balance, chat1)

                except ValueError:
                    bot.send_message(user_id, 'Не корректная сумма', reply_markup=buttonsbot.menu_button())
                    bot.register_next_step_handler(message, str_msg)

            else:
                bot.send_message(user_id, 'Не корректная сумма', reply_markup=buttonsbot.menu_button())
                bot.register_next_step_handler(message, str_msg)

        except ValueError:
            bot.send_message(user_id, 'Не корректная сумма', reply_markup=buttonsbot.menu_button())
            bot.register_next_step_handler(message, str_msg)


def check_payme(message, id, sum, user_id_pay, chat, name, name1, name2, balance, chat1):
    user_id = message.from_user.id
    headers = {
        'device': '6Fk1rB',
        'user-agent': 'Mozilla/57.36'
    }

    transaction_id = id

    data = {
        "method": "cheque.get",
        "params": {
            "id": transaction_id
        }
    }

    response = requests.post('https://payme.uz/api/cheque.get', headers=headers, json=data)
    res = response.json()
    info_succ = res['result']['cheque']['meta']['has_invoice']

    if info_succ == True:
        bot.delete_message(user_id, chat.message_id)
        bot.delete_message(user_id, chat1.message_id)
        bot.delete_message(user_id, message.message_id)
        if res['result']['cheque'] is not None and 'pay_time' in res['result']['cheque']:
            print("Transaction was successful.")
            print(user_id_pay)
            print(sum)
            requests.post('http://ck83858.tw1.ru/api/')
            try:
                phone_number = bot_bd.view_number(user_id)
                dt_format = "%d-%m-%Y %H:%M:%S"
                a = datetime.now(timezone('Asia/Tashkent'))
                add_1xbet = requests.post(f'http://ck83858.tw1.ru/api/pay.php?user_id={user_id_pay}&summa={sum}').text
                print(f'{add_1xbet}\nTelegram id: {user_id}\n1xBetId {user_id_pay}')
                bot.send_message(user_id, f'💵 Пополнение счета\n🆔: {user_id_pay}\n👤 Ф.И.О: {name} {name1} {name2}\n💰 На счету: {balance} UZS\n💶 Сумма: {sum}UZS\n🕘 {a.strftime(dt_format)}\n✅ Успешно')
                bot.send_message(user_id, '*Выберите нужный раздел 👇*', reply_markup=buttonsbot.menu_button(), parse_mode='MarkDown')
                text_info1 = f'*🆔Account ID*: `{user_id_pay}`\nNumber: {phone_number[1]}\n*👤Ф.И.О*: *{name} {name1} {name2}*\n*💰Баланс*:' \
                             f' *{balance}*\n===============\n💵*Сумма: {sum} UZS' \
                             f'\n💸Услуга: 0 UZS*'
                chanel_id12 = -1001913028408
                bot.send_message(chanel_id12, text_info1, parse_mode='MarkDown')
                bot.register_next_step_handler(message, str_msg)

            except:
                bot.send_message(user_id, 'Ваш запрос не обработан!\nСообщите это администратору',
                                 reply_markup=buttonsbot.support_unsucceful(), parse_mode='MarkDown')
                bot.send_message(user_id, f'*Ваш id* `{user_id}`', reply_markup=buttonsbot.menu_button(),
                                 parse_mode='MarkDown')
                bot.register_next_step_handler(message, str_msg)

    elif message.text == 'Отменить 🚫':
        print("Transaction was cancellation.")
        print(user_id_pay)
        print(sum)
        bot.send_message(user_id, 'Операция отменена', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)

    else:
        print("Transaction was unsuccessful", user_id)
        bot.send_message(user_id, 'Вы еше не оплатили')
        bot.register_next_step_handler(message, check_payme, id, user_id_pay, sum, chat)


@bot.message_handler(commands=['xbet'])
def xbet(message):
    user_id = message.from_user.id
    id = [5225418097, 1819193668]
    if user_id in id:
        bot.send_message(user_id, 'Отправте 1xBet ID')
        bot.register_next_step_handler(message, get_id_xbet)
    else:
        bot.send_message(user_id, 'Ошибка', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg)


def get_id_xbet(message):
    user_id = message.from_user.id
    id = message.text
    result = requests.post(f'http://ck83858.tw1.ru/api/check.php?user_id={id}').text
    result = json.loads(result)
    id = result['Data'][0][0]
    name = result['Data'][0][2]
    name1 = result['Data'][0][3]
    name2 = result['Data'][0][4]
    balance = result['Data'][0][15]
    bot.send_message(user_id, f'*1XBET ID: {id}\nФ.И.О: {name} {name1} {name2}\nБаланс: {balance}*',
                     parse_mode='MarkDown')
    bot.register_next_step_handler(message, get_check_for_pay, id)


def get_check_for_pay(message, id):
    user_id = message.from_user.id
    sum = message.text
    requests.post(f'http://ck83858.tw1.ru/api/pay.php?user_id={id}&summa={sum}')
    time.sleep(5)
    result = requests.post(f'http://ck83858.tw1.ru/api/check.php?user_id={id}').text
    result = json.loads(result)
    id = result['Data'][0][0]
    name = result['Data'][0][2]
    name1 = result['Data'][0][3]
    name2 = result['Data'][0][4]
    balance = result['Data'][0][15]
    bot.send_message(user_id, f'*1XBET ID: {id}\nФ.И.О: {name} {name1} {name2}\nБаланс: {balance}*',
                     reply_markup=buttonsbot.menu_button(), parse_mode='MarkDown')
    bot.register_next_step_handler(message, str_msg)


# UZB
@bot.message_handler(commands=['uz'])
def start_message_uz(message):
    user_id = message.from_user.id
    checker = bot_bd.check_user(user_id)
    admin_id = 5225418097
    adm_id = 1819193668
    checker1 = bot_bd.check_id_admin(admin_id)
    if checker1 == True:
        if checker:
            bot.send_message(user_id, text=f'*FlamePayBot* - ga xush kelibsiz.\n'
                                           f'Bot bilan ishlash uchun kerakli bolimni tanlang 👇', parse_mode='Markdown',
                             reply_markup=buttonsbot.menu_button_uz())
            bot.register_next_step_handler(message, str_msg_uz)

        elif message.text == '/admin':
            bot.register_next_step_handler(message, start_admin)

        else:
            bot_bd.add_user(user_id)
            bot.send_message(user_id, text=f'*FlamePayBot* - ga xush kelibsiz.\n'
                                      f'Bot bilan ishlash uchun kerakli bolimni tanlang 👇', parse_mode='Markdown',
                             reply_markup=buttonsbot.menu_button_uz())
            bot.register_next_step_handler(message, str_msg_uz)

    elif message.text == '/start':
        bot.send_message(user_id, 'Бот перезапушен введите /start')
        bot.register_next_step_handler(message, start_message)

    elif message.text == '/admin':
        bot.register_next_step_handler(message, start_admin)

    else:
        bot.send_message(user_id, 'Bot vaqtincha ochirilgan', reply_markup=buttonsbot.bot_unsuported())
        bot.register_next_step_handler(message, bot_stop)


@bot.message_handler(chat_types=['text'])
def str_msg_uz(message):
    user_id = message.from_user.id
    if message.text == '💵Hisobni toldirish':
        admin_id = 1819193668
        photo = bot_bd.view_system(admin_id, 'xid')
        chat = bot.send_photo(user_id, photo[2], '*💵 1XBET UZS ID-gizni kiriting :*',
                              reply_markup=buttonsbot.return_pay_uz(), parse_mode='Markdown')
        bot.register_next_step_handler(message, get_id_pay_uz, chat)

    elif message.text == '📤Pulni yechib olish':
            admin_id = 1819193668
            photo = bot_bd.view_system(admin_id, 'withdraw')
            chat = bot.send_photo(user_id, photo[2], '*Kassa manzilimiz* :\n*Город: Нукус (Каракалпакстан)*\n'
                                                     '*Улица: Вечный огонь (24/7)*',
                                  reply_markup=buttonsbot.return_pay_uz(), parse_mode='Markdown')
            chat1 = bot.send_message(user_id, '💵* 1XBET UZS ID raqamingizni kiriting *:', parse_mode='Markdown')
            bot.register_next_step_handler(message, get_sum_withdraw_uz, chat, chat1)

    elif message.text == 'Tilni tanglash 🇷🇺 🇺🇿':
        user_id = message.from_user.id
        bot.send_message(user_id, 'Tilni tanlang', reply_markup=buttonsbot.set_language())
        bot.register_next_step_handler(message, select_language)

    elif message.text == '☎️ Texnik yordam':
        bot.send_message(user_id, '*Agar sizda botdan foydalanishda savollaringiz yoki'
                                  ' muammolaringiz bolsa:* @FlamePaySupport',
                         reply_markup=buttonsbot.menu_button(), parse_mode='Markdown')
        bot.register_next_step_handler(message, str_msg_uz)

    elif message.text == '/admin':
        bot.register_next_step_handler(message, start_admin)

    elif message.text == '/start':
        bot.send_message(user_id, 'Yana bir bor /start')
        bot.register_next_step_handler(message, start_message_uz)

    elif message.text == '/xbet':
        bot.register_next_step_handler(message, xbet)

    else:
        bot.send_message(user_id, 'Tugmasini ishlating')
        bot.register_next_step_handler(message, str_msg_uz)


def bot_stop_uz(message):
    user_id = message.from_user.id
    bot.send_message(user_id, config.bot_stop, parse_mode='Markdown')
    bot.register_next_step_handler(message, start_message)


def get_sum_withdraw_uz(message, chat, chat1):
    user_id = message.from_user.id
    if message.text:
        id_for_pay = message.text
        bot.delete_message(user_id, chat.message_id)
        bot.delete_message(user_id, chat1.message_id)
        bot.delete_message(user_id, message.message_id)
        try:
            select = requests.post(f'http://ck83858.tw1.ru/api/without.php?user_id={id_for_pay}').text
            select = json.loads(select)
            print(select)
            select_data = select['Data'][0][3]
            print(select)
            sum = select['Data'][0][5]
            print(sum)
            if message.text:
                if select_data == 'Операция выполнена успешно':
                    id = 1819193668
                    photo = bot_bd.view_system(id, 'withdraw_pass')
                    chat = bot.send_photo(user_id, photo[2], '*Plastik karta raqamingizni kiriting:*',
                                   reply_markup=buttonsbot.return_pay_uz(), parse_mode='Markdown')
                    bot.register_next_step_handler(message, fin_withdraw_uz, id_for_pay, sum, chat)

                elif select_data == 'Запрос на выплату не подтвержден, находится на рассмотрении':
                    bot.send_message(user_id, 'Toʻlov soʻrovi tasdiqlanmadi, kutilmoqda',
                                     reply_markup=buttonsbot.menu_button())
                    bot.register_next_step_handler(message, str_msg_uz)

                elif select_data == 'Валюта пользователя отличается от валюты кассы. Операция невозможна':
                    bot.send_message(user_id, 'Foydalanuvchining valyutasi kassa valyutasidan farq qiladi. Operatsiya mumkin emas')
                    bot.register_next_step_handler(message, str_msg_uz)

                else:
                    bot.send_message(user_id, 'Xato, pulni olib qoʻyish haqidagi soʻrovingiz topilmadi!',
                                     reply_markup=buttonsbot.menu_button_uz())
                    bot.register_next_step_handler(message, str_msg_uz)

            elif message.text == 'Bekor qilish 🚫':
                bot.send_message(user_id, 'Pul yechish bekor qilindi', reply_markup=buttonsbot.menu_button_uz())
                bot.register_next_step_handler(message, str_msg_uz)

            else:
                bot.send_message(user_id, 'Notogri ID')
                bot.register_next_step_handler(message, get_sum_withdraw_uz, chat, chat1)

        except:
            bot.send_message(user_id, '*Pul yechish bekor qilindi*', reply_markup=buttonsbot.menu_button_uz(),
                             parse_mode='MarkDown')
            bot.register_next_step_handler(message, str_msg_uz)

    else:
        bot.send_message(user_id, 'Bekor qilindi', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)


def fin_withdraw_uz(message, id_for_pay, sum, chat):
    user_id = message.from_user.id
    card = message.text
    bot.delete_message(user_id, chat.message_id)
    dt_format = "%d-%m-%Y %H:%M:%S"
    a = datetime.now(timezone('Asia/Tashkent'))
    number = bot_bd.view_number(user_id)
    if message.text:
        bot.send_message(user_id, f'🆔 {user_id}\n⬆Berish: {sum} UZS\n⬇Olish: {sum} UZS'
                                  f'\n💳CARD UZS: {card}\n📅Sana: {a.strftime(dt_format)}\n📝Status: Ожидайте⏳',
                         reply_markup=buttonsbot.menu_button(), parse_mode='Markdown')
        chanel_id12 = -1001913028408
        bot.send_message(chanel_id12, f'Запрос на вывод средств:\n\nTelegram : {user_id}\nNumber: {number[1]}\n1xBet ID:'
                                      f' {id_for_pay}\n'
                                    f'Pay Amount : `{sum}`\nCard number: `{card}`\nTime : {a.strftime(dt_format)}'
                                      f'\nСтатус: В ожидании⏳',
                         parse_mode='Markdown')
        bot_bd.delete_check(user_id)
        bot_bd.save_check(user_id, sum, card, id_for_pay)
        bot.register_next_step_handler(message, str_msg_uz)

    else:
        bot.send_message(user_id, 'Karta notogri kiritilgan')
        bot.register_next_step_handler(message, fin_withdraw_uz, id_for_pay)


def get_id_pay_uz(message, chat):
    user_id = message.from_user.id
    bot.delete_message(user_id, chat.message_id)
    bot.delete_message(user_id, message.message_id)
    user_id_pay = message.text
    v = str(user_id_pay)
    if 8 <= len(v) <= 9:
        result = requests.get(f'http://ck83858.tw1.ru/api/check.php?user_id={user_id_pay}').text
        result = json.loads(result)
        for i in result['Data']:
            chat = bot.send_message(user_id, f'*🆔Account ID: *`{i[0]}`\n👤*F.I.O*: {i[2]} {i[3]} {i[4]}\n💰Balans*:'
                                             f' {i[15]}*', parse_mode='Markdown')
            chat1 = bot.send_message(user_id, config.pay_min_uz, parse_mode='Markdown', reply_markup=buttonsbot.return_pay_uz())
            bot.register_next_step_handler(message, get_payment_sum_uz, user_id_pay, chat, chat1)

    elif message.text == 'Bekor qilish 🚫':
        bot.send_message(user_id, 'bekor qilindi', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)

    elif message.photo:
        bot.send_message(user_id, 'Foto munkin emas', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)

    else:
        bot.send_message(user_id, 'Notogri ID', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)


def get_payment_sum_uz(message, user_id_pay, chat, chat1):
    user_id = message.from_user.id
    if message.text == 'Bekor qilish 🚫':
        bot.send_message(user_id, 'bekor qilindi', reply_markup=buttonsbot.menu_button_uz())
        bot.register_next_step_handler(message, str_msg_uz)

    else:
        try:
            sum = message.text
            n = int(sum)
            if 1000 <= n <= 50000000:
                bot.delete_message(user_id, chat.message_id)
                bot.delete_message(user_id, chat1.message_id)
                bot.delete_message(user_id, message.message_id)
                headers = {
                    'device': '6Fk1rB',
                    'user-agent': 'Mozilla/57.36'
                }
                sum1 = int(sum) * 100

                data = {
                    "method": "p2p.create",
                    "params": {
                        "card_id": '6374d26a65f23ea1d3c687f2',
                        "amount": sum1,
                        "description": 'Rahmat'
                    }
                }

                response = requests.post('https://payme.uz/api/p2p.create', headers=headers, json=data)
                res = response.json()
                print(res)

                csv = {
                    '_id': res['result']['cheque']['_id'],
                    '_url': 'https://checkout.paycom.uz',
                    '_pay_amount': str(sum) + ' UZS',
                    '_pay_url': 'https://checkout.paycom.uz/' + str(res['result']['cheque']['_id'])
                }

                ec = {
                    '_details': csv
                }

                ec2 = {
                    '_result': ec
                }

                print(json.dumps(csv, indent=4))
                link = csv['_pay_url']
                id = csv['_id']
                try:
                    result = requests.get(f'http://ck83858.tw1.ru/api/check.php?user_id={user_id_pay}').text
                    result = json.loads(result)
                    # bot_bd.add_payment(user_id, user_id_pay, sum)
                    for i in result["Data"]:
                        kbi = telebot.types.InlineKeyboardMarkup()
                        button = telebot.types.InlineKeyboardButton('💸 Tolash', url=link)
                        kbi.add(button)
                        name = (i[2])
                        name1 = (i[3])
                        name2 = (i[4])
                        balance = (i[15])
                        text_info = f'*🆔Account ID*: `{i[0]}`\n*👤F.I.O*: *{i[2]} {i[3]} {i[4]}*\n*💰Balans*:' \
                                    f' *{i[15]}*\n===============\n💵*Summa: {sum} UZS' \
                                    f'\n💸Xizmat: 0 UZS\n💰Tolovga: {sum} UZS*'
                        chat = bot.send_message(user_id, text_info, parse_mode='Markdown', reply_markup=kbi)
                        chat1 = bot.send_message(user_id,
                                         f'1️⃣ Tolov uchun: Hisobimizga {sum} som otkazishingiz kerak,'
                                         f' quyidagi tugmani bosish orqali *( 💸 Tolash )* PayMe ilovasida!\n\n'
                                         f'2️⃣ Tolovdan keyin 10 daqiqa ichida tugmani bosishingiz kerak *( Tolandi ✅ )*',
                                         reply_markup=buttonsbot.ret_and_accept_uz(), parse_mode='MarkDown')
                        bot.register_next_step_handler(message, check_payme_uz, id, sum, user_id_pay, chat, name, name1, name2, balance, chat1)

                except ValueError:
                    bot.send_message(user_id, 'Yaroqsiz miqdor', reply_markup=buttonsbot.menu_button())
                    bot.register_next_step_handler(message, str_msg_uz)

            else:
                bot.send_message(user_id, 'Yaroqsiz miqdor', reply_markup=buttonsbot.menu_button())
                bot.register_next_step_handler(message, str_msg_uz)

        except ValueError:
            bot.send_message(user_id, 'Yaroqsiz miqdor', reply_markup=buttonsbot.menu_button())
            bot.register_next_step_handler(message, str_msg_uz)


def check_payme_uz(message, id, sum, user_id_pay, chat, name, name1, name2, balance, chat1):
    user_id = message.from_user.id
    headers = {
        'device': '6Fk1rB',
        'user-agent': 'Mozilla/57.36'
    }

    transaction_id = id

    data = {
        "method": "cheque.get",
        "params": {
            "id": transaction_id
        }
    }

    response = requests.post('https://payme.uz/api/cheque.get', headers=headers, json=data)
    res = response.json()
    info_succ = res['result']['cheque']['meta']['has_invoice']

    if info_succ == True:
        bot.delete_message(user_id, chat.message_id)
        bot.delete_message(user_id, chat1.message_id)
        bot.delete_message(user_id, message.message_id)
        if res['result']['cheque'] is not None and 'pay_time' in res['result']['cheque']:
            print("Transaction was successful.")
            print(user_id_pay)
            print(sum)
            requests.post('http://ck83858.tw1.ru/api/')
            try:
                phone_number = bot_bd.view_number(user_id)
                dt_format = "%d-%m-%Y %H:%M:%S"
                a = datetime.now(timezone('Asia/Tashkent'))
                add_1xbet = requests.post(f'http://ck83858.tw1.ru/api/pay.php?user_id={user_id_pay}&summa={sum}').text
                print(f'{add_1xbet}\nTelegram id: {user_id}\n1xBetId {user_id_pay}')
                bot.send_message(user_id,
                                 f'💵 Hisobni toldirish\n🆔: {user_id_pay}\n👤 Ф.И.О: {name} {name1} {name2}\n💰 Hisob: {balance} UZS\n💶 Summa: {sum}UZS\n🕘 {a.strftime(dt_format)}\n✅ Bajarildi', parse_mode='MarkDown')
                bot.send_message(user_id, '*Выберите нужный раздел 👇*', reply_markup=buttonsbot.menu_button(), parse_mode='MarkDown')
                chanel_id12 = -1001913028408
                text_info1 = f'*🆔Account ID*: `{user_id_pay}`\nNumber: {phone_number[1]}\n*👤F.I.O*: *{name} {name1} {name2}*\n*💰Balans*:' \
                             f' *{balance}*\n💵*Summa: {sum} UZS'\
                             f'\n💸Xizmat: 0 UZS*'
                bot.send_message(chanel_id12, text_info1, parse_mode='MarkDown')
                bot.register_next_step_handler(message, str_msg_uz)

            except:
                bot.send_message(user_id, 'Sizning sorovingiz korib chiqilmadi!\nBu haqda administratorga xabar bering',
                                 reply_markup=buttonsbot.support_unsucceful(), parse_mode='MarkDown')
                bot.send_message(user_id, f'*Sizning ID* `{user_id}`', reply_markup=buttonsbot.menu_button(),
                                 parse_mode='MarkDown')
                bot.register_next_step_handler(message, str_msg_uz)

    elif message.text == 'Bekor qilish 🚫':
        print("Transaction was cancellation.")
        print(user_id_pay)
        print(sum)
        bot.send_message(user_id, 'bekor qilindi', reply_markup=buttonsbot.menu_button())
        bot.register_next_step_handler(message, str_msg_uz)

    else:
        print("Transaction was unsuccessful", user_id)
        bot.send_message(user_id, 'Siz hali tolamagansiz')
        bot.register_next_step_handler(message, check_payme_uz, id, user_id_pay, sum, chat)


while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)
bot.polling()
