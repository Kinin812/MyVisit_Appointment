import os

import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(token=os.getenv('API_TOKEN'))
chat_id = os.getenv('CHAT_ID')


def send_message(message):
    bot.send_message(chat_id, message)


if __name__ == '__main__':
    send_message('kuku')
