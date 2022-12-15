import os
import sys
import telebot
import psycopg2
from PIL import Image
from loguru import logger
from configs.db_config import host, user, password, db_name
from telebot import types
from pytesseract import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip


have_to_delete_old_translate = False
driver = webdriver.Firefox()
driver.get("https://translate.google.com/")
close_cookie_message = driver.find_element(By.XPATH, """
/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button
""")
time.sleep(4)  # If browser don't load all needest, he died

close_cookie_message.click()

translate_input = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea
        """)
select_language_input = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[5]/button/div[3]
        """)
select_language_input.click()

find_language = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[2]/input
        """)
find_language.send_keys('Russian')
select_russian = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[4]/div/div[1]
        """)
select_russian.click()

del close_cookie_message, select_language_input, find_language, select_russian


@logger.catch()
def translate(text: str, bot, message) -> None:
    """Translate input text"""
    global have_to_delete_old_translate

    if have_to_delete_old_translate is False:
        translate_input.send_keys(text)
        time.sleep(10)
        copy_answer = driver.find_element(By.XPATH, """
                /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[8]/div/div[4]/div[2]/span[2]/button/div[3]
                """)
        copy_answer.click()
        answer = pyperclip.paste()
        bot.send_message(message.chat.id, answer)
        have_to_delete_old_translate = True

    else:
        delete_old_translation = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/div[1]/div/div/span/button/div[3]
        """)
        delete_old_translation.click()
        translate_input.send_keys(text)
        time.sleep(10)
        copy_answer = driver.find_element(By.XPATH, """
        /html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[8]/div/div[4]/div[2]/span[2]/button/div[3]
        """)
        copy_answer.click()
        answer = pyperclip.paste()
        bot.send_message(message.chat.id, answer)


api_token = os.getenv("TELEGRAM_KEY")
bot = telebot.TeleBot(api_token)
logger.add("log_file,json",
        format="{time} {level} {message}",
        level="INFO", rotation="1 week",
        compression="zip", serialize=True)


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

try:
    from bin.bot_tranlator import ban_system
    from bin.bot_tranlator import sound
    from bin.bot_tranlator import select_language

except ImportError:
    pass
try:
    try:
        @logger.catch()
        def get_user_photo(message) -> None:
            """Download Photo with the text from user."""
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)

            with open("image.jpg", "wb") as newfile:
                newfile.write(downloaded_file)

        @logger.catch()
        def read_text_from_image(message) -> None:
            """Select Language and Read The text from user image."""
            cursor.execute(f"select * from banned where userid = '{message.from_user.id}'")
            row_main = cursor.fetchall()
            len_main = len(row_main)

            if len_main == 0:
                try:
                    data = pytesseract.image_to_string(Image.open('image.jpg'), lang=select_language.read_language(message, bot))

                    if (not(data and data.strip())):
                        logger.info(f"Someone send empty foto, ID:{message.from_user.id}")
                        data = "Program Can't find any text!"
                        bot.send_message(message.chat.id, data)

                    bot.send_message(message.chat.id, "Processing...It's 10 seconds or less", parse_mode='html')
                    sound.tell_text(data, bot, select_language.read_sound(message), message)
                    translate(data, bot, message)

                except UnboundLocalError:
                    bot.send_message(message.chat.id, "Sorry, somethings wrong and system decided ban you!")
                    logger.warning(f"User with id {message.from_user.id} try kill programm!")
                    ban_system.ban_user(message.from_user.id)
                    logger.warning("Because he try use bag number 1 str 97")


        @bot.message_handler(commands=['start'])
        @logger.catch()
        def start(message) -> None:
            """When user type start command start this thing."""
            cursor.execute(f"select userid from banned where userid = '{message.from_user.id}'")
            ban_row = cursor.fetchall()
            lenq = len(ban_row)

            if lenq == 0:
                start_message = "What's up and welcome to TelePyTransl , just send me image"
                bot.send_message(message.chat.id, start_message, parse_mode='html')

                @bot.message_handler(content_types=['photo'])
                @logger.catch()
                def photo(message):
                    """Download Photo from user"""
                    get_user_photo(message)

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

                    greekbutton = types.KeyboardButton('Greek')
                    englishbutton = types.KeyboardButton('English')
                    russianbutton = types.KeyboardButton('Russian')
                    turkishbutton = types.KeyboardButton('Turkish')
                    markup.add(greekbutton, englishbutton, turkishbutton, russianbutton)
                    bot.send_message(message.chat.id, "select language:", parse_mode='html', reply_markup=markup)

                    @bot.message_handler()
                    @logger.catch()
                    def get_user_text(message):
                        read_text_from_image(message)

            elif lenq != 0:
                bot.send_message(message.chat.id, """You are banned!,
                 TO unbun you send message /unblock
                  or write to helper bot t.me/TelePyTranslHelperBot.
                  """, parse_mode='html')
                logger.info(f"Banned user with id {message.from_user.id} send some message.")

        @bot.message_handler(commands=['rules'])
        @logger.catch()
        def rules(message) -> None:
            rules_message = """One big one rule don't try hack or crash programm or you have banned."""
            bot.send_message(message.chat.id, rules_message, parse_mode='html')


        @bot.message_handler(commands=['unblock'])
        @logger.catch()
        def unblock(message) -> None:
            ban_system.captcha_function(message, bot)

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
