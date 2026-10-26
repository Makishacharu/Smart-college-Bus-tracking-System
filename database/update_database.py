import sqlite3

DB_PATH = "database/college_bus.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

try:
    cursor.execute("""
        ALTER TABLE bus_locations
        ADD COLUMN distance REAL
    """)
    print("Distance column added!")

except sqlite3.OperationalError:
    print("Distance column already exists.")


try:
    cursor.execute("""
        ALTER TABLE bus_locations
        ADD COLUMN eta REAL
    """)
    print("ETA column added!")

except sqlite3.OperationalError:
    print("ETA column already exists.")


connection.commit()
connection.close()

print("\nDatabase update completed!")