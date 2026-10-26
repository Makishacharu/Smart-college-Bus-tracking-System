import multiprocessing
import socket
import json
import time


HOST = "127.0.0.1"
PORT = 5001


def track_bus(bus_id, latitude, longitude):

    print(f"🚌 Bus {bus_id} Tracking Started")

    bus_data = {
        "bus_id": bus_id,
        "latitude": latitude,
        "longitude": longitude,
        "status": "GPS Active"
    }

    try:

        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client.connect((HOST, PORT))

        data = json.dumps(bus_data)

        client.send(data.encode())

        response = client.recv(4096).decode()

        print(f"Bus {bus_id}: {response}")

        client.close()

    except Exception as error:

        print(
            f"❌ Bus {bus_id} connection error:",
            error
        )


if __name__ == "__main__":

    buses = [
        (1, 10.7905, 78.7047),
        (2, 10.8005, 78.7147),
        (3, 10.8105, 78.7247),
        (4, 10.8205, 78.7347),
        (5, 10.8305, 78.7447)
    ]

    processes = []

    for bus in buses:

        process = multiprocessing.Process(
            target=track_bus,
            args=bus
        )

        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("\n===================================")
    print("ALL BUSES PROCESSED SUCCESSFULLY")
    print("===================================")