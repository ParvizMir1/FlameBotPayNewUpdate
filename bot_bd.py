import sqlite3

connection = sqlite3.connect('bot2.db')
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS system (telegram_id INTEGER, photo_name TEXT, photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS user (telegram_id INTEGER);')
sql.execute('CREATE TABLE IF NOT EXISTS payment_info (telegram_id INTEGER, id_pay INTEGER, payment_sum INTEGER);')
sql.execute('CREATE TABLE IF NOT EXISTS all_check (telegram_id INTEGER, photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS all_check_temporary (telegram_id INTEGER, id_pay INTEGER, payment_sum '
            'INTEGER, photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS withdraw(telegram_id INTEGER, id_for_pay INTEGER,'
            ' password_id TEXT, card_number INTEGER);')
sql.execute('CREATE TABLE IF NOT EXISTS withdraw_temporary(telegram_id INTEGER, id_for_pay INTEGER,'
            ' password_id TEXT, card_number INTEGER);')
sql.execute('CREATE TABLE IF NOT EXISTS admin_id (telegram_id INTEGER);')
sql.execute('CREATE TABLE IF NOT EXISTS withdraw_sum (telegram_id INTEGER, sum_with TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS withdraw_sum_temporary (telegram_id INTEGER, sum_with TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS photo_text (telegram_id INTEGER, text TEXT, photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS document_text (telegram_id INTEGER, text TEXT, document TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS checks (telegram_id INTEGER, sum TEXT, card TEXT, xbet);')
sql.execute('CREATE TABLE IF NOT EXISTS number (telegram_id INTEGER, phone_number TEXT);')


def add_number(user_id, number):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO number VALUES (?,?);', (user_id, number))

    connection.commit()


def view_number(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM number WHERE telegram_id=?;', (user_id,)).fetchone()

    return s


def add_sum(user_id, sum_amount):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO withdraw_sum VALUES (?,?);', (user_id, sum_amount))

    connection.commit()


def view_withdraw_sum(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM withdraw_sum_temporary WHERE telegram_id=?;', (user_id,)).fetchone()

    return s


def add_sum_temporary(user_id, sum_amount):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO withdraw_sum_temporary VALUES (?,?);', (user_id, sum_amount))

    connection.commit()


def delete_sum_temporary(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM withdraw_sum_temporary WHERE telegram_id=?;', (user_id,)).fetchall()

    connection.commit()


# Проверка пользователя
def check_user(telegram_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT telegram_id FROM user WHERE telegram_id=?', (telegram_id,)).fetchone()

    if checker:
        return True
    else:
        return False


# Добавление пользователя
def add_user(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO user VALUES (?);', (user_id,))

    connection.commit()


# Вывод рассылка
def check_user_rass():
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT telegram_id FROM user;').fetchall()

    return checker


# Добавление системную инфу
def add_for_system(user_id, photo_name, photo):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO system VALUES (?,?,?)', (user_id, photo_name, photo))

    connection.commit()


# Вывод системной инфы
def view_system(user_id, photo_name):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM system WHERE telegram_id=? and photo_name=?;', (user_id, photo_name)).fetchone()

    return s


# Удаление системной инфы
def delete_system(photo_name):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM system WHERE photo_name=?;', (photo_name,)).fetchall()

    connection.commit()


# Добавления истории платежа
def add_payment(user_id, id_pay, payment_sum):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO payment_info VALUES (?,?,?)', (user_id, id_pay, payment_sum))

    connection.commit()


# Вывод историю платежа
def view_payment(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('SELECT * FROM payment_info WHERE telegram_id=?', (user_id,)).fetchone()

    connection.commit()


# Добавления чека в бд
def add_check(user_id, photo):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO all_check VALUES (?,?);', (user_id, photo))

    connection.commit()


def add_temporary(user_id, id_pay, pay_sum, photo):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO all_check_temporary VALUES (?,?,?,?);', (user_id, id_pay, pay_sum, photo))

    connection.commit()


# Вывод чека для админ
def view_check(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM all_check_temporary WHERE telegram_id=?;', (user_id,)).fetchone()

    return s


# Функция обновления для админа
def delete_upd(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM all_check_temporary WHERE telegram_id=?', (user_id,)).fetchall()

    connection.commit()


# Добавления данных для вывода
def add_withdraw(user_id, id_for_pay, password_id, card_number):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO withdraw VALUES(?,?,?,?);', (user_id, id_for_pay, password_id, card_number))

    connection.commit()


# Обновления данных для пополнения
def add_withdraw_temporary(user_id, id_for_pay, password_id, card_number):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO withdraw_temporary VALUES(?,?,?,?);', (user_id, id_for_pay, password_id, card_number))

    connection.commit()


# Вывод данных для пополнения
def view_withdraw(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM withdraw_temporary WHERE telegram_id=?;', (user_id,)).fetchone()

    return s


# Функция обновления для корректной работы
def delete_withdraw(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM withdraw_temporary WHERE telegram_id=?', (user_id,)).fetchall()

    connection.commit()


# Функция блокировки
def add_admin_id(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO admin_id VALUES(?);', (user_id,))

    connection.commit()


def check_id_admin(telegram_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT telegram_id FROM admin_id WHERE telegram_id=?', (telegram_id,)).fetchone()

    if checker:
        return True
    else:
        return False


def unblock_admin(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM admin_id WHERE telegram_id=?', (user_id,)).fetchall()

    connection.commit()


def delete_user(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM user WHERE telegram_id=?', (user_id,)).fetchone()

    connection.commit()


# Для рассылки
def add_photo_text(user_id, text, photo):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO photo_text VALUES(?,?,?);', (user_id, text, photo))

    connection.commit()


# Для рассылки
def view_photo_text(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM photo_text WHERE telegram_id=?;', (user_id,)).fetchone()

    return s


def add_document_text(user_id, text, document):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO document_text VALUES(?,?,?);', (user_id, text, document))

    connection.commit()


def view_document_text(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM document_text WHERE telegram_id=?;', (user_id,)).fetchone()

    return s


def delete_photo(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM photo_text WHERE telegram_id=?', (user_id,)).fetchall()

    connection.commit()


def delete_document(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM document_text WHERE telegram_id=?', (user_id,)).fetchall()

    connection.commit()
#####################################


def save_check(user_id, sum, card, xbet):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO checks VALUES(?,?,?,?)', (user_id, sum, card, xbet))

    connection.commit()


def view_checks(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()

    s = sql.execute('SELECT * FROM checks WHERE telegram_id=?', (user_id,)).fetchone()

    return s


def delete_check(user_id):
    connection = sqlite3.connect('bot2.db')
    sql = connection.cursor()
    try:
        sql.execute('DELETE * FROM check WHERE telegram_id=?', (user_id,))

        connection.commit()

    except:
        return
