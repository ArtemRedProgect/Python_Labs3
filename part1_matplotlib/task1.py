import numpy as np
import matplotlib.pyplot as plt

xGrafic = np.linspace(-360, 360, 1000)
xCalc = np.deg2rad(xGrafic)

p = np.exp(np.sin(xCalc)) + np.log(np.sin(0.5 * xCalc) ** 2 + 1) * np.cos(xCalc)
q = -np.log((np.sin(xCalc) - np.cos(xCalc)) ** 2 + 2) + 8

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 7))

ax1.plot(xGrafic, p, label="p(x)")
ax1.set_title("График функции p(x)")
ax1.set_ylabel("p(x)")
ax1.grid(True)
ax1.legend()

ax2.plot(xGrafic, q, label="q(x)")
ax2.set_title("График функции q(x)")
ax2.set_xlabel("x, градусы")
ax2.set_ylabel("q(x)")
ax2.grid(True)
ax2.legend()
ax2.set_xticks(np.arange(-360, 361, 90))

plt.tight_layout()
plt.show()