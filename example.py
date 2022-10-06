from time import sleep
import gspread
import telebot
from telebot import types

#bot = telebot.TeleBot("5246846512:AAFUwoY6s-RKwyaMRdDk88SU6oJpp0csW7Y")
bot = telebot.TeleBot("5553272907:AAGS3WWDCjRpw9J08h6-7n1TzMLSWYsjA_4")

def parse_google_sheet():
    gc = gspread.oauth(
        credentials_filename=r"C:\Users\NASTYA\AppData\Roaming\gspread\credentials.json"
        )
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1XJdOEXyi24SkWr45N7QZgfF0AhxjHWpB46tRbvt8s3I/edit#gid=490512256")

    return sh.sheet1.get_all_values()


@bot.message_handler(commands=['start'])
def start(message):
    global sent_message
    markup = types.InlineKeyboardMarkup(row_width=1)
    start_button = types.InlineKeyboardButton(text="Проверить себя", callback_data="start_checking")
    information_button = types.InlineKeyboardButton(text="О боте", callback_data="information")
    markup.add(start_button, information_button)
    #sent_mes = bot.send_message(message.chat.id, "some text", reply_markup=markup)
    sent_message = bot.send_message(message.chat.id, "some text", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback:
                            callback.data in ("start_checking", "information"))
def reply_to_start_command(callback):
    data = callback.data
    if data == "start_checking":
        # сначала запускаем функцию с парсингом
        global words, keyboard, know_btn, dont_know_btn, stop_btn, sent_message, counter, ind
        counter, ind = 0, 0
        words = sum(parse_google_sheet(), [])
        #words = sum(words, [])
        keyboard = types.InlineKeyboardMarkup()
        #word_btn = types.InlineKeyboardButton(text=f"words[0]", callback_data="current_word")
        know_btn = types.InlineKeyboardButton(text="Знаю", callback_data="know")
        dont_know_btn = types.InlineKeyboardButton(text="Не знаю", callback_data="don't_know")
        stop_btn = types.InlineKeyboardButton(text="Преждевременный конец", callback_data="stop")
        #keyboard.add(word_btn)
        keyboard.add(know_btn, dont_know_btn)
        keyboard.add(stop_btn)
        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.id, 
                                text=words[ind], reply_markup=keyboard)

    elif data == "information":
        # выводим информацию о боте
        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.id,
            text="There will be information about the bot.")

@bot.message_handler(commands=['help'])
def help(message):
    # вызывается функция, которая показывает информацию о боте
    pass


@bot.callback_query_handler(func=lambda callback:
                            callback.data in ("know", "don't_know", "stop")
                            )
def game(callback):
    data = callback.data
    if data in ("know", "don't_know"):
        global keyboard, know_btn, dont_know_btn, stop_btn, sent_message, counter, words, ind
        if ind == len(words) - 1:
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.id,
            text=f"Ваш результат {counter} из 1000")
        ind += 1
        if data == 'know':
            counter += 1
        #word_btn = types.InlineKeyboardButton(text=f"words[ind]", callback_data="current_word")
        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.id,
        text=words[ind], reply_markup=keyboard)
    
    elif data == "stop":
        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.id,
        text=f"Ваш результат {counter} из 1000")


while True:
    try:
        bot.polling(non_stop=True)
    except:
        sleep(15)

# bot.polling()
