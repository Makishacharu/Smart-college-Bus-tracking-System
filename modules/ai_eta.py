from sklearn.linear_model import LinearRegression
import numpy as np


# ==============================
# TRAINING DATA
# Distance (km), Speed (km/h)
# ==============================

X = np.array([
    [2, 20],
    [5, 20],
    [8, 25],
    [10, 25],
    [12, 30],
    [15, 30],
    [18, 35],
    [20, 35],
    [25, 40],
    [30, 40]
])

# Actual travel time in minutes
y = np.array([
    6,
    15,
    19,
    24,
    24,
    30,
    31,
    34,
    38,
    45
])


# ==============================
# TRAIN AI MODEL
# ==============================

model = LinearRegression()

model.fit(X, y)


# ==============================
# TEST PREDICTION
# ==============================

distance = 12
speed = 30

prediction = model.predict([
    [distance, speed]
])


eta = round(float(prediction[0]), 2)


print("===================================")
print("       AI ETA PREDICTION")
print("===================================")

print("Distance :", distance, "km")
print("Speed    :", speed, "km/h")
print("AI ETA   :", eta, "minutes")

print("===================================")