import pandas as pd
import numpy as np
import openpyxl
import math

file_path = 'Geofizyka.xlsx'
df_data = pd.read_excel(file_path, sheet_name='Data')
df_NMT = pd.read_excel(file_path, sheet_name='NMT')

# print(df_data)
# print(df_NMT)

# n - liczba wycinków
# rl, rl_1 - długość promieni ograniczających dany odcinek
# h - średnia wysokość terenu objętego i-tym wycinkiem w stosunku do położenia punktu pomiarowego
# k - stałą grawitacji
# p - średnia gęstość skał w podłozu

# CONSTANTS

p = 2.670  # kg / m * m * m
k = 6.67430 * (10 ^ (-11))

# DATA

Y_data = df_data['EG'].tolist()
X_data = df_data['NG'].tolist()
Z_data = df_data['H'].tolist()

g_data = df_data['g'].tolist()

B_data = [(x * math.pi / 180) for x in df_data['B'].tolist()]
L_data = [(x * math.pi / 180) for x in df_data['L'].tolist()]

# print(Y_data)
# print(X_data)
# print(H_data)
# print(g_data)
# print(B_data)
# print(L_data)

# NMT DATA

Y_nmt = df_NMT['NCN'].tolist()
X_nmt = df_NMT['NCE'].tolist()
Z_nmt = df_NMT['Hnorm'].tolist()

# print(Y_nmt)
# print(X_nmt)
# print(H_nmt)

w1, k1 = len(Y_data), len(Y_data)
w2, k2 = len(Y_nmt), len(Y_nmt)

popr_terenowa = []

for i in range(w2):
    for j in range(w1):
        l = math.sqrt((Y_data[j] - Y_nmt[i]) ** 2 + (X_data[j] - X_nmt[i]) ** 2 + (Z_data[j] - Z_nmt[i]) ** 2)

        popr_pkt = (abs(k * p *
                        (((Z_data[j] * math.atan(X_data[j] * Y_data[j] / l / Z_data[j])) -
                        ((Z_data[j] * math.atan(X_nmt[i] * Y_data[j] / l / Z_data[j]))))) -
                        ((Z_data[j] * math.atan(X_data[j] * (Y_nmt[i] / l / Z_data[j]))) -
                        ((Z_data[j] * math.atan(X_nmt[i] * Y_nmt[i] / l / Z_data[j]))))) -
                        k * p *
                        (((Z_nmt[i] * math.atan(X_data[j] * Y_data[j] / l / Z_nmt[i])) -
                        ((Z_nmt[i] * math.atan(X_nmt[i] * Y_data[j] / l / Z_nmt[i]))))) -
                        ((Z_nmt[i] * math.atan(X_data[j] * Y_nmt[i] / l / Z_nmt[i]))) -
                        ((Z_nmt[i] * math.atan(X_nmt[i] * Y_nmt[i] / l / Z_nmt[i]))))

        popr_terenowa.append(popr_pkt)

print(popr_terenowa)
print(len(popr_terenowa))
