import sqlite3

DB_PATH = "database/college_bus.db"


def add_student():
    name = input("Enter student name: ")
    roll_number = input("Enter roll number: ")
    bus_id = input("Enter bus ID: ")
    parent_name = input("Enter parent name: ")
    parent_phone = input("Enter parent phone: ")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students
            (name, roll_number, bus_id, parent_name, parent_phone)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, roll_number, bus_id, parent_name, parent_phone)
        )

        connection.commit()
        print("\nStudent added successfully!")

    except sqlite3.IntegrityError:
        print("\nRoll number already exists!")

    connection.close()


def view_students():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n========== STUDENT LIST ==========")

    if not students:
        print("No students found.")
    else:
        for student in students:
            print(student)

    connection.close()


if __name__ == "__main__":
    add_student()
    view_students()