import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, dblquad

f = lambda x: x * np.sin(x)

I1, error1 = quad(f, 0, np.pi)

print("1. Определённый интеграл:")
print(f"Результат: {I1:.10f}")
print(f"Аналитическое значение: {np.pi:.10f}")
print(f"Абсолютная погрешность: {abs(I1 - np.pi):.10e}")

g = lambda y, x: x + y

I2, error2 = dblquad(g,0, 1, lambda x: 0, lambda x: x)

print("\n2. Двойной интеграл:")
print(f"Результат: {I2:.10f}")
print("Аналитическое значение: 0.5")
print(f"Абсолютная погрешность: {abs(I2 - 0.5):.10e}")

N_values = np.array([10**3, 10**4, 10**5, 10**6])
exact_value = 0.5
errors = []
np.random.seed(42)

for N in N_values:
    x = np.random.uniform(0, 1, N)
    y = np.random.uniform(0, 1, N)
    values = (x + y) * (y <= x)
    I_mc = np.mean(values)
    error = abs(I_mc - exact_value)
    errors.append(error)
    print(f"\nN = {N}")
    print(f"Интеграл Монте-Карло: {I_mc:.6f}")
    print(f"Погрешность: {error:.6f}")

errors = np.array(errors)
plt.figure(figsize=(9, 5))
plt.loglog(N_values, errors, marker='o', linestyle='-', label='Метод Монте-Карло')
plt.xlabel('Количество точек N')
plt.ylabel('Абсолютная погрешность')
plt.title('Зависимость погрешности от числа точек')
plt.grid(True, which='both')
plt.legend()
plt.show()
