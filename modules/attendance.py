import sqlite3

DB_PATH = "database/college_bus.db"


def mark_attendance():
    student_id = input("Enter student ID: ")
    date = input("Enter date (YYYY-MM-DD): ")
    status = input("Enter status (Present/Absent): ")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO attendance
            (student_id, date, status)
            VALUES (?, ?, ?)
        """, (student_id, date, status))

        connection.commit()
        print("\nAttendance marked successfully!")

    except sqlite3.Error as error:
        print("\nError:", error)

    finally:
        connection.close()


def view_attendance():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT * FROM attendance
        """)

        records = cursor.fetchall()

        print("\n========== ATTENDANCE ==========")

        if not records:
            print("No attendance records found.")
        else:
            for record in records:
                print(record)

    except sqlite3.Error as error:
        print("\nError:", error)

    finally:
        connection.close()


def attendance_menu():
    while True:
        print("\n========== ATTENDANCE MANAGEMENT ==========")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            mark_attendance()

        elif choice == "2":
            view_attendance()

        elif choice == "3":
            break

        else:
            print("Invalid choice!")