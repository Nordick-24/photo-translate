from bin import bot_transalator
from bin import bot_support
from threading import Thread
from loguru import logger
import os


if __name__ == '__main__':
    th1 = Thread(target=bot_support.bot.polling)
    th2 = Thread(target=bot_transalator.bot.polling)

    th2.start()
    logger.info("Bot Translator is Working")
    th1.start()
    logger.info("Bot Support is Working")

