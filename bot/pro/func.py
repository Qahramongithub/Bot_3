import numpy as np

Y = np.array([1, 2, 3, 4, 5])            # Uzunligi 5
y_prit = np.array([1, 2, 3, 4, 5, 6])     # Uzunligi 6

# Farqini topamiz:
# difference = Y - y_prit


if len(Y) == len(y_prit):
    difference = Y - y_prit
else:
    print("Xatolik: massivlar uzunligi teng emas!")

