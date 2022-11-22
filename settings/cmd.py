import os
import psycopg2
from loguru import logger
from config import host, user, password, db_name
from getpass import getpass

logger.info("Welcome to admin panel!")


try:
    """Connect to database"""
    database = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    database.autocommit = True
    cursor = database.cursor()

    user_want = int(input("""What do you want to do?
        \n1)Ban user
        \n2)UnBan user
        \n3)Look banned users
        \n4)Create Injection yourself\n"""))
    
    if user_want == 1:
        user_id = input("Enter id:\n")
        cursor.execute(f"insert into banned (userid) values ('{user_id}')")
        logger.info("Done!")

    elif user_want == 2:
        user_id = input("Enter id:\n")
        cursor.execute(f"delete from banned where userid = '{user_id}'")
        logger.info("Done!")

    elif user_want == 3:
        cursor.execute("select * from banned")
        row = cursor.fetchall()
        for data in row:
            print(data)

    elif user_want == 4:
        user_password = getpass("So It's danger step please enter your password:\n")
        set_password = os.getenv("sqlpass")

        if set_password == user_password:
            injection = input("Input What ever you want:\n")
        else:
            logger.error("Passwords don't much!")




except Exception as _ex:
    logger.error(f"Database Error: {_ex}")


finally:
    cursor.close()
    database.close()
