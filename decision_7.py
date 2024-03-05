import psycopg2
from psycopg2 import DatabaseError

def get_top_students(conn):
    """Знайти оцінки студентів у окремій групі з певного предмета.."""
    try:
        cur = conn.cursor()

        # Запит - оцінки студентів у окремій групі з певного предмета.
        query = """
        SELECT Groups.name, Subjects.name, Students.name, Grades.grade
		FROM Students
		JOIN Grades ON Students.id = Grades.student_id
		JOIN Subjects ON Grades.subject_id = Subjects.id
		JOIN Groups ON Students.group_id = Groups.id
		WHERE Groups.name = (SELECT name FROM Groups ORDER BY RANDOM() LIMIT 1)
		AND Subjects.name = (SELECT name FROM Subjects ORDER BY RANDOM() LIMIT 1);
        """
        
        cur.execute(query)
        top_students = cur.fetchall()

        # Виведення результатів
        print("оцінки студентів у окремій групі з певного предмета:")
        for student in top_students:
            print(f"Група: {student[0]}, Предмет: {student[1]}, Ім'я: {student[2]}, Оцінка: {student[3]}")

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
        if conn is not None:
            conn.close()
