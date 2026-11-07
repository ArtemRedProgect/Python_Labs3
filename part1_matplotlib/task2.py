import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-8, 8, 2000)
y = 4 / (x ** 2 - 4)
y = np.ma.masked_where(np.abs(np.abs(x) - 2) < 0.05, y)

fig, ax1 = plt.subplots(figsize=(10, 7))

ax1.plot(x, y, label="y(x)")
ax1.axvline(-2, color="red", linestyle="--", label="асимптоты x = ±2")
ax1.axvline(2, color="red", linestyle="--")
ax1.set_xlim(-8, 8)
ax1.set_ylim(-10, 10)
ax1.set_title("График функции y(x)")
ax1.set_xlabel("x")
ax1.set_ylabel("y(x)")
ax1.grid(True)
ax1.legend()
ax1.set_xticks(np.arange(-8, 9, 2))

plt.tight_layout()
plt.show()