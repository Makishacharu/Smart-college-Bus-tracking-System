import sqlite3


DB_PATH = "database/college_bus.db"


def create_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # ==================================================
    # STUDENTS TABLE
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_id INTEGER UNIQUE,
        name TEXT NOT NULL,
        roll_number TEXT UNIQUE NOT NULL,
        bus_id INTEGER,
        parent_name TEXT,
        parent_phone TEXT
    )
    """)

    # ==================================================
    # ADD COLLEGE ID TO EXISTING DATABASE
    # ==================================================

    try:
        cursor.execute("""F
            ALTER TABLE students
            ADD COLUMN college_id INTEGER
            ALTER TABLE bus_locations
            ADD COLOUMN status TEXT DEFAULT 'GPS Active'
        """)
    except sqlite3.OperationalError:
        pass

    # Existing students-ku college ID assign pannum
    cursor.execute("""
        UPDATE students
        SET college_id = student_id
        WHERE college_id IS NULL
    """)

    # ==================================================
    # BUSES TABLE
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buses (
        bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_number TEXT NOT NULL,
        driver_name TEXT NOT NULL,
        route TEXT NOT NULL
    )
    """)

    # BUS GPS LOCATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bus_locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    try:
        cursor.execute(""" ALTER TABLE bus_locations
        ADD COLUMN status TEXT DEFAULT 'GPS ACTIVE'
    """)
    except Exception:
       pass

    # ==================================================
    # ATTENDANCE TABLE
    # ==================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
    )
    """)

    # ==================================================
    # SAVE DATABASE
    # ==================================================

    connection.commit()
    connection.close()

    print("Database created successfully!")


# ==================================================
# RUN PROGRAM
# ==================================================

if __name__ == "__main__":
    create_database()