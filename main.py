import random
import telebot
import db_cur
from threading import Timer
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README_.txt
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README_.txt
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README_.txt
TOKEN = '6877130360:AAEGRWtyHS41iJ-mrInMWAAiQezFieZJcPM'
bot = telebot.TeleBot(TOKEN)
db_cur = db_cur.DBcur('users.db')

keyboard = InlineKeyboardMarkup()
keyboard.add(InlineKeyboardButton("Информация и помощь", callback_data='info'))
keyboard.add(InlineKeyboardButton("Баланс", callback_data='balance'),
             InlineKeyboardButton("Играть", callback_data='play'))
keyboard.add(InlineKeyboardButton("Зарабатывать LC", callback_data='job'),
             InlineKeyboardButton("Топ игроков", callback_data='top'))
keyboard.add(InlineKeyboardButton("Сад", callback_data='garden'),
             InlineKeyboardButton("Офисы", callback_data='offices'))


@bot.message_handler(content_types=['text'])
def handle_message(message):
    fetch = db_cur.get_balance(message.chat.id)
    if fetch == -2:
        if db_cur.create_player(message.chat.id):
            bot.send_message(message.chat.id, 'Вы успешно зарегестрировались! Выберите действие:',
                             reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка в базе данных. Наши разработчики уже всё исправляют, '
                                              'попробуйте позже.')
    else:
        text = str(message.text).lower()
        if text == '/balance' or text == 'баланс' or text == 'б':
            bot.send_message(message.chat.id, text=f'Ваш баланс: {round(db_cur.get_balance(message.chat.id), 3)} LC!')
            start_bot(message)
        elif text == '/play' or text == 'игра' or text == 'играть':
            bot.send_message(message.chat.id, text='Отлично! Теперь введите ставку.')
            bot.register_next_step_handler(message, play_part1)
        elif text == '/top' or text == 'топ':
            bot.send_message(message.chat.id, text=f'Топ 10 игроков на данный момент:\n\n{db_cur.get_top()}',
                             parse_mode='HTML')
            start_bot(message)
        elif text == '/garden' or text == 'сад' or text == 'сады':
            last_cost = db_cur.get_garden_last_cost(message.chat.id)
            new_cost = last_cost + (last_cost * 0.20)
            if last_cost == 0:
                new_cost = 1
            garden = db_cur.get_garden_trees(message.chat.id) - 0.001
            if garden == -0.001:
                garden = 0
            bot.send_message(message.chat.id, text='<b>Ваш сад.</b>\n\n'
                                                        f'Дереьвев посажено: {round(garden * 1000)}'
                                                        f'\nСтоимость прошлого дерева: {last_cost} LC'
                                                        f'\nСтоимость следующего дерева: {new_cost} LC'
                                                        f'\n\n<i>Для того, чтобы купить ещё одно дерево, '
                                                        f'напишите "ДА". Чтобы оказаться - "НЕТ"</i>',
                             parse_mode='HTML')
            bot.register_next_step_handler(message, buy_tree)
        elif text == '/offices' or text == 'офисы' or text == 'офис':
            last_cost = db_cur.get_office_last_cost(message.chat.id)
            new_cost = last_cost + (last_cost * 0.10)
            if last_cost == 0:
                new_cost = 50
            bot.send_message(message.chat.id, text='<b>Ваша компания.</b>\n\n'
                                                   f'Офисов куплено: {db_cur.get_office(message.chat.id)}'
                                                   f'\nСтоимость прошлого офиса: {last_cost} LC'
                                                   f'\nСтоимость следующего офиса: {new_cost} LC'
                                                   f'\n\n<i>Для того, чтобы купить ещё одие офис, '
                                                   f'напишите "ДА". Чтобы оказаться - "НЕТ"</i>',
                             parse_mode='HTML')
            bot.register_next_step_handler(message, buy_office)
        elif text == '/job' or text == 'работать' or text == 'ворк':
            bot.send_message(message.chat.id, text='Вы начали зарабатывать LC. За каждый написанный символ вы '
                                                   'получите 0.001 LC')
            bot.register_next_step_handler(message, job_do)
        elif text == '/info' or text == 'помощь' or text == 'инфо' or text == 'информация':
            bot.send_message(message.chat.id, open('map.txt', 'r', encoding='utf-8').read(), parse_mode='HTML')
        else:
            start_bot(message)


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id, text='Выберите действие:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data)
def query_handler_assortment(call):
    bot.answer_callback_query(call.id)
    if call.data == 'balance':
        bot.send_message(call.message.chat.id, text=f'Ваш баланс: {round(db_cur.get_balance(call.message.chat.id), 3)} LC!')
    elif call.data == 'play':
        bot.send_message(call.message.chat.id, text='Отлично! Теперь введите ставку.')
        bot.register_next_step_handler(call.message, play_part1)
    elif call.data == 'job':
        bot.send_message(call.message.chat.id, text='Вы начали зарабатывать LC. За каждый написанный символ вы '
                                                    'получите 0.001 LC')
        bot.register_next_step_handler(call.message, job_do)
    elif call.data == 'garden':
        last_cost = db_cur.get_garden_last_cost(call.message.chat.id)
        new_cost = last_cost + (last_cost * 0.20)
        if last_cost == 0:
            new_cost = 1
        garden = db_cur.get_garden_trees(call.message.chat.id) - 0.001
        if garden == -0.001:
            garden = 0
        bot.send_message(call.message.chat.id, text='<b>Ваш сад.</b>\n\n'
                                               f'Дереьвев посажено: {round(garden * 1000)}'
                                               f'\nСтоимость прошлого дерева: {last_cost} LC'
                                               f'\nСтоимость следующего дерева: {new_cost} LC'
                                               f'\n\n<i>Для того, чтобы купить ещё одно дерево, '
                                               f'напишите "ДА". Чтобы оказаться - "НЕТ"</i>',
                         parse_mode='HTML')
        bot.register_next_step_handler(call.message, buy_tree)
    elif call.data == 'offices':
        last_cost = db_cur.get_office_last_cost(call.message.chat.id)
        new_cost = last_cost + (last_cost * 0.10)
        if last_cost == 0:
            new_cost = 50
        bot.send_message(call.message.chat.id, text='<b>Ваша компания.</b>\n\n'
                                               f'Офисов куплено: {db_cur.get_office(call.message.chat.id)}'
                                               f'\nСтоимость прошлого офиса: {last_cost} LC'
                                               f'\nСтоимость следующего офиса: {new_cost} LC'
                                               f'\n\n<i>Для того, чтобы купить ещё одие офис, '
                                               f'напишите "ДА". Чтобы оказаться - "НЕТ"</i>',
                         parse_mode='HTML')
        bot.register_next_step_handler(call.message, buy_office)
    elif call.data == 'top':
        bot.send_message(call.message.chat.id, text=f'Топ 10 игроков на данный момент:\n\n{db_cur.get_top()}',
                         parse_mode='HTML')
    elif call.data == 'info':
        bot.send_message(call.message.chat.id, open('map.txt', 'r', encoding='utf-8').read(), parse_mode='HTML')


def buy_tree(message):
    text = str(message.text).lower()
    if text == 'да':
        lvl = (db_cur.get_garden_trees(message.chat.id) - 0.001) * 1000
        if lvl < 10:
            price = db_cur.get_garden_last_cost(message.chat.id)
            price = price + (price * 0.20)
            balance = db_cur.get_balance(message.chat.id)
            if price == 0:
                price = 1
            if balance >= price:
                bot.send_message(message.chat.id, f'Вы успешно купили ещё одно дерево за {price} LC!')
                db_cur.update_garden(message.chat.id)
                db_cur.update_garden_last_cost(message.chat.id, price)
                db_cur.set_balance(message.chat.id, balance - price)
            else:
                bot.send_message(message.chat.id, 'У вас недостаточно средств для покупки дерева!'
                                                  f'\nНужно: {price} LC'
                                                  f'\nВаш баланс: {balance} LC')
        else:
            bot.send_message(message.chat.id, 'У вас уже максимальное кол-во деревьев!')
    else:
        bot.send_message(message.chat.id, 'Вы отказались от покупки дерева, или ввели некорректный ответ.')


def buy_office(message):
    text = str(message.text).lower()
    if text == 'да':
        lvl = db_cur.get_office(message.chat.id)
        if lvl < 10:
            price = db_cur.get_office_last_cost(message.chat.id)
            price = price + (price * 0.10)
            balance = db_cur.get_balance(message.chat.id)
            if price == 0:
                price = 50
            if balance >= price:
                bot.send_message(message.chat.id, f'Вы успешно купили ещё один офис за {price} LC!')
                db_cur.update_office(message.chat.id)
                db_cur.update_office_last_cost(message.chat.id, price)
                db_cur.set_balance(message.chat.id, balance - price)
            else:
                bot.send_message(message.chat.id, 'У вас недостаточно средств для покупки офиса!'
                                                  f'\nНужно: {price} LC'
                                                  f'\nВаш баланс: {balance} LC')
        else:
            bot.send_message(message.chat.id, 'У вас уже максимальное кол-во офисов!')
    else:
        bot.send_message(message.chat.id, 'Вы отказались от покупки офиса, или ввели некорректный ответ.')


def job_do(message):
    i = 0
    earn = 0.0
    plus = db_cur.get_garden(message.chat.id)
    if plus >= 0.002:
        bot.send_message(message.chat.id, f'У вас есть сад, поэтому ваш доход увеличен до {plus} LC за символ!')
    while i < len(str(message.text)):
        earn += plus
        i += 1
    earn = round(earn, 3)
    bot.send_message(chat_id=message.chat.id, text=f'В написанном тексте было {len(str(message.text))} символов. Вы '
                                                   f'заработали: <b>{earn} LC</b>', parse_mode='HTML')
    balance = round(db_cur.get_balance(message.chat.id) + earn, 3)
    db_cur.set_balance(message.chat.id, balance)


def play_part1(message):
    global bet
    text = str(message.text).replace('.', '')
    if text.isdigit():
        bet = float(message.text)
        if bet <= db_cur.get_balance(message.chat.id):
            bot.send_message(message.chat.id, text=f'Ваша ставка: {bet} LC. Игра началась!\n'
                                                   'Если вы выиграете - выиграете х3 от своей ставки.\n'
                                                   'Если проиграете - ваша ставка сгорит.\n\n'
                                                   'Правила игры простые. Я загадываю число от 1 до 3. Если отгадаете '
                                                   '- вы выиграли')
            bot.register_next_step_handler(message, play_part2)
    else:
        bot.send_message(message.chat.id, text='Ставка должна быть числом!')


def play_part2(message):
    global bet
    text = str(message.text)
    if text.isdigit():
        number = int(text)
        my_number = random.randint(1, 3)
        if number == my_number:
            bot.send_message(message.chat.id, f'Вы выиграли в игре, и получаете {bet * 3} LC. Поздравляю!')
            balance = round(db_cur.get_balance(message.chat.id) + (bet * 3), 3)
        else:
            bot.send_message(message.chat.id, f'Вы проиграли в игре. С вашего баланса списано {bet} LC. '
                                              f'Удачи в следующий раз!\n\nЗагаданное число: {my_number}')
            balance = round(db_cur.get_balance(message.chat.id) - bet, 3)
        db_cur.set_balance(message.chat.id, balance)
    else:
        bot.send_message(message.chat.id, 'В тексте должно присутствовать только одно число от 1 до 3! Попробуйте ещё '
                                          'раз')
        bot.register_next_step_handler(message, play_part2)


def repeater(interval, function):
    Timer(interval, repeater, [interval, function]).start()
    function()


def give_passive():
    players = db_cur.cur.execute(f"SELECT * FROM offices;").fetchall()
    for player in players:
        if player[1] > 0:
            balance = db_cur.get_balance(player[0]) + player[1]
            db_cur.set_balance(player[0], balance)
            bot.send_message(player[0], f'Вам был начислен пассивный доход в размере {player[1]} LC'
                                        f' за ваши офисы.')


repeater(3600, give_passive)
bot.polling(none_stop=True)
