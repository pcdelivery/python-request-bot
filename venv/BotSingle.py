from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
# import mysql.connector

TG_TOKEN = "1250829139:AAG8s2rrNLckMPBWERLPXsg03Y4ew5g9rCs"


# def init_database():
    # mysql.connector.Connect()
    # database = mysql.connector.connect(
    #     host="localhost",
    #     user="user",
    #     passwd="passwd"
    # )

    # cursor = database.cursor()
    # cursor.execute("CREATE DATABASE IF NOT EXIST places_database")
    # cursor.execute("CREATE TABLE IF NOT EXIST places (title VARCHAR(255), address VARCHAR(255))")
    # cursor.execute("INSERT INTO TABLE places (title, address) VALUES (%s, %s)", ("moyahata", "moyaddress"))

    # return cursor


def message_handler(bot: Bot, update: Updater):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        # string array of random words
        name = "Anonimous"

    text = update.effective_message.text
    reply_text = f'Hello, {name}!\n\n{text}'
    bot.send_message(update.effective_message.chat_id, reply_text)


def main():
    print("init")
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot, use_context=True, base_url="https://telegg.ru/orig/bot")
    handler = MessageHandler(Filters.all, message_handler)

    # context = CallbackContext(updater.dispatcher)
    # handler.collect_additional_context(context, updater, updater.dispatcher, null)

    updater.dispatcher.add_handler(handler)


    # cursor = init_database()
    # cursor.execute("SELECT * FROM places")
    # print(cursor.fetchall())
    # bot.send_message(bot.get_chat().id, cursor.fetchall()[0])

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()