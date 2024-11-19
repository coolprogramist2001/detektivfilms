import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import detektivfilmov
bot=telebot.TeleBot("")
@bot.message_handler(commands=["start"])
def start (message):
    keyboard= InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Помощь",callback_data="help"))
    bot.send_message(message.chat.id,"Привет с тобой Детектив Фильмов и я помогу тебе найти любой фильм!",reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def help (message):
    keyboard= InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Фильмы",callback_data="Films"))
    bot.send_message(message.chat.id,"Нажимай кнопку ниже и смотри крутые фильмы!",reply_markup=keyboard)


@bot.message_handler(commands=["films"])
def films (message):
    keyboard= InlineKeyboardMarkup()
    buttons=[InlineKeyboardButton(str(index+1),callback_data=f"film:{index}")
             for index, film in enumerate(detektivfilmov.films)
                                  ]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id ,"Нажимай кнопку ниже и смотри крутые фильмы!",reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call:True)
def button(call):
    if call.data == "help":
        keyboard= InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Фильмы",callback_data="Films"))
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,"Нажимай кнопку ниже и смотри крутые фильмы!",reply_markup=keyboard)
    elif call.data == "Films":
        keyboard= InlineKeyboardMarkup()
        buttons=[InlineKeyboardButton(str(index+1),callback_data=f"film:{index}")
        for index, film in enumerate(detektivfilmov.films)
                                  ]
        keyboard.add(*buttons)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id ,"Нажимай кнопку ниже и смотри крутые фильмы!",reply_markup=keyboard)
    elif call.data.startswith("film:"):
        index=int(call.data.split(":")[1])
        name=list(detektivfilmov.films.keys())[index]
        info=detektivfilmov.films[name]
        foto=info.get("Фото","")
        response = f"{name} ({info['Год выпуска']})\nРежисер: {info['Режисер']}\nЖанр: {info['Жанр']}"
        if foto:
            bot.send_photo(call.message.chat.id, foto,caption=response)
        else:
            bot.send_message(call.message.chat.id, response)
@bot.message_handler(commands=['addmovie'])
def  addmovie(message):
    bot.reply_to(message,'Введите название фильма.')
    bot.register_next_step_handler(message,adddirector)
def adddirector(message):
    userdata={}
    userdata["Name"]=message.text
    bot.reply_to(message,'Введите режиссёра фильма.')
    bot.register_next_step_handler(message,addyear,userdata)
def addyear(message,userdata):
    userdata["director"]=message.text
    bot.reply_to(message,'Введите год выпуска фильма.')
    bot.register_next_step_handler(message,addjanr,userdata)
def addjanr(message,userdata):
    userdata["year"]=message.text
    bot.reply_to(message,'Введите жанр фильма.')
    bot.register_next_step_handler(message,addphoto,userdata)
def addphoto(message,userdata):
    userdata["janr"]=message.text
    bot.reply_to(message,'Введите ссылку на фото фильма.')
    bot.register_next_step_handler(message,save,userdata)
def save(message,userdata):
    detektivfilmov.films[userdata['Name']]={
        "Режисер":userdata["director"],
        "Год выпуска":userdata["year"],
        "Жанр":userdata["janr"],
        "Фото":message.text
    }
    bot.reply_to(message,"Фильм добавлен.")



































bot.polling()