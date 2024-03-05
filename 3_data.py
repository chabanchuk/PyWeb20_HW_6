import logging
import psycopg2
from psycopg2 import DatabaseError
from faker import Faker

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fill_tables(conn, fake):
    """Наповнює таблиці тестовими даними."""
    try:
        with conn.cursor() as cur:
            fill_groups(cur, fake)
            fill_teachers(cur, fake)
            fill_subjects(cur, fake)
            fill_students(cur, fake)
            fill_grades(cur, fake)
            
        conn.commit()
        logger.info("Дані успішно додані до таблиць.")
    except DatabaseError as e:
        logger.error(f"Помилка при наповненні таблиць: {e}")
        conn.rollback()

def fill_groups(cur, fake):
    """Наповнення таблиці Groups."""
    try:
        data = [(f"група-{i}",) for i in range(1, 4)]
        cur.executemany("INSERT INTO Groups (name) VALUES (%s);", data)
        logger.info("Дані успішно додані до таблиці Groups.")
    except DatabaseError as e:
        logger.error(f"Помилка при додаванні даних до таблиці Groups: {e}")

def fill_students(cur, fake):
    """Наповнення таблиці Students."""
    try:
        data = [(fake.name(), fake.random_int(min=1, max=3)) for _ in range(40)]
        cur.executemany("INSERT INTO Students (name, group_id) VALUES (%s, %s);", data)
        logger.info("Дані успішно додані до таблиці Students.")
    except DatabaseError as e:
        logger.error(f"Помилка при додаванні даних до таблиці Students: {e}")

def fill_teachers(cur, fake):
    """Наповнення таблиці Teachers."""
    try:
        data = [(fake.name(),) for _ in range(4)]
        cur.executemany("INSERT INTO Teachers (name) VALUES (%s);", data)
        logger.info("Дані успішно додані до таблиці Teachers.")
    except DatabaseError as e:
        logger.error(f"Помилка при додаванні даних до таблиці Teachers: {e}")

def fill_subjects(cur, fake):
    """Наповнення таблиці Subjects."""
    try:
        teachers_count = 4  # Кількість вчителів
        subjects = ['математика', 'фізика', 'географія', 'історія', 'література', 'музика']
        data = [(subject, fake.random_int(1, teachers_count)) for subject in subjects]
        cur.executemany("INSERT INTO Subjects (name, teacher_id) VALUES (%s, %s);", data)
        logger.info("Дані успішно додані до таблиці Subjects.")
    except DatabaseError as e:
        logger.error(f"Помилка при додаванні даних до таблиці Subjects: {e}")

def fill_grades(cur, fake):
    """Наповнення таблиці Grades."""
    try:
        students_count = 40  # Кількість студентів
        subjects_count = 6  # Кількість предметів
        data = [(fake.random_int(1, students_count), fake.random_int(1, subjects_count), fake.random_int(4, 12), fake.date_time_this_year()) for _ in range(students_count * subjects_count)]
        cur.executemany("INSERT INTO Grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s);", data)
        logger.info("Дані успішно додані до таблиці Grades.")
    except DatabaseError as e:
        logger.error(f"Помилка при додаванні даних до таблиці Grades: {e}")


if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        fill_tables(conn, Faker('uk_UA'))
    except DatabaseError as e:
        logger.error(f"Помилка бази даних: {e}")
    finally:
        conn.close()
