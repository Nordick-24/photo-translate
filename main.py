from threading import Thread
from loguru import logger
import sys
import time


@logger.catch()
def main() -> None:
    from bin.bot_tranlator import bot_transalator
    from bin.bot_support import bot_support

    start_time = time.monotonic()


    th1 = Thread(target=bot_support.bot.polling)
    th2 = Thread(target=bot_transalator.bot.polling)

    th2.start()
    logger.info(f"Bot Translator is Working(started in {start_time})")
    th1.start()
    logger.info(f"Bot Support is Working(started in {start_time})")


if __name__ == '__main__' and sys.argv[1] == "run":
    main()
    logger.warning("All processes run, but if you have any errors , maybe program not working!")

elif __name__ == '__main__' and sys.argv[1] == "test":
    if sys.argv[2] == "-translator" or sys.argv[2] == "--translator":
        from bin.bot_tranlator import bot_transalator
        bot_transalator.bot.polling()

    elif sys.argv[2] == "-support" or sys.argv[2] == '--support':
        from bin.bot_support import bot_support
        bot_support.bot.polling()
