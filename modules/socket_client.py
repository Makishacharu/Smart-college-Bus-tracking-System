import socket
import json
import time

HOST = "127.0.0.1"
PORT = 5001


def send_bus_location(bus_id, latitude, longitude):

    bus_data = {
        "bus_id": bus_id,
        "latitude": latitude,
        "longitude": longitude,
        "status": "GPS Active"
    }

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect((HOST, PORT))

    print(f"Bus {bus_id} connected to socket server!")

    data = json.dumps(bus_data)

    client.send(data.encode())

    response = client.recv(4096).decode()

    print(f"Bus {bus_id} Server Response:")
    print(response)

    client.close()


if __name__ == "__main__":

    buses = [
        (1, 10.7905, 78.7047),
        (2, 10.8050, 78.7200),
        (3, 10.8150, 78.7300),
        (4, 10.8250, 78.7400),
        (5, 10.8350, 78.7500)
    ]

    for bus_id, latitude, longitude in buses:

        send_bus_location(
            bus_id,
            latitude,
            longitude
        )

        time.sleep(1)

    print("\nAll bus GPS data sent successfully!")