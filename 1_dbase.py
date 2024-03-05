import logging
import psycopg2
from psycopg2 import DatabaseError, extensions

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_homework_database():
    """Створює базу даних 'homework_6', якщо вона не існує."""
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='567234', host='localhost')
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datname = 'homework_6';")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE homework_6;")
            logging.info("База даних 'homework_6' успішно створена.")
        else:
            logging.info("База даних 'homework_6' вже існує.")
        cur.close()
        conn.close()
    except DatabaseError as e:
        logging.error(f"Помилка при створенні/перевірці бази даних 'homework_6': {e}")

if __name__ == "__main__":
    create_homework_database()