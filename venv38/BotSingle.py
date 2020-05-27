# Добавить исключения

import logging
import json
from venv38.my_utils import *
from venv38.params import *
from venv38.tags import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# class Form(StatesGroup):
#     person_define = State()
#     user = State()
#     moderator = State()


user_commands_available = ("/info", "/help", "/add", "/change", "/auth")
mod_commands_available = ("/info", "/help", "/list10", "/one_by_one", "/logout")


# def auth(func):
#     async def wrapper(message):
#         if message['from']['id'] !=




logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN, proxy=TG_PROXY)
storage = MemoryStorage()
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def who_are_you(message: types.Message):
    if is_moderator(message.from_user.id):
        storage.data['is_moderator'] = True
        return SendMessage(message.chat.id,
                           get_phrase_from_res(JsonTags.WELCOME_MODERATOR, message.from_user.language_code))

    return SendMessage(message.chat.id, get_phrase_from_res(JsonTags.WELCOME, message.from_user.language_code))


@dp.message_handler(commands=['auth'])
async def auth_req(message: types.Message):
    if storage.data['is_moderator']:
        print("auth command: already moderator")
        return SendMessage(message.chat.id,
                           get_phrase_from_res(JsonTags.AUTH_YOU_ALREADY_MOD, message.from_user.language_code))

    storage.data['is_auth_requested'] = True
    return SendMessage(message.chat.id, get_phrase_from_res(JsonTags.AUTH_WELCOME, message.from_user.language_code))


@dp.message_handler(regexp="[?]\w+::\w+::\w+$")
async def auth(message: types.Message):
    if not storage.data['is_auth_requested']:
        print("auth regex handler: not requested")
        return SendMessage(message.chat.id,
                           get_phrase_from_res(JsonTags.AUTH_NOT_REQUESTED, message.from_user.language_code))

    storage.data['is_auth_requested'] = False
    print("auth regex handler: requested")
    if login_moderator(message.text, message.from_user.id):
        print("auth regex handler: login_moderator is True")
        storage.data['is_moderator'] = True
        return SendMessage(message.chat.id,
                           get_phrase_from_res(JsonTags.AUTH_SUCCESS_MODERATOR, message.from_user.language_code))

    return SendMessage(message.chat.id,
                       get_phrase_from_res(JsonTags.AUTH_FAIL_MODERATOR, message.from_user.language_code))


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    return SendMessage(message.chat.id,
                       get_phrase_from_res(JsonTags.INFO, message.from_user.language_code))


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    if storage.data['is_moderator']:
        return SendMessage(message.chat.id,
                           get_phrase_from_res(JsonTags.HELP_MODERATOR, message.from_user.language_code))

    return SendMessage(message.chat.id,
                       get_phrase_from_res(JsonTags.HELP_USER, message.from_user.language_code))


@dp.message_handler(commands=['logout'])
async def moderator_logout(message: types.Message):
    if not storage.data['is_moderator']:
        return SendMessage(message.chat.id,
                           get_phrase_from_res(JsonTags.LOGOUT_FAIL, message.from_user.language_code))

    storage.data['is_moderator'] = False
    return SendMessage(message.chat.id,
                       get_phrase_from_res(JsonTags.LOGOUT_SUCCESS, message.from_user.language_code))

#
# @dp.message_handler(regexp='^Где$')
# async def point_place(message: types.Message):
#     with open("data/img/.png", "rb") as photo:
#         await message.reply_photo(photo, caption="Here!")


@dp.message_handler()
async def echo(message: types.Message):
    # await message.reply("Извините, не понимаю запроса")
    reply_message = get_phrase_from_res(JsonTags.STRING_DONT_GET_IT, message.from_user.language_code)
    # await message.reply(f"{reply_message}")
    return SendMessage(message.chat.id, reply_message)


if __name__ == "__main__":
    storage.data['is_auth_requested'] = False
    storage.data['is_moderator'] = False
    # Вычислять язык пользователя для всех хендлеров
    # Выдавать сгенерированную таблицу с расписаним курсов
    executor.start_polling(dp, skip_updates=True)

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
#     cursor.execute("CREATE TABLE I NOT EXIST places (title VARCHAR(255), address VARCHAR(255))")
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
