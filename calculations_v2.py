import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import openpyxl
import math

from matplotlib.patches import Circle

file_path = 'Geofizyka.xlsx'
df_data = pd.read_excel(file_path, sheet_name='Data')
df_NMT = pd.read_excel(file_path, sheet_name='NMT')


# DATA

X_data = df_data['EG'].tolist()
Y_data = df_data['NG'].tolist()
Z_data = df_data['H'].tolist()

g_data = df_data['g'].tolist()

B_data = [(x * math.pi / 180) for x in df_data['B'].tolist()]
L_data = [(x * math.pi / 180) for x in df_data['L'].tolist()]


# NMT DATA

X_nmt = df_NMT['NCE'].tolist()
Y_nmt = df_NMT['NCN'].tolist()
Z_nmt = df_NMT['Hnorm'].tolist()


# CONSTANTS

p_density = 2670  # kg / m * m * m
G = 6.67430 * (10 ^ (-11))


# OTHERS

number_of_points = len(X_data)
number_of_grids = len(X_nmt)
Integral = np.zeros((number_of_grids, 1))

# NUMERIC INTEGRATION

for i in range(number_of_points):
    for j in range(number_of_grids):
        distance = math.sqrt((X_nmt[j] - X_data[i]) ** 2 + (Y_nmt[j] - Y_data[i]) ** 2 + (1 / 2 * (Z_nmt[j] - Z_data[i])) ** 2)

        if distance <= 1200:
            Integral_in_point = Z_nmt[j] * (math.atan((X_nmt[j] * Y_nmt[j]) / (Z_nmt[j] * distance)) - math.atan((X_data[i] * Y_nmt[j]) / (Z_nmt[j] * distance)) -
                                            math.atan((X_nmt[j] * Y_data[i]) / (Z_nmt[j] * distance)) + math.atan((X_data[i] * Y_data[i]) / (Z_nmt[j] * distance))) - \
                                Z_data[i] * (math.atan((X_nmt[j] * Y_nmt[j]) / (Z_data[i] * distance)) - math.atan((X_data[i] * Y_nmt[j]) / (Z_data[i] * distance)) -
                                             math.atan((X_nmt[j] * Y_data[i]) / (Z_data[i] * distance)) + math.atan((X_data[i] * Y_data[i]) / (Z_data[i] * distance)))
            Integral[i, 0] += Integral_in_point

            plt.scatter(X_nmt[j], Y_nmt[j], color='red')


for i in range(len(X_data)):
    circle = Circle((X_data[i], Y_data[i]), 1200, fill=False, color='blue')
    plt.gca().add_patch(circle)


plt.scatter(X_data, Y_data, color='blue')
plt.axis('equal')
plt.show()

# TERRAIN CORRECTION [mgal]

terrain_correction = np.zeros((number_of_points, 1))

for i in range(number_of_points):
    terrain_correction[i] = G * p_density * Integral[i] * 100000

print(terrain_correction)
print('\n', len(terrain_correction))
