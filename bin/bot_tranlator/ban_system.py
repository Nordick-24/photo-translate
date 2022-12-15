import telebot
import psycopg2
from loguru import logger
from captcha.image import ImageCaptcha
import os
from bin.bot_tranlator.bot_transalator import database, cursor
import string
import random


@logger.catch()
def ban_user(userid: str) -> None:
    cursor.execute(f"insert into banned (userid) values ('{userid}')")
    logger.info(f"User {userid} is banned.")


@logger.catch()
def unban_user(userid: str) -> None:
    cursor.execute(f"delete from banned where userid = '{userid}'")
    return logger.info(f"User {userid} UnBanned.")


@logger.catch()
def captcha_function(message, bot) -> None:
    """Make and send captcha photo for banned user"""
    captcha_sett = ImageCaptcha(width=280, height=90)
    letters = string.ascii_lowercase
    captcha_text = ''.join(random.choice(letters) for long in range(5))

    captcha_sett.generate(captcha_text)
    captcha_sett.write(captcha_text, 'captcha.png')

    with open("captcha.png", "rb") as capcha_image:
        bot.send_photo(message.chat.id, capcha_image)

    del captcha_sett, letters, captcha_text

    return logger.info("captcha function used")

    @bot.message_handler()
    @logger.catch()
    def user_text(message):
        if message.text == captcha_text:
            unban_user(message.from_user.id)
