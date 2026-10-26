import sqlite3

connection = sqlite3.connect("database/college_bus.db")
cursor = connection.cursor()

try:
    cursor.execute("""
        ALTER TABLE notifications
        ADD COLUMN notification_type TEXT DEFAULT 'Parent'
    """)

    connection.commit()
    print("Column added successfully!")

except sqlite3.OperationalError as error:
    print("Database message:", error)

connection.close()