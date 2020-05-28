# Добавить исключения

import logging
import json
from venv38.my_utils import *
from venv38.params import *
from venv38.tags import *
from venv38.DatabaseManager import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from typing import Tuple


class Form(StatesGroup):
    info = State()
    description = State()
    place_name = State()
    question = State()
    answer = State()
    correct_answer = State()


user_commands_available = ("/info", "/help", "/add", "/change", "/auth")
mod_commands_available = ("/info", "/help", "/list10", "/one_by_one", "/logout")

QUESTIONS_MAX = 8
ANSWERS_PER_QUESTION_MAX = 25

# def auth(func):
#     async def wrapper(message):
#         if message['from']['id'] !=


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN, proxy=TG_PROXY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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
async def info(message: types.Message):
    return SendMessage(message.chat.id,
                       get_phrase_from_res(JsonTags.INFO, message.from_user.language_code))


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
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


# Для модератора также доступно
@dp.message_handler(commands=['add', 'cancel'], state='*')
async def add_place1(message: types.Message):
    print("Add init")

    await Form.description.set()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_DESCRIPTION, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.description, content_types=types.ContentTypes.TEXT)
async def add_place2(message: types.Message, state: FSMContext):
    print("Description: " + message.text)

    storage.data["description"] = message.text

    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_PLACE, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.place_name, content_types=types.ContentTypes.TEXT)
async def add_place3(message: types.Message, state: FSMContext):
    print("Place name: " + message.text)

    storage.data["place"] = message.text
    storage.data["question_list"] = []

    # storage.data["que_ans"] = [1][1]
    # storage.data["que_index"] = 0

    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_QUESTION, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(commands=["commit_questions"], state=Form.question)
async def add_place7(message: types.Message, state: FSMContext):
    print("Questions committed: ")

    req = UserRequest(message.from_user.id, storage.data["description"], storage.data["place"], storage.data["question_list"])
    text_storing(req)

    await Form.info.set()

    response = get_phrase_from_res(JsonTags.ADD_RESULT, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.question, content_types=types.ContentTypes.TEXT)
async def add_place4(message: types.Message, state: FSMContext):
    print("Question: " + message.text)

    storage.data["question"] = []
    storage.data["question"].append(message.text)


    # matrix = storage.data["que_ans"]
    # cur_que = storage.data["que_index"]
    # storage.data["ans_index"] = 1
    #
    # matrix[cur_que][0] = message.text

    # print("Question size: " + str(storage.data["que_index"]))

    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_ANSWER, message.from_user.language_code)
    return SendMessage(message.chat.id, response)





@dp.message_handler(commands=["commit_answers"], state=Form.answer)
async def add_place6(message: types.Message, state: FSMContext):
    # print("COMMIT ANSWERS: " + str(storage.data["question"]))

    # storage.data["question_list"].append(storage.data["question"])
    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_CORRECT_ANSWER, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.correct_answer)
async def add_place8(message: types.Message, state: FSMContext):
    storage.data["question_list"].append(storage.data["question"])
    await Form.question.set()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_QUESTION, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.answer, content_types=types.ContentTypes.TEXT)
async def add_place5(message: types.Message, state: FSMContext):
    print("Answer: " + message.text)

    storage.data["question"].append(message.text)

    # matrix = storage.data["que_ans"]
    # cur_que = storage.data["que_index"]
    # cur_ans = storage.data["ans_index"]
    #
    # matrix[cur_que][cur_ans] = message.text
    # storage.data["ans_index"] += 1

    # print("Answer2: " + matrix[cur_que][cur_ans])
    # print("Answers size: " + str(storage.data["ans_index"]))

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_ANSWER_AGAIN, message.from_user.language_code)
    return SendMessage(message.chat.id, response)



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
