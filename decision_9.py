import psycopg2
from psycopg2 import DatabaseError

def get_student_courses(conn):
    """Retrieve the subjects attended by a random student."""
    try:
        cur = conn.cursor()

        # Вибираємо випадкового студента
        cur.execute("SELECT id, name FROM Students ORDER BY RANDOM() LIMIT 1;")
        student_id, student_name = cur.fetchone()

        query = """
        SELECT DISTINCT s.name
        FROM Subjects s
        JOIN Grades ON s.id = Grades.subject_id
        WHERE Grades.student_id = %s;
        """

        cur.execute(query, (student_id,))
        student_courses = cur.fetchall()

        # Виведення результатів
        if student_courses:
            print(f"Список унікальних предметів, які відвідує студент {student_name}:")
            for subject in student_courses:
                print(subject[0])
        else:
            print(f"Студент {student_name} не відвідує жодного предмета.")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_student_courses(conn)
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        conn.close()