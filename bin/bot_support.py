import telebot
import os


api_token = os.getenv("TELEGRAM_SUPP_TOKEN")
bot = telebot.TeleBot(api_token)

def get_user_photo(message, bot):
    fileId = message.photo[-1].file_id
    file_info = bot.get_file(fileId)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("reports/image.jpg", "wb") as save_photo:
        save_photo.write(downloaded_file)

    bot.send_message(message.chat.id, "Ok, after some time we check it!")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello,it's support bot, if you was banned from some bag send screenshot of this thing.")

    @bot.message_handler(content_types=['photo'])
    def user_screenshot(message):
        get_user_photo(message, bot)


