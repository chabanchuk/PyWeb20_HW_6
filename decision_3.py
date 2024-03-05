import psycopg2
from psycopg2 import DatabaseError

def get_random_subject_id(conn):
    """Повертає випадковий ідентифікатор предмету з бази даних."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM Subjects ORDER BY RANDOM() LIMIT 1;")
        subject_id, subject_name = cur.fetchone()
        cur.close()
        return subject_id, subject_name
    except DatabaseError as e:
        raise e

def get_group_name_by_id(conn, group_id):
    """Повертає назву групи за її ідентифікатором."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM Groups WHERE id = %s;", (group_id,))
        group_name = cur.fetchone()[0]
        cur.close()
        return group_name
    except DatabaseError as e:
        raise e

def get_average_grade_by_group(conn):
    """Знайти середній бал у групах з випадкового предмета."""
    try:
        cur = conn.cursor()

        # Отримуємо випадковий ідентифікатор та назву предмету
        subject_id, subject_name = get_random_subject_id(conn)

        # Запит на обчислення середнього балу для кожної групи з випадкового предмету
        query = """
        SELECT st.group_id, ROUND(AVG(g.grade), 2) as avg_grade
        FROM Grades g
        JOIN Students st ON g.student_id = st.id
        WHERE g.subject_id = %s
        GROUP BY st.group_id
        """
        
        cur.execute(query, (subject_id,))
        average_grades = cur.fetchall()

        # Виведення результатів
        print(f"Середній бал у групах з випадкового предмету ({subject_name}):")
        for group_id, avg_grade in average_grades:
            group_name = get_group_name_by_id(conn, group_id)
            print(f"Група: {group_name}, Середній бал: {avg_grade}")

        cur.close()
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(dbname='homework_6', user='postgres', password='567234', host='localhost')
        get_average_grade_by_group(conn)
    except DatabaseError as e:
        print(f"Помилка бази даних: {e}")
    finally:
        conn.close()

