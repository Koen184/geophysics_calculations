import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import openpyxl
import math

from matplotlib.patches import Circle, Rectangle


# FUNCTIONS - equations used in main integral equation

def distance(x, y, z):
    distance_value = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    return distance_value


def equation(x, y, z):
    distance_value = distance(x, y, z)
    result = -x * np.log(y + distance_value) - y * np.log(x + distance_value) + z * np.arctan(
        (x * y) / (z * distance_value))
    return result


# LOAD FILE

file_path = 'Geofizyka.xlsx'
df_data = pd.read_excel(file_path, sheet_name='Data')
df_NMT = pd.read_excel(file_path, sheet_name='NMT')

# DATA

X_data = df_data['EG'].tolist()
Y_data = df_data['NG'].tolist()
Z_data = df_data['H'].tolist()


# NMT DATA

X_nmt = df_NMT['NCE'].tolist()
Y_nmt = df_NMT['NCN'].tolist()
Z_nmt = df_NMT['Hnorm'].tolist()

# CONSTANTS

p_density = 2670  # kg / m * m * m
G = 6.67430 * (10 ** (-11))
cuboid_size = 1000  # m

# OTHERS

number_of_points = len(X_data)
number_of_grids = len(X_nmt)
integral_results = []

# NUMERIC INTEGRATION

for i in range(number_of_points):
    integral_point = 0

    for j in range(number_of_grids):
        distance_check = np.sqrt((X_nmt[j] - X_data[i]) ** 2 + (Y_nmt[j] - Y_data[i]) ** 2 + (Z_nmt[j] - Z_data[i]) ** 2)

        if distance_check <= 1200:
            X_1 = abs(X_nmt[j] - X_data[i]) - cuboid_size / 2
            X_2 = abs(X_nmt[j] - X_data[i]) + cuboid_size / 2
            Y_1 = abs(Y_nmt[j] - Y_data[i]) - cuboid_size / 2
            Y_2 = abs(Y_nmt[j] - Y_data[i]) + cuboid_size / 2

            if Z_data[i] < Z_nmt[j]:
                Z_1 = Z_data[i]
                Z_2 = Z_nmt[j]
            else:
                Z_1 = Z_nmt[j]
                Z_2 = Z_data[i]

            point = equation(X_2, Y_2, Z_2) - equation(X_1, Y_2, Z_2) - equation(X_2, Y_1, Z_2) + equation(X_1, Y_1, Z_2) - \
                    equation(X_2, Y_2, Z_1) + equation(X_1, Y_2, Z_1) + equation(X_2, Y_1, Z_1) - equation(X_1, Y_1, Z_1)

            integral_point = integral_point + point

            plt.scatter(X_nmt[j], Y_nmt[j], color='red')
            square = Rectangle((X_nmt[j] - 500, Y_nmt[j] - 500), 1000, 1000, fill=False, color='green')
            plt.gca().add_patch(square)

    integral_results.append(integral_point)

for i in range(len(X_data)):
    circle = Circle((X_data[i], Y_data[i]), 1200, fill=False, color='blue')
    plt.gca().add_patch(circle)

plt.scatter(X_data, Y_data, color='blue')
plt.axis('equal')
plt.show()

# TERRAIN CORRECTION [mgal]

terrain_correction = []

for value in integral_results:
    terrain_correction.append(value * G * p_density * 100000)

# PRINT AND SAVE RESULTS

print(terrain_correction)
print('\nNumber of points: ', len(terrain_correction))
