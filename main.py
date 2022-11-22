from bin import bot_transalator
from bin import bot_support
from threading import *
from loguru import logger
import os


try:
    th1 = Thread(target = bot_support.bot.polling)
    th2 = Thread(target = bot_transalator.bot.polling)

    th2.start()
    logger.info("Bot Translator is Working")
    th1.start()
    logger.info("Bot Support is Working")

finally:
    os.remove('captcha.png')
