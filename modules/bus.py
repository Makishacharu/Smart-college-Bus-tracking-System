import sqlite3

DB_PATH = "database/college_bus.db"I

i
def add_bus():
    bus_number = input("Enter bus number: ")
    driver_name = input("Enter driver name: ")
    route = input("Enter route: ")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO buses (bus_number, driver_name, route)
        VALUES (?, ?, ?)
    """, (bus_number, driver_name, route))

    connection.commit()
    connection.close()

    print("\nBus added successfully!")


def view_buses():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()

    print("\n========== BUS LIST ==========")

    if not buses:
        print("No buses found.")
    else:
        for bus in buses:
            print(bus)

    connection.close()