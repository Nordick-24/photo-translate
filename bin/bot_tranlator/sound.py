from loguru import logger
from gtts import gTTS


@logger.catch()
def tell_text(date, bot, user_lang, message) -> None:
    """Tell text, save it to file and send it"""
    read = gTTS(text=date, lang=user_lang, slow=False)
    read.save("sound.mp3")

    bot.send_message(message.chat.id, "It's gonna read like:")
    sound = open('sound.mp3', 'rb')
    bot.send_audio(message.chat.id, sound)
