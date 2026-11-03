
import numpy as np

A = np.array([ [4,   -1.5,  2,   0.5],
    [1,    5,   -2,   1.2],
    [-2,   1,    6,  -1],
    [0.5,  2,   -1,   7] ])

B = np.array([
    [11.05],
    [-6.82],
    [11.5],
    [-0.5]
])

det_A = np.linalg.det(A)

print("Определитель:", det_A)

if np.isclose(det_A, 0):
    print("Матрица необратима. Решение невозможно найти.")
else:
    cond_A = np.linalg.cond(A)
    print("Число обусловленности:", cond_A)

    A_inv = np.linalg.inv(A)
    X1 = A_inv @ B

    print("\nРешение через обратную матрицу:")
    print(X1)

    X2 = np.linalg.solve(A, B)

    print("\nРешение через solve:")
    print(X2)

    difference = np.linalg.norm(X1 - X2)
    print("\nНорма разности:", difference)

    check = np.linalg.norm(A @ X2 - B)
    print("Проверка подстановкой:", check)

    print("\nИтоговое решение:")
    print(np.round(X2.flatten(), 1))
