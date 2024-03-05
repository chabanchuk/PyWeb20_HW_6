import logging
import psycopg2
from psycopg2 import DatabaseError

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables(conn):
    """Створює таблиці у базі даних 'homework_6'."""
    try:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50)
        );

        CREATE TABLE IF NOT EXISTS Students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            group_id INTEGER REFERENCES Groups(id)
        );

        CREATE TABLE IF NOT EXISTS Teachers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS Subjects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            teacher_id INTEGER REFERENCES Teachers(id)
        );

        CREATE TABLE IF NOT EXISTS Grades (
            id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES Students(id),
            subject_id INTEGER REFERENCES Subjects(id),
            grade INTEGER,
            date TIMESTAMP
        );
        """)
        conn.commit()
        logging.info("Таблиці успішно створені.")
    except DatabaseError as e:
        logging.error(f"Помилка при створенні таблиць: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        create_tables(conn)
    except DatabaseError as e:
        logger.error(f"Помилка бази даних: {e}")
    finally:
        conn.close()
