# from telegram import Bot
# from telegram import Update
# from telegram.ext import CallbackContext
# from telegram.ext import Updater
# from telegram.ext import MessageHandler
# from telegram.ext import Filters
# import mysql.connector

# from telegram import *
# from telegram.ext import *
# from telegram.ext import Updater, CommandHandler

# Добавить исключения

import logging
import json
from aiogram import Bot, Dispatcher, executor, types

TG_TOKEN = "1250829139:AAF0oTZCy34C8oAGX8mu_Zexpe_69Cqd3R0"
TG_PROXY = "socks5://45.91.93.166:1080"


# def auth(func):
#     async def wrapper(message):
#         if message['from']['id'] !=

class JsonTags:
    STRING_HERE_POINT = "here_point"
    STRING_DONT_GET_IT = "dont_get_it"
    INTERLANG_INFO_TAG = "info"


logging.basicConfig(level=logging.INFO)
# bot = Bot(token=TG_TOKEN)
bot = Bot(token=TG_TOKEN, proxy=TG_PROXY)
dp = Dispatcher(bot)


# def init_database():
#     mysql.connector.Connect()
#     database = mysql.connector.connect(
#         host="localhost",
#         user="user",
#         passwd="passwd"
#     )
#
#     cursor = database.cursor()
#     cursor.execute("CREATE DATABASE IF NOT EXIST places_database")
#     cursor.execute("CREATE TABLE IF NOT EXIST places (title VARCHAR(255), address VARCHAR(255))")
#     cursor.execute("INSERT INTO TABLE places (title, address) VALUES (%s, %s)", ("moyahata", "moyaddress"))
#
#     return cursor


# def message_handler(bot: Bot, update: Updater):
#     user = update.effective_user
#     if user:
#         name = user.first_name
#     else:
#         # string array of random words
#         name = "Anonimous"

# text = update.effective_message.text
# reply_text = f'Hello, {name}!\n\n{text}'
# bot.send_message(update.effective_message.chat_id, reply_text)


# cursor = init_database()
# cursor.execute("SELECT * FROM places")
# print(cursor.fetchall())
# bot.send_message(bot.get_chat().id, cursor.fetchall()[0])

def get_phrase_from_res(tag, user_lang_code):
    # log needed
    print(f"[get_phrase_from_res: tag {tag}, user_lang: {user_lang_code}]")

    if user_lang_code not in user_codes_avail:
        return ""
    with open("data/inter_lang.json", "r") as json_file:
        data = json.load(json_file)
        try:
            return data['phrases'][tag][user_lang_code]
        except:
            return data['phrases'][tag]['en']


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! My name is Local Places Bot")


@dp.message_handler(regexp='^Где$')
async def point_place(message: types.Message):
    with open("data/img/.png", "rb") as photo:
        await message.reply_photo(photo, caption="Here!")


@dp.message_handler()
async def echo(message: types.Message):
    # await message.reply("Извините, не понимаю запроса")
    reply_message = get_phrase_from_res(JSON_TAGS.STRING_DONT_GET_IT, message.from_user.language_code)
    await message.reply(f"{reply_message}")


if __name__ == "__main__":
    # Вычислять язык пользователя для всех хендлеров
    # Выдавать сгенерированную таблицу с расписаним курсов
    executor.start_polling(dp, skip_updates=True)
