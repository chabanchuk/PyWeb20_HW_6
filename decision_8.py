import psycopg2
from psycopg2 import DatabaseError

def get_average_grade_for_teacher(conn):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    try:
        cur = conn.cursor()

        # Запит на отримання ID випадкового викладача
        cur.execute("SELECT id FROM Teachers ORDER BY RANDOM() LIMIT 1;")
        teacher_id = cur.fetchone()[0]

        # Запит на обчислення середнього балу, який ставить певний викладач зі своїх предметів
        query = """
            SELECT Teachers.name, AVG(Grades.grade)
		FROM Grades
		JOIN Subjects ON Grades.subject_id = Subjects.id
		JOIN Teachers ON Subjects.teacher_id = Teachers.id
		WHERE Teachers.id = %s
		GROUP BY Teachers.name;
        """
        
        cur.execute(query, (teacher_id,))
        result = cur.fetchone()

        # Виведення результатів
        if result:
            print(f"Середній бал, який ставить викладач '{result[0]}': {result[1]}")
        else:
            print(f"Викладача з ID '{teacher_id}' не знайдено.")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_average_grade_for_teacher(conn)  # Отримуємо середній бал для випадкового викладача
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        conn.close()

