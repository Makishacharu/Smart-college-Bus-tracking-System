import sqlite3
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from ai_eta import model


DB_PATH = "database/college_bus.db"


def save_bus_location(bus_id, latitude, longitude, status="GPS Active"):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_id INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO bus_locations
        (bus_id, latitude, longitude, updated_at, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        bus_id,
        latitude,
        longitude,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status
    ))

    connection.commit()
    connection.close()

    print("Bus location saved successfully!")


def get_latest_location(bus_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT bus_id, latitude, longitude, status, updated_at
        FROM bus_locations
        WHERE bus_id = ?
        ORDER BY updated_at DESC
        LIMIT 1
    """, (bus_id,))

    location = cursor.fetchone()

    connection.close()

    return location


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


def predict_ai_eta(distance, speed):

    prediction = model.predict([[distance, speed]])

    return round(float(prediction[0]), 2)


if __name__ == "__main__":

    print("==============================")
    print("   BUS GPS + AI ETA SYSTEM")
    print("==============================")

    bus_id = int(input("Enter Bus ID: "))

    latitude = float(input("Enter Current Latitude: "))
    longitude = float(input("Enter Current Longitude: "))

    destination_latitude = float(
        input("Enter Destination Latitude: ")
    )

    destination_longitude = float(
        input("Enter Destination Longitude: ")
    )

    speed = float(
        input("Enter Bus Speed (km/h): ")
    )

    # Save GPS location
    save_bus_location(
        bus_id,
        latitude,
        longitude
    )

    # Get latest GPS location
    latest = get_latest_location(bus_id)

    print("\nLatest Bus Location:")
    print(latest)

    # Calculate distance
    distance = calculate_distance(
        latitude,
        longitude,
        destination_latitude,
        destination_longitude
    )

    # AI ETA prediction
    eta = predict_ai_eta(
        distance,
        speed
    )

    print("\n==============================")
    print("       AI ETA RESULT")
    print("==============================")

    print("Bus ID:", bus_id)
    print("Distance:", distance, "km")
    print("Speed:", speed, "km/h")
    print("AI Predicted ETA:", eta, "minutes")