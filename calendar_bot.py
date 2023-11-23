import telebot
from telebot import types

token = "6331100840:AAH6gCMo2wjv3se6QGXLLVw3jupVM5BaAJQ"
bot = telebot.TeleBot(token)


class Ivent:
    '''Класс события, которое планирует человек. Содержит в себе:
    дату начала события, дату конца события, время начала события, время окончания события, описание события, номер события'''

    def __init__(self, start_date, end_date, start_time, end_time, description, number):
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.number = number


class Person:
    '''Класс пользователя. Содержит в себе id пользователя, счетчик, на единицу меньший числа событий и массив событий'''

    def __init__(self, id, ivents):
        self.id = id
        self.cntivents = -1
        self.ivents = ivents


People = {}  ## тут храним пользовтаелей
flag = False  ## переменная для обработки


@bot.message_handler(commands=['start'])
def start(message):
    keyboard1 = telebot.types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Добавить событие", callback_data="Добавить событие")
    btn2 = types.InlineKeyboardButton(text="Посмотреть события", callback_data="Посмотреть события")
    btn3 = types.InlineKeyboardButton(text="Удалить событие", callback_data="Удалить событие")
    btn4 = types.InlineKeyboardButton(text="Удалить пользователя", callback_data="Удалить пользователя")
    greeting = "Привет! Я бот - календарь, который поможет тебе не забыть о своих планах"
    bot.send_message(message.chat.id, greeting, reply_markup=keyboard1)
    People[message.chat.id] = Person(message.chat.id, [])  ## регистрация автоматическая при старте


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_from_start(callback):
    if callback.data == "Добавить событие":
        add_ivent(callback.message)
    elif callback.data == "Посмотреть события":
        show_ivents(callback.message)
    elif callback.data == "Удалить событие":
        delete_ivent(callback.message)
    elif callback.data == "Удалить пользователя":
        delete_person(callback.message)


@bot.message_handler(commands=['delete_ivent'])
def delete_ivent(message):
    show_ivents(message)
    sent = bot.send_message(message.chat.id, "Введите одно число: номер события, которое хотите удалить.")
    bot.register_next_step_handler(sent, deliting_ivent)

def deliting_ivent(message):
    for x in People[message.chat.id].ivents:
        if int(x.number) == int(message.text):
            People[message.chat.id].ivents.remove(x)
        elif int(x.number) > int(message.text):
            x.number = str(int(x.number) - 1)
    People[message.chat.id].cntivents -= 1
    bot.send_message(message.chat.id, "Событие удалено")

@bot.message_handler(commands=['delete_person'])
def delete_person(message):
    keyboard2 = telebot.types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Да", callback_data="Да")
    button2 = types.InlineKeyboardButton(text="Нет", callback_data="Нет")
    keyboard2.add(button1, button2)
    bot.send_message(message.chat.id, "Вы уверены, что хотите удалить аккаунт?", reply_markup=keyboard2)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_from_delete_person(callback):
    if callback.data == "Да":
        del People[callback.message.chat.id]
        bot.send_message(callback.message.chat.id, 'Ваш аккаунт был удалён. Для повторной регистрации введите /start')
    elif callback.data == "Нет":
        bot.send_message(callback.message.chat.id, 'Ваш аккаунт был удалён. Шучу)')


@bot.message_handler(commands=['add_ivent'])
def add_ivent(message):
    sent = bot.send_message(message.chat.id, "Введите описание события")
    bot.register_next_step_handler(sent, add_description)


def add_description(message):
    People[message.chat.id].ivents.append(Ivent('', '', '', '', '', ''))
    People[message.chat.id].cntivents += 1
    People[message.chat.id].ivents[People[message.chat.id].cntivents].number = People[message.chat.id].cntivents + 1
    People[message.chat.id].ivents[People[message.chat.id].cntivents].description = message.text
    sent = bot.send_message(message.chat.id, "Когда состоится ваше событие? Введите дату начала в формате ДД.ММ.ГГГГ")
    bot.register_next_step_handler(sent, add_start_date)


def add_start_date(message):
    People[message.chat.id].ivents[People[message.chat.id].cntivents].start_date = message.text
    sent = bot.send_message(message.chat.id,
                            "Во сколько состоится ваше событие? Введите время начала в формате ЧЧ:ММ (по Мск)")
    bot.register_next_step_handler(sent, add_start_time)


def add_start_time(message):
    People[message.chat.id].ivents[People[message.chat.id].cntivents].start_time = message.text
    sent = bot.send_message(message.chat.id,
                            "Когда заканчивается ваше событие? Введите дату окончания в формате ДД.ММ.ГГГГ")
    bot.register_next_step_handler(sent, add_end_date)


def add_end_date(message):
    People[message.chat.id].ivents[People[message.chat.id].cntivents].end_date = message.text
    sent = bot.send_message(message.chat.id,
                            "Во сколько завершается ваше событие? Введите время окончания в формате ЧЧ:ММ (по Мск)")
    bot.register_next_step_handler(sent, add_end_time)


def add_end_time(message):
    People[message.chat.id].ivents[People[message.chat.id].cntivents].end_time = message.text
    bot.send_message(message.chat.id, "Ваше событие записано")


@bot.message_handler(commands=['show_ivents'])
def show_ivents(message):
    for x in People[message.chat.id].ivents:
        bot.send_message(message.chat.id,
                         f" номер события: {x.number}. Дата начала:{x.start_date}. Дата конца: {x.end_date}. Время начала: {x.start_time}. Время конца: {x.end_time}."
                         f"запланированно событие: {x.description}")


@bot.message_handler(func=lambda message: True)  ## обработка обычного текста
def get_user_text(message):
    bot.send_message(message.chat.id, "Список доступных комманд:")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(non_stop=True)
