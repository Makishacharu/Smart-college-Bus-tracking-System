from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371

    lat1 = radians(lat1)
    lat2 = radians(lat2)
s
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c

    return round(distance, 2)


def calculate_eta(distance_km, speed_kmph):

    if speed_kmph <= 0:
        return None

    time_hours = distance_km / speed_kmph

    time_minutes = time_hours * 60

    return round(time_minutes, 2)


if __name__ == "__main__":

    distance = calculate_distance(
        10.7905,
        78.7047,
        10.8050,
        78.7200
    )

    eta = calculate_eta(distance, 30)

    print("Distance:", distance, "km")
    print("ETA:", eta, "minutes")