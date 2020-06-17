import logging
from venv38.my_utils import *
from venv38.params import *
from venv38.tags import *
from venv38.DatabaseManager import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

REGEX_AUTH_CHECKER = "[?]\w+::\w+::\w+$"


class Form(StatesGroup):
    info = State()
    description = State()
    place_name = State()
    question = State()
    answer = State()
    correct_answer = State()


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN, proxy=TG_PROXY)
# bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start", state='*')
async def who_are_you(message: types.Message):
    if is_moderator(message.from_user.id):
        storage.data['is_moderator'] = True
        reply = get_phrase_from_res(JsonTags.WELCOME_MODERATOR, message.from_user.language_code)
    else:
        reply = get_phrase_from_res(JsonTags.WELCOME, message.from_user.language_code)

    await Form.info.set()
    return SendMessage(message.chat.id, reply)


@dp.message_handler(commands=['auth'], state=Form.info)
async def auth_req(message: types.Message):
    if storage.data['is_moderator']:
        print("auth command: already moderator")
        reply = get_phrase_from_res(JsonTags.AUTH_YOU_ALREADY_MOD, message.from_user.language_code)
    else:
        storage.data['is_auth_requested'] = True
        reply = get_phrase_from_res(JsonTags.AUTH_WELCOME, message.from_user.language_code)

    return SendMessage(message.chat.id, reply)


@dp.message_handler(regexp=REGEX_AUTH_CHECKER, state=Form.info)
async def auth(message: types.Message):
    if not storage.data['is_auth_requested']:
        print("auth regex handler: not requested")
        reply = get_phrase_from_res(JsonTags.AUTH_NOT_REQUESTED, message.from_user.language_code)
    else:
        storage.data['is_auth_requested'] = False
        print("auth regex handler: requested")

        if login_moderator(message.text, message.from_user.id):
            print("auth regex handler: login_moderator is True")
            storage.data['is_moderator'] = True
            reply = get_phrase_from_res(JsonTags.AUTH_SUCCESS_MODERATOR, message.from_user.language_code)
        else:
            reply = get_phrase_from_res(JsonTags.AUTH_FAIL_MODERATOR, message.from_user.language_code)

    return SendMessage(message.chat.id, reply)


@dp.message_handler(commands=['info'], state=Form.info)
async def info(message: types.Message):
    return SendMessage(message.chat.id,
                       get_phrase_from_res(JsonTags.INFO, message.from_user.language_code))


@dp.message_handler(commands=['help'], state=Form.info)
async def help_message(message: types.Message):
    if storage.data['is_moderator']:
        reply = get_phrase_from_res(JsonTags.HELP_MODERATOR, message.from_user.language_code)
    else:
        reply = get_phrase_from_res(JsonTags.HELP_USER, message.from_user.language_code)

    return SendMessage(message.chat.id, reply)


@dp.message_handler(commands=['logout'], state=Form.info)
async def moderator_logout(message: types.Message):
    if not storage.data['is_moderator']:
        reply = get_phrase_from_res(JsonTags.LOGOUT_FAIL, message.from_user.language_code)
    else:
        storage.data['is_moderator'] = False
        reply = get_phrase_from_res(JsonTags.LOGOUT_SUCCESS, message.from_user.language_code)

    return SendMessage(message.chat.id, reply)


@dp.message_handler(commands=['cancel'], state=Form.description)
async def add_place1(message: types.Message):
    print("Total cancel. Changes discarded")
    reply = get_phrase_from_res(JsonTags.ADD_CANCEL, message.from_user.language_code)

    await Form.info.set()
    return SendMessage(message.chat.id, reply)


# Для модератора также доступно
@dp.message_handler(commands=['add', 'cancel'], state='*')
async def add_place2(message: types.Message):
    print("Cancel retry")

    await Form.description.set()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_DESCRIPTION, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.description, content_types=types.ContentTypes.TEXT)
async def add_place3(message: types.Message):
    print("Description: " + message.text)

    storage.data["description"] = message.text

    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_PLACE, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.place_name, content_types=types.ContentTypes.TEXT)
async def add_place4(message: types.Message):
    print("Place name: " + message.text)

    storage.data["place"] = message.text
    storage.data["question_list"] = []

    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_QUESTION, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(commands=["commit_questions"], state=Form.question)
async def add_place5(message: types.Message):
    print("Questions committed")

    req = UserRequest(message.from_user.id,
                      storage.data["description"],
                      storage.data["place"],
                      storage.data["question_list"])
    text_storing(req)

    await Form.info.set()

    response = get_phrase_from_res(JsonTags.ADD_RESULT, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.question, content_types=types.ContentTypes.TEXT)
async def add_place6(message: types.Message):
    print("Question: " + message.text)

    storage.data["question"] = []
    storage.data["question"].append(message.text)

    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_ANSWER, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(commands=["commit_answers"], state=Form.answer)
async def add_place7(message: types.Message):
    await Form.next()

    response = get_phrase_from_res(JsonTags.ADD_CORRECT_ANSWER, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.correct_answer)
async def add_place8(message: types.Message):
    storage.data["question_list"].append(storage.data["question"])
    await Form.question.set()

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_QUESTION, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(state=Form.answer, content_types=types.ContentTypes.TEXT)
async def add_place9(message: types.Message):
    print("Answer: " + message.text)

    storage.data["question"].append(message.text)

    response = get_phrase_from_res(JsonTags.ADD_QUESTIONS_ANSWER_AGAIN, message.from_user.language_code)
    return SendMessage(message.chat.id, response)


@dp.message_handler(commands=['fetch_one'], state=Form.info)
async def fetch_one(message: types.Message):
    if not storage.data['is_moderator']:
        reply = get_phrase_from_res(JsonTags.DATA_NOT_MODERATOR, message.from_user.language_code)
        return SendMessage(message.chat.id, reply)

    result = ""
    writ_was_began = False

    lines = open("data/new_data.txt").readlines()
    lines_to_delete = 0

    for line in lines:
        print("LINE: " + line)
        if "User id" in line and not writ_was_began:
            writ_was_began = True

        lines_to_delete += 1
        result += line

        if (line == "" or line == "\n") and writ_was_began:
            break

    with open("data/new_data.txt", "w") as file:
        file.writelines(lines[lines_to_delete:-1])

    if result == "":
        result = get_phrase_from_res(JsonTags.DATA_IS_EMPTY, message.from_user.language_code)

    return SendMessage(message.chat.id, result)


@dp.message_handler(state=Form.info)
async def echo(message: types.Message):
    reply_message = get_phrase_from_res(JsonTags.STRING_DONT_GET_IT, message.from_user.language_code)
    return SendMessage(message.chat.id, reply_message)


if __name__ == "__main__":
    storage.data['is_auth_requested'] = False
    storage.data['is_moderator'] = False
    executor.start_polling(dp, skip_updates=True)
