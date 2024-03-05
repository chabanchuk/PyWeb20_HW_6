import psycopg2
from psycopg2 import DatabaseError

def get_average_grade_overall(conn):
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    try:
        cur = conn.cursor()

        # Запит на обчислення середнього балу по всій таблиці оцінок
        query = """
        SELECT ROUND(AVG(grade), 2) as avg_grade
        FROM Grades
        """
        
        cur.execute(query)
        average_grade = cur.fetchone()[0]

        # Виведення результатів
        print(f"Середній бал на потоці: {average_grade}")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_average_grade_overall(conn)
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        conn.close()
