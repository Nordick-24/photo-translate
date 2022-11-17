import os
import random
import string
import telebot
import psycopg2
from PIL import Image
from loguru import logger
from config import host, user, password, db_name 
from translate import Translator
from telebot import types
from pytesseract import pytesseract
from captcha.image import ImageCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import asyncio

def translate(text):
    driver = webdriver.Firefox()
    driver.get("https://translate.google.com/")
    element = driver.find_element(By.XPATH, """/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button""")
    time.sleep(2.5)
    element.click()

    search_bar = driver.find_element(By.XPATH, """/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea""")
    russian_transl = driver.find_element(By.XPATH, """/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[5]/button/div[3]""")
    russian_transl.click()

    search_button = driver.find_element(By.XPATH, """/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[2]/input""")
    search_button.send_keys('Russian')

    russian_buttin = driver.find_element(By.XPATH, """/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[4]/div/div[1]""")
    russian_buttin.click()

    search_bar.send_keys(text)


api_token = os.getenv("TELEGRAM_KEY")
bot = telebot.TeleBot(api_token)
logger.add("info.log", format="{time} {level} {message}", level="INFO") #Create a log file
"""If we start this thing on server , programm can died , and we need log"""

try:
    """Connect to Database"""
    database = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    database.autocommit = True
    cursor = database.cursor()

except Exception as _ex:
    logger.error(f"Detect Database Error: {_ex}")


def ban_user(userid):
    cursor.execute(f"insert into banned (userid) values ('{userid}')")
    logger.info(f"User {userid} is banned.")

def unban_user(userid):
    cursor.execute(f"delete from banned where userid = '{userid}'")
    logger.info(f"User {userid} UnBanned.")

def captcha_function(message, bot):
    captcha_sett = ImageCaptcha(width = 280, height = 90)
    letters = string.ascii_lowercase
    captcha_text =  ''.join(random.choice(letters) for i in range(5))

    captcha = captcha_sett.generate(captcha_text)
    captcha_sett.write(captcha_text, 'captcha.png')

    capcha_image = open("captcha.png", "rb")
    bot.send_photo(message.chat.id, capcha_image)

    @bot.message_handler()
    def user_text(message):
        if message.text == captcha_text:
            unban_user(message.from_user.id)

try:
    try:
        logger.info("Started Successfully!")

        def get_user_photo(message):
            """Download Photo with the text from user."""
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)

            with open("image.jpg", "wb") as newfile:
                newfile.write(downloaded_file)
#Here Function finish.

        def main_function(message):
            """Select Language and Read The text from user image."""
            global database
            global cursor

            cursor.execute(f"select * from banned where userid = '{message.from_user.id}'")
            row_main = cursor.fetchall()
            len_main = len(row_main)

            if len_main == 0:
                try:
                    if message.text == 'Greek':
                        user_lang = "ell"

                    elif message.text == 'Russian':
                        user_lang = "rus"

                    elif message.text == 'English':
                        user_lang = "eng"

                    data = pytesseract.image_to_string(Image.open('image.jpg'), lang=user_lang)

                    if (not(data and data.strip())):
                        logger.info(f"Someone send empty foto, ID:{message.from_user.id}")
                        data = "Program Can't find any text!"
                        
                    bot.send_message(message.chat.id, data, parse_mode='html')
                    bot.send_message(message.chat.id, "Processing...", parse_mode='html')

                    translate(data)

                    bot.send_message(message.chat.id, data, parse_mode='html')

                except UnboundLocalError:
                    """Bug Number. Ban because if use it many time use it it can crash system because, processing need many resorses! """
                    bot.send_message(message.chat.id, "It's rule number 1 , it's not allowed, you are banned!")
                    logger.info(f"User with id {message.from_user.id} try kill programm!")
                    ban_user(message.from_user.id)
                    logger.info("Because he try use bag number 1 str 97")


#Here Function Finished

        @bot.message_handler(commands=['start'])
        def start(message):
            """When user type start command start this thing."""

            global database
            global cursor

            ban_row = cursor.execute(f"select userid from banned where userid = '{message.from_user.id}'")
            ban_rowd = cursor.fetchall()
            lenq = len(ban_rowd)
        
            if lenq == 0: 
                start_message = "What's up and welcome to TelePyTransl , just send me image"
                bot.send_message(message.chat.id, start_message, parse_mode='html')

                @bot.message_handler(content_types=['photo'])
                def photo(message):
                    """Download Photo from user"""
                    get_user_photo(message)

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

                    greekbutton = types.KeyboardButton('Greek')
                    englishbutton = types.KeyboardButton('English')
                    russianbutton = types.KeyboardButton('Russian')
                    markup.add(greekbutton, englishbutton, russianbutton)
                    bot.send_message(message.chat.id, "select language:", parse_mode='html', reply_markup=markup)

                    @bot.message_handler()
                    def get_user_text(message):
                        main_function(message)

            elif lenq != 0:
                bot.send_message(message.chat.id, "You are banned!", parse_mode='html')
                logger.info(f"Banned user with id {message.from_user.id} send some message.")

        @bot.message_handler(commands=['rules'])
        def rules(message):
            rules_message = """One big one rule don't try hack or crash programm or you have banned."""
            bot.send_message(message.chat.id, rules_message, parse_mode='html')


        @bot.message_handler(commands=['unblock'])
        def unblock(message):
            captcha_function(message, bot)
                        

        #bot.polling(none_stop=True) #Start bot

    finally:
        try:

            os.remove("image.jpg")

        except FileNotFoundError:
            pass
        
        logger.info("Log File writed.")

except Exception as _ex:
    logger.error(f"An unforeseen error: {_ex}")

finally:
    try:
        os.remove("captcha.png")
        os.remove("image.jpg")
        database.close()
        cursor.close()
    except NameError:
        pass
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
