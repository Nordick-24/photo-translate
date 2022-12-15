from loguru import logger


@logger.catch()
def read_language(message, bot) -> str:
    """Return user languages"""
    try:
        if message.text == 'Greek':
            user_lang = "ell"

        elif message.text == 'Turkish':
            user_lang = "tur"

        elif message.text == 'Russian':
            user_lang = "rus"

        elif message.text == 'English':
            user_lang = "eng"

        return user_lang

    except UnboundLocalError:
        bot.send_message(message.chat.id, "Sorry, it's unknow language!")


@logger.catch()
def read_sound(message) -> str:
    if message.text == 'English':
        sound_language="en"

    elif message.text == 'Greek':
        sound_language="el"

    elif message.text == 'Russian':
        sound_language="ru"

    elif message.text == 'Turkish':
        sound_language="tr"

    return sound_language


