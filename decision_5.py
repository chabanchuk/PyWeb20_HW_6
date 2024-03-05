import psycopg2
from psycopg2 import DatabaseError

def get_random_teacher_id(conn):
    """Повертає випадковий ідентифікатор викладача з бази даних."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM Teachers ORDER BY RANDOM() LIMIT 1;")
        teacher_id = cur.fetchone()[0]
        cur.close()
        return teacher_id
    except DatabaseError as e:
        raise e

def get_courses_by_teacher(conn):
    """Знайти курси, які читає випадковий викладач."""
    try:
        cur = conn.cursor()

        # Отримуємо випадковий ідентифікатор викладача
        teacher_id = get_random_teacher_id(conn)

        # Запит на знаходження курсів, які читає випадковий викладач
        query = """
        SELECT t.name, sb.name
        FROM Subjects sb
        JOIN Teachers t ON sb.teacher_id = t.id
        WHERE t.id = %s
        """
        
        cur.execute(query, (teacher_id,))
        courses = cur.fetchall()

        # Виведення результатів
        if courses:
            print(f"Курси, які читає випадковий викладач '{courses[0][0]}':")
            for course in courses:
                print(course[1])
        else:
            print(f"Випадковий викладач з ID '{teacher_id}' не читає жодного курсу.")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_courses_by_teacher(conn)
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        if conn is not None:
            conn.close()

