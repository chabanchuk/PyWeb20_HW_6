import psycopg2
from psycopg2 import DatabaseError

def get_top_students(conn):
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    try:
        cur = conn.cursor()

        # Запит на обчислення середнього балу для кожного студента
        query = """
        SELECT s.id, s.name, ROUND(AVG(g.grade), 2) as avg_grade
        FROM Students s
        JOIN Grades g ON s.id = g.student_id
        GROUP BY s.id, s.name
        ORDER BY avg_grade DESC
        LIMIT 5;
        """
        
        cur.execute(query)
        top_students = cur.fetchall()

        # Виведення результатів
        print("Топ 5 студентів із найбільшим середнім балом:")
        for student in top_students:
            print(f"ID: {student[0]}, Ім'я: {student[1]}, Середній бал: {student[2]}")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_top_students(conn)
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        conn.close()
