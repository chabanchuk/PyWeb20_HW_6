import psycopg2
from psycopg2 import DatabaseError
import random

def get_random_subject(conn):
    """Повертає випадковий предмет з бази даних."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM Subjects ORDER BY RANDOM() LIMIT 1;")
        subject = cur.fetchone()
        cur.close()
        return subject
    except DatabaseError as e:
        raise e

def get_top_student_for_random_subject(conn):
    """Знайти студента з найвищим середнім балом з випадкового предмета."""
    try:
        cur = conn.cursor()

        # Отримуємо випадковий предмет
        subject = get_random_subject(conn)
        subject_id = subject[0]
        subject_name = subject[1]

        # Запит на обчислення середнього балу для кожного студента з випадкового предмета
        query = """
        SELECT s.id, s.name, ROUND(AVG(g.grade), 2) as avg_grade
        FROM Students s
        JOIN Grades g ON s.id = g.student_id
        WHERE g.subject_id = %s
        GROUP BY s.id, s.name
        ORDER BY avg_grade DESC
        LIMIT 1;
        """
        
        cur.execute(query, (subject_id,))
        top_student = cur.fetchone()

        # Виведення результатів
        if top_student:
            print(f"Студент з найвищим середнім балом з випадкового предмета ({subject_name}):")
            print(f"ID: {top_student[0]}, Ім'я: {top_student[1]}, Середній бал: {top_student[2]}")
        else:
            print(f"Студентів з предмета ({subject_name}) не знайдено.")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_top_student_for_random_subject(conn)
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        conn.close()

