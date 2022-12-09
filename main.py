from bin import bot_transalator, bot_support
from threading import Thread
from loguru import logger


@logger.catch()
def main():
    th1 = Thread(target=bot_support.bot.polling)
    th2 = Thread(target=bot_transalator.bot.polling)

    th2.start()
    logger.info("Bot Translator is Working")
    th1.start()
    logger.info("Bot Support is Working")


if __name__ == '__main__':
    main()
    logger.warning("All processes run, but if you have any errors , maybe program not working!")
