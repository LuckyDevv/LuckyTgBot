import base64
import random
import urllib.request
from threading import Timer
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import db_cur

#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README.md
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README.md
#  ПЕРЕД ВКЛЮЧЕНИЕМ БОТА. ОБЯЗАТЕЛЬНО ПРОЧТИТЕ ФАЙЛ README.md
TOKEN = ''  # Введите сюда токен своего Telegram-бота
bot = telebot.TeleBot(TOKEN)
db_cur = db_cur.DBcur('users.db')
last_messages = {}

map_text = base64.b64decode('PGI+0JTQsNC90L3Ri9C5INCx0L7RgiDQvdC1INGP0LLQu9GP0LXRgtGB0Y'
                            '8g0YHRgNC10LTRgdGC0LLQvtC8INC30LDRgNCw0LHQvtGC0LrQsCDQuCDQvd'
                            'C1INC/0YDQvtCy0L7RhtC40YDRg9C10YIg0L3QsCDQuNCz0YDRgyDQsiDQsNC30LD'
                            'RgNGC0L3Ri9C1INC40LPRgNGLITwvYj4KCjxiPkx1Y2t5Q29pbiAoTEMpPC9iPi'
                            'AtINCy0L3Rg9GC0YDQuNC40LPRgNC+0LLQsNGPINCy0LDQu9GO0YLQsCwg0L'
                            'rQvtGC0L7RgNGD0Y4g0LzQvtC20L3QviAi0LfQsNGA0LDQsdCw0YLRi9Cy0LDRgt'
                            'GMIiDQuCDRgtGA0LDRgtC40YLRjCDQvdCwINCy0L3Rg9GC0YDQuNC40LPRgNC+0LLRi9'
                            'C1INC/0L7QutGD0L/QutC4Cgo8Yj7QodC/0L7RgdC+0LHRiyDQt9Cw0YDQsNC'
                            'x0L7RgtC60LAgTEM6PC9iPgo8aT48Yj4xLiDQmtC90L7Qv9C60LAgItCX0LDR'
                            'gNCw0LHQsNGC0YvQstCw0YLRjCBMQyIg0LjQu9C4INC60L7QvNCw0L3QtNCwIC9qb'
                            '2IuPC9iPjwvaT4K0JLQsNC8INC/0L7RgtGA0LXQsdGD0LXRgtGB0Y8g0L/QuNGB0LDRgtG'
                            'MINGC0LXQutGB0YIsINC80L3QvtCz0L4g0YLQtdC60YHRgtCwLiDQl9CwINC60'
                            'LDQttC00YvQuSDRgdC40LzQstC+0Lsg0LIg0YLQtdC60YHRgtC1INCy0LDQvCDQvd'
                            'Cw0YfQuNGB0LvRj9C10YLRgdGPIDAuMDAxIExDLiDQp9C10Lwg0LHQvtC70YzRiNC1I'
                            'NGC0LXQutGB0YLQsCAtINGC0LXQvCDQsdC+0LvRjNGI0LUg0LLRiyDQt9Cw0YDQsNCx0L7Rg'
                            'tCw0LXRgtC1LiAKPGk+PGI+Mi4g0JrQvdC+0L/QutCwICLQodCw0LQiINC40LvQuCDQu'
                            'tC+0LzQsNC90LTQsCAvZ2FyZGVuLjwvYj48L2k+CtCt0YLQviDQvdC1INGB0YDQtdC00YHRgtC'
                            'y0L4g0LfQsNGA0LDQsdC+0YLQutCwLCDQvtC00L3QsNC60L4g0LTQsNGB0YIg0LLQsNC8I'
                            'NC+0YnRg9GC0LjQvNC+0LUg0YPQu9GD0YfRiNC10L3QuNC1INC30LDRgNCw0LHQvtGC0LrQsC4g0'
                            'J/QtdGA0LLQvtC1INC00LXRgNC10LLQviDRgdGC0L7QuNGCIDEgTEMuINCf0L7RgdC70L'
                            'XQtNGD0Y7RidC40LUg0LTQtdGA0LXQstGM0Y8g0L7RhtC10L3QuNCy0LDRjtGC0YHRjyArMj'
                            'AlINC6INC/0YDQvtGI0LvQvtC5INGB0YPQvNC80LUg0L/QvtC60YPQv9C60LguINCc0LD'
                            'QutGB0LjQvNGD0Lwg0LzQvtC20L3QviDQuNC80LXRgtGMIDEwINC00LXRgNC10LLRjNC10LIu'
                            'CjxpPjxiPjMuINCa0L3QvtC/0LrQsCAi0J7RhNC40YEiINC40LvQuCDQutC+0LzQsNC9'
                            '0LTQsCAvb2ZmaWNlcy48L2I+PC9pPgrQrdGC0L4g0L/QsNGB0YHQuNCy0L3Ri9C5INCy0LjQt'
                            'CDQt9Cw0YDQsNCx0L7RgtC60LAuINCa0LDQttC00YvQuSDRh9Cw0YEg0L/QviDRgdC'
                            '10YDQstC10YDQvdC+0LzRgyDQstGA0LXQvNC10L3QuCDQstCw0Lwg0LHRg9C00LXRgiDQvdCw0'
                            'YfQuNGB0LvRj9GC0YzRgdGPIDEgTEMg0LfQsCDQutCw0LbQtNGL0Lkg0LrRg9C/'
                            '0LvQtdC90L3Ri9C5INC+0YTQuNGBLiDQn9C10YDQstGL0Lkg0L7RhNC40YEg0YHRgtC+0'
                            'LjRgiA1MCBMQy4g0J/QvtGB0LvQtdC00YPRjtGJ0LjQtSDRgdGC0L7Rj9G'
                            'CICsxMCUg0Log0L/RgNC+0YjQu9C+0Lkg0YHRg9C80LzQtSD'
                            'Qv9C+0LrRg9C/0LrQuCDQnNCw0LrRgdC40LzRg9C8INC80L7QttC90L4g0Lj'
                            'QvNC10YLRjCAyMCDQvtGE0LjRgdC+0LIuCjxpPjxiPjQuINCa0L3QvtC/0LrQsCAi0Jj'
                            'Qs9GA0LDRgtGMIiDQuNC70Lgg0LrQvtC80LDQvdC00LAgL3BsYXkuPC9iPjw'
                            'vaT4K0K3RgtC+INCw0LfQsNGA0YLQvdGL0Lkg0LLQuNC0INC30LDRgNCw0LHQvtGC0L'
                            'rQsC4g0JLRiyDQtNC+0LvQttC90Ysg0LLRi9Cx0YDQsNGC0Ywg0YHR'
                            'g9C80LzRgyDRgdGC0LDQstC60LggKNGB0YPQvNC80LAg0YHRgtCw0LLQut'
                            'C4INC80L7QttC10YIg0LHRi9GC0Ywg0LvRjtCx0LDRjykuINCR0L7RgiDQt9Cw'
                            '0LPQsNC00YvQstCw0LXRgiDRh9C40YHQu9C+INC+0YIgMSDQtNC+IDMuINCS0L'
                            'DRiNCwINC30LDQtNCw0YfQsCAtINGD0LPQsNC00LDRgtGMLCDQutCw0LrQvtC1INGH0'
                            'LjRgdC70L4g0LfQsNCz0LDQtNCw0Lsg0LHQvtGCLiDQn9GA0Lgg0LLRi9C40LPRgNGL0Y'
                            'jQtSDQstGLINC/0L7Qu9GD0YfQsNC10YLQtSDRhTMg0L7RgiDRgdGC0LDQstC60LguINC'
                            'f0YDQuCDQv9GA0L7QuNCz0YDRi9GI0LUg0YEg0LLQsNGI0LXQs9C+INCx0LDQu9Cw0L3Rgd'
                            'CwINGB0L/QuNGB0YvQstCw0LXRgtGB0Y8g0YHRg9C80LzQsCDRgdGC0LDQstC60LguINCa0L7'
                            'Quy3QstC+INC/0L7Qv9GL0YLQvtC6INC90LUg0L7Qs9GA0LDQvdC40YfQtdC90L4uINCU0LDQvd'
                            'C90YvQuSDRgdC/0L7RgdC+0LEg0LfQsNGA0LDQsdC+0YLQutCwINC/0L7QtNC+0LnQtNC10YIg0YL'
                            'QvtC70YzQutC+INC00LvRjyDRgtC10YUsINC60YLQviDQu9GO0LHQuNGCINGA0LjRgdC60L7QstCw0'
                            'YLRjCDQuCDQv9C40YLRjCDRiNCw0LzQv9Cw0L3RgdC60L7QtS4KCtCi0L7QvyDQuNCz0YDQvtC60L7Q'
                            'siAtINGN0YLQviDQu9C40YjRjCDRgdC/0L7RgdC+0LEg0L/QvtC60LDQt9Cw0YLRjCDRgdCy0L7RkSDRg'
                            'dC+0YHRgtC+0Y/QvdC40LUg0YHRgNC10LTQuCDQtNGA0YPQs9C40YUg0LjQs9GA0L7QutC+0LIuINCX0LA'
                            'g0L3QsNGF0L7QttC00LXQvdC40LUg0LIg0YLQvtC/0LUg0LLRiyDQvdC1INC/0L7Qu9GD0YfQsNC10YLQtSD'
                            'QvdC40LrQsNC60LjRhSDQuNCz0YDQvtCy0YvRhSDQv9GA0LXQuNC80YPRidC10YHRgtCyLgoKPGk+PGI+'
                            '0KHQvtC30LTQsNGC0LXQu9GMINCx0L7RgtCwIC0gTHVja3lEZXZ2IChAbHVja3lkZXZ2KTwvYj4'
                            '8L2k+CjxpPtCSINCx0L7RgtC1INC+0YLRgdGD0YLRgdGC0LLRg9GO0YIg0L/QvtC60YPQv'
                            '9C60Lgg0LfQsCDQvdCw0YHRgtC+0Y/RidC40LUg0LTQtdC90YzQs9C4INC4INCy0L7Qt9C80'
                            'L7QttC90L7RgdGC0Ywg0LrRg9C/0LjRgtGMINCy0LDQu9GO0YLRgyDQt9CwINC90LDRgdGC0'
                            'L7Rj9GJ0LjQtSDQtNC10L3RjNCz0LguPC9pPgoKPGI+PGEgaHJlZj0iaHR0cHM6Ly9naXRod'
                            'WIuY29tL0x1Y2t5RGV2di9MdWNreVRnQm90Ij7QntGE0LjRhtC40LDQu9GM0L3Ri9C5IEdpdEh'
                            '1YiDQsdC+0YLQsDwvYT48L2I+')  # ЕСЛИ ВЫ УБЕРЕТЕ ДАННЫЙ КОД, БОТ НЕ БУДЕТ РАБОТАТЬ

keyboard = InlineKeyboardMarkup()
keyboard.add(InlineKeyboardButton("Информация и помощь", callback_data='info'))
keyboard.add(InlineKeyboardButton("Баланс", callback_data='balance'),
             InlineKeyboardButton("Играть", callback_data='play'))
keyboard.add(InlineKeyboardButton("Зарабатывать LC", callback_data='job'),
             InlineKeyboardButton("Топ игроков", callback_data='top'))
keyboard.add(InlineKeyboardButton("Сад", callback_data='garden'),
             InlineKeyboardButton("Офисы", callback_data='offices'))


def deleteOldMessage(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass


@bot.message_handler(content_types=['text'])
def handle_message(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    fetch = db_cur.get_balance(message.chat.id)
    if fetch == -2:
        if db_cur.create_player(message.chat.id, message.from_user.first_name):
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, 'Вы успешно зарегестрировались! Выберите действие:',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
        else:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id,
                                          'Произошла ошибка в базе данных. Наши разработчики уже всё исправляют, '
                                          'попробуйте позже.').message_id
            last_messages[message.chat.id] = message_id
    else:
        text = str(message.text).lower()
        if text == '/balance' or text == 'баланс' or text == 'б':
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id,
                                          text=f'Ваш баланс: {round(db_cur.get_balance(message.chat.id), 3)} LC!',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
        elif text == '/play' or text == 'игра' or text == 'играть':
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, text='Отлично! Теперь введите ставку.').message_id
            last_messages[message.chat.id] = message_id
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.register_next_step_handler(message, play_part1)
        elif text == '/top' or text == 'топ':
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id,
                                          text=f'Топ 10 игроков на данный момент:\n\n{db_cur.get_top()}',
                                          parse_mode='HTML', reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
        elif text == '/garden' or text == 'сад' or text == 'сады':
            last_cost = db_cur.get_garden_last_cost(message.chat.id)
            new_cost = last_cost + (last_cost * 0.20)
            if last_cost == 0:
                new_cost = 1
            garden = db_cur.get_garden_trees(message.chat.id) - 0.001
            if garden == -0.001:
                garden = 0
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, text='<b>Ваш сад.</b>\n\n'
                                                                f'Дереьвев посажено: {round(garden * 1000)}'
                                                                f'\nСтоимость прошлого дерева: {last_cost} LC'
                                                                f'\nСтоимость следующего дерева: {new_cost} LC'
                                                                f'\n\n<i>Для того, чтобы купить ещё одно дерево, '
                                                                f'напишите "ДА". Чтобы оказаться - "НЕТ"</i>',
                                          parse_mode='HTML').message_id
            last_messages[message.chat.id] = message_id
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.register_next_step_handler(message, buy_tree)
        elif text == '/offices' or text == 'офисы' or text == 'офис':
            last_cost = db_cur.get_office_last_cost(message.chat.id)
            new_cost = last_cost + (last_cost * 0.10)
            if last_cost == 0:
                new_cost = 50
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, text='<b>Ваша компания.</b>\n\n'
                                                                f'Офисов куплено: {db_cur.get_office(message.chat.id)}'
                                                                f'\nСтоимость прошлого офиса: {last_cost} LC'
                                                                f'\nСтоимость следующего офиса: {new_cost} LC'
                                                                f'\n\n<i>Для того, чтобы купить ещё одие офис, '
                                                                f'напишите "ДА". Чтобы оказаться - "НЕТ"</i>',
                                          parse_mode='HTML').message_id
            last_messages[message.chat.id] = message_id
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.register_next_step_handler(message, buy_office)
        elif text == '/job' or text == 'работать' or text == 'ворк':
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id,
                                          text='Вы начали зарабатывать LC. За каждый написанный символ вы '
                                               'получите 0.001 LC').message_id
            last_messages[message.chat.id] = message_id
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.register_next_step_handler(message, job_do)
        elif text == '/info' or text == 'помощь' or text == 'инфо' or text == 'информация':
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, map_text,
                                          parse_mode='HTML', disable_web_page_preview=True,
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
        else:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(chat_id=message.chat.id, text='Выберите действие:',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try:
        deleteOldMessage(message.chat.id, last_messages[message.chat.id])
    except:
        pass
    message_id = bot.send_message(chat_id=message.chat.id, text='Выберите действие:', reply_markup=keyboard).message_id
    last_messages[message.chat.id] = message_id


@bot.callback_query_handler(func=lambda call: call.data)
def query_handler_assortment(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id)
    if call.data == 'balance':
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id,
                                      text=f'Ваш баланс: {round(db_cur.get_balance(call.message.chat.id), 3)} LC!',
                                      reply_markup=keyboard).message_id
        last_messages[call.message.chat.id] = message_id
    elif call.data == 'play':
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id, text='Отлично! Теперь введите ставку.').message_id
        last_messages[call.message.chat.id] = message_id
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.register_next_step_handler(call.message, play_part1)
    elif call.data == 'job':
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id,
                                      text='Вы начали зарабатывать LC. За каждый написанный символ вы '
                                           'получите 0.001 LC').message_id
        last_messages[call.message.chat.id] = message_id
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.register_next_step_handler(call.message, job_do)
    elif call.data == 'garden':
        last_cost = db_cur.get_garden_last_cost(call.message.chat.id)
        new_cost = last_cost + (last_cost * 0.20)
        if last_cost == 0:
            new_cost = 1
        garden = db_cur.get_garden_trees(call.message.chat.id) - 0.001
        if garden == -0.001:
            garden = 0
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id, text='<b>Ваш сад.</b>\n\n'
                                                                 f'Дереьвев посажено: {round(garden * 1000)}'
                                                                 f'\nСтоимость прошлого дерева: {last_cost} LC'
                                                                 f'\nСтоимость следующего дерева: {new_cost} LC'
                                                                 f'\n\n<i>Для того, чтобы купить ещё одно дерево, '
                                                                 f'напишите "ДА". Чтобы оказаться - любое другое '
                                                                 f'слово</i>',
                                      parse_mode='HTML').message_id
        last_messages[call.message.chat.id] = message_id
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.register_next_step_handler(call.message, buy_tree)
    elif call.data == 'offices':
        last_cost = db_cur.get_office_last_cost(call.message.chat.id)
        new_cost = last_cost + (last_cost * 0.10)
        if last_cost == 0:
            new_cost = 50
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id, text='<b>Ваша компания.</b>\n\n'
                                                                 f'Офисов куплено: {db_cur.get_office(call.message.chat.id)}'
                                                                 f'\nСтоимость прошлого офиса: {last_cost} LC'
                                                                 f'\nСтоимость следующего офиса: {new_cost} LC'
                                                                 f'\n\n<i>Для того, чтобы купить ещё одие офис, '
                                                                 f'напишите "ДА". Чтобы оказаться - любое другое слово</i>',
                                      parse_mode='HTML').message_id
        last_messages[call.message.chat.id] = message_id
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.register_next_step_handler(call.message, buy_office)
    elif call.data == 'top':
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id,
                                      text=f'Топ 10 игроков на данный момент:\n\n{db_cur.get_top()}',
                                      parse_mode='HTML', reply_markup=keyboard).message_id
        last_messages[call.message.chat.id] = message_id
    elif call.data == 'info':
        try:
            deleteOldMessage(call.message.chat.id, last_messages[call.message.chat.id])
        except:
            pass
        message_id = bot.send_message(call.message.chat.id, map_text,
                                      parse_mode='HTML', disable_web_page_preview=True,
                                      reply_markup=keyboard).message_id
        last_messages[call.message.chat.id] = message_id


def buy_tree(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    text = str(message.text).lower().strip()
    if text == 'да':
        lvl = (db_cur.get_garden_trees(message.chat.id) - 0.001) * 1000
        if lvl < 20:
            price = db_cur.get_garden_last_cost(message.chat.id)
            price = price + (price * 0.20)
            balance = db_cur.get_balance(message.chat.id)
            if price == 0:
                price = 1
            if balance >= price:
                try:
                    deleteOldMessage(message.chat.id, last_messages[message.chat.id])
                except:
                    pass
                message_id = bot.send_message(message.chat.id, f'Вы успешно купили ещё одно дерево за {price} LC!',
                                              reply_markup=keyboard).message_id
                last_messages[message.chat.id] = message_id
                db_cur.update_garden(message.chat.id)
                db_cur.update_garden_last_cost(message.chat.id, price)
                db_cur.set_balance(message.chat.id, message.from_user.first_name, balance - price)
            else:
                try:
                    deleteOldMessage(message.chat.id, last_messages[message.chat.id])
                except:
                    pass
                message_id = bot.send_message(message.chat.id, 'У вас недостаточно средств для покупки дерева!'
                                                               f'\nНужно: {price} LC'
                                                               f'\nВаш баланс: {balance} LC',
                                              reply_markup=keyboard).message_id
                last_messages[message.chat.id] = message_id
        else:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, 'У вас уже максимальное кол-во деревьев!',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
    else:
        try:
            deleteOldMessage(message.chat.id, last_messages[message.chat.id])
        except:
            pass
        message_id = bot.send_message(message.chat.id, 'Вы отказались от покупки дерева.',
                                      reply_markup=keyboard).message_id
        last_messages[message.chat.id] = message_id


def buy_office(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    text = str(message.text).lower().strip()
    if text == 'да':
        lvl = db_cur.get_office(message.chat.id)
        if lvl < 10:
            price = db_cur.get_office_last_cost(message.chat.id)
            price = price + (price * 0.10)
            balance = db_cur.get_balance(message.chat.id)
            if price == 0:
                price = 50
            if balance >= price:
                try:
                    deleteOldMessage(message.chat.id, last_messages[message.chat.id])
                except:
                    pass
                message_id = bot.send_message(message.chat.id, f'Вы успешно купили ещё один офис за {price} LC!',
                                              reply_markup=keyboard).message_id
                last_messages[message.chat.id] = message_id
                db_cur.update_office(message.chat.id)
                db_cur.update_office_last_cost(message.chat.id, price)
                db_cur.set_balance(message.chat.id, message.from_user.first_name, balance - price)
            else:
                try:
                    deleteOldMessage(message.chat.id, last_messages[message.chat.id])
                except:
                    pass
                message_id = bot.send_message(message.chat.id, 'У вас недостаточно средств для покупки офиса!'
                                                               f'\nНужно: {price} LC'
                                                               f'\nВаш баланс: {balance} LC',
                                              reply_markup=keyboard).message_id
                last_messages[message.chat.id] = message_id
        else:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, 'У вас уже максимальное кол-во офисов!',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
    else:
        try:
            deleteOldMessage(message.chat.id, last_messages[message.chat.id])
        except:
            pass
        message_id = bot.send_message(message.chat.id, 'Вы отказались от покупки офиса.',
                                      reply_markup=keyboard).message_id
        last_messages[message.chat.id] = message_id


def job_do(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    i = 0
    earn = 0.0
    plus = db_cur.get_garden(message.chat.id)
    if plus >= 0.002:
        try:
            deleteOldMessage(message.chat.id, last_messages[message.chat.id])
        except:
            pass
        message_id = bot.send_message(message.chat.id,
                                      f'У вас есть сад, поэтому ваш доход увеличен до {plus} LC за символ!').message_id
        last_messages[message.chat.id] = message_id
    while i < len(str(message.text)):
        earn += plus
        i += 1
    earn = round(earn, 3)
    try:
        deleteOldMessage(message.chat.id, last_messages[message.chat.id])
    except:
        pass
    message_id = bot.send_message(chat_id=message.chat.id,
                                  text=f'В написанном тексте было {len(str(message.text))} символов. Вы '
                                       f'заработали: <b>{earn} LC</b>', parse_mode='HTML',
                                  reply_markup=keyboard).message_id
    last_messages[message.chat.id] = message_id
    balance = round(db_cur.get_balance(message.chat.id) + earn, 3)
    db_cur.set_balance(message.chat.id, message.from_user.first_name, balance)


def play_part1(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    global bet
    text = str(message.text).replace('.', '')
    if text.isdigit():
        bet = float(message.text)
        if bet <= db_cur.get_balance(message.chat.id):
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, text=f'Ваша ставка: {bet} LC. Игра началась!\n'
                                                                'Если вы выиграете - выиграете х3 от своей ставки.\n'
                                                                'Если проиграете - ваша ставка сгорит.\n\n'
                                                                'Правила игры простые. Я загадываю число от 1 до 3. Если отгадаете '
                                                                '- вы выиграли').message_id
            last_messages[message.chat.id] = message_id
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.register_next_step_handler(message, play_part2)
        else:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, text='У вас недостаточно средств!',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
    else:
        try:
            deleteOldMessage(message.chat.id, last_messages[message.chat.id])
        except:
            pass
        message_id = bot.send_message(message.chat.id, text='Ставка должна быть числом!',
                                      reply_markup=keyboard).message_id
        last_messages[message.chat.id] = message_id


def play_part2(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    global bet
    text = str(message.text)
    if text.isdigit():
        number = int(text)
        my_number = random.randint(1, 3)
        if number == my_number:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, f'Вы выиграли в игре, и получаете {bet * 3} LC. Поздравляю!',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
            balance = round(db_cur.get_balance(message.chat.id) + (bet * 3), 3)
        else:
            try:
                deleteOldMessage(message.chat.id, last_messages[message.chat.id])
            except:
                pass
            message_id = bot.send_message(message.chat.id, f'Вы проиграли в игре. С вашего баланса списано {bet} LC. '
                                                           f'Удачи в следующий раз!\n\nЗагаданное число: {my_number}',
                                          reply_markup=keyboard).message_id
            last_messages[message.chat.id] = message_id
            balance = round(db_cur.get_balance(message.chat.id) - bet, 3)
        db_cur.set_balance(message.chat.id, message.from_user.first_name, balance)
    else:
        try:
            deleteOldMessage(message.chat.id, last_messages[message.chat.id])
        except:
            pass
        message_id = bot.send_message(message.chat.id,
                                      'В тексте должно присутствовать только одно число от 1 до 3! Попробуйте ещё '
                                      'раз').message_id
        last_messages[message.chat.id] = message_id
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.register_next_step_handler(message, play_part2)


def repeater(interval, function):
    Timer(interval, repeater, [interval, function]).start()
    function()


def give_passive():
    players = db_cur.cur.execute(f"SELECT * FROM offices;").fetchall()
    for player in players:
        if player[1] > 0:
            player_name = db_cur.get_name(player[0])
            if player_name != False:
                balance = db_cur.get_balance(player[0]) + player[1]
                db_cur.set_balance(player[0], player_name, balance)
                bot.send_message(player[0], f'Вам был начислен пассивный доход в размере {player[1]} LC'
                                            f' за ваши офисы.')


repeater(3600, give_passive)
bot.polling(none_stop=True)
