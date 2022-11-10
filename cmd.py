import psycopg2
from loguru import logger
from config import host, user, password, db_name

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

    user_want = int(input("""What do you want to do?\n1)Ban user\n2)UnBan user\n3)Look banned users\n"""))
    
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


except Exception as _ex:
    logger.error(f"Database Error: {_ex}")


finally:
    cursor.close()
    database.close()
