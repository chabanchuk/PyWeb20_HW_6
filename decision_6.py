import psycopg2
from psycopg2 import DatabaseError

def get_students_in_group(conn):
    """Знайти список студентів у певній групі."""
    try:
        cur = conn.cursor()

        # Знайти список студентів у випадковій групі
        query = """
SELECT groups.name, students.name
FROM students
JOIN groups ON students.group_id = groups.id
GROUP BY groups.name, students.name
ORDER BY RANDOM();
        """
        
        cur.execute(query)
        students = cur.fetchall()

        # Виведення результатів
        if students:
            print(f"Студенти у випадковій групі '{students[0][0]}':")
            for student in students:
                print(f"Ім'я: {student[1]}")
        else:
            print("Не вдалося знайти студентів у випадковій групі.")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        
        get_students_in_group(conn)  # Отримуємо студентів у випадковій групі
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        if conn is not None:
            conn.close()

