import socket
import json
import sqlite3
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from ai_eta import model


HOST = "127.0.0.1"
PORT = 5001

DB_PATH = "database/college_bus.db"

DESTINATION_LAT = 10.8050
DESTINATION_LON = 78.7200

BUS_SPEED = 30


def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(earth_radius * c, 2)


def save_bus_data(bus_data):

    latitude = bus_data["latitude"]
    longitude = bus_data["longitude"]

    # Calculate distance
    distance = calculate_distance(
        latitude,
        longitude,
        DESTINATION_LAT,
        DESTINATION_LON
    )

    # AI ETA prediction
    prediction = model.predict(
        [[distance, BUS_SPEED]]
    )

    eta = round(float(prediction[0]), 2)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create table if needed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_id INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT,
            updated_at TEXT NOT NULL,
            distance REAL,
            eta REAL
        )
    """)

    cursor.execute("""
        INSERT INTO bus_locations
        (bus_id, latitude, longitude, status,
         updated_at, distance, eta)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        bus_data["bus_id"],
        latitude,
        longitude,
        bus_data["status"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        distance,
        eta
    ))

    connection.commit()
    connection.close()

    print("Bus data saved to database!")
    print("Distance:", distance, "km")
    print("AI ETA:", eta, "minutes")


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen(5)


print("===================================")
print("       BUS SOCKET SERVER")
print("===================================")
print(f"Server running on {HOST}:{PORT}")
print("Waiting for bus connection...")


while True:

    connection, address = server.accept()

    print("\nBus connected:", address)

    try:

        data = connection.recv(4096).decode()

        bus_data = json.loads(data)

        print("\nReceived Bus Data:")
        print("Bus ID:", bus_data["bus_id"])
        print("Latitude:", bus_data["latitude"])
        print("Longitude:", bus_data["longitude"])
        print("Status:", bus_data["status"])

        save_bus_data(bus_data)

        connection.send(
            "GPS + AI ETA saved successfully!".encode()
        )

    except json.JSONDecodeError:

        print("Invalid JSON data received!")

        connection.send(
            "Invalid bus data!".encode()
        )

    except Exception as error:

        print("Error:", error)

        connection.send(
            "Server error!".encode()
        )

    finally:

        connection.close()