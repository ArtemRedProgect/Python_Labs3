import os
import matplotlib.patches as patches
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 7))

sky = patches.Rectangle((0, 0), 10, 10, facecolor="skyblue", edgecolor="none")
ax.add_patch(sky)

ground = patches.Rectangle((0, 0), 10, 3, facecolor="green", edgecolor="none")
ax.add_patch(ground)

sun = patches.Circle((1.5, 8.5), 0.8, facecolor="yellow", edgecolor="orange", linewidth=2)
ax.add_patch(sun)

cloud1 = patches.Ellipse((7.5, 8.5), 1.8, 0.8, facecolor="white", edgecolor="none", alpha=0.85)
cloud2 = patches.Ellipse((8.3, 8.3), 1.4, 0.7, facecolor="white", edgecolor="none", alpha=0.85)
ax.add_patch(cloud1)
ax.add_patch(cloud2)

building = patches.Rectangle((4, 2.5), 2.5, 4.5, facecolor="blue", edgecolor="darkblue", linewidth=2)
ax.add_patch(building)


roof = patches.Polygon([[3.8, 7.0], [5.25, 8.5], [6.7, 7.0]], facecolor="red", edgecolor="darkred",linewidth=2,)
ax.add_patch(roof)

window_positions = [(4.4, 5.5), (5.4, 5.5), (4.4, 4.0), (5.4, 4.0)]
for pos in window_positions:
    win = patches.Rectangle(pos, 0.6, 0.8, facecolor="lightyellow", edgecolor="darkblue", linewidth=1)
    ax.add_patch(win)

door = patches.Rectangle((4.9, 2.5), 0.7, 1.0, facecolor="brown", edgecolor="black", linewidth=1)
ax.add_patch(door)

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.axis("off")

os.makedirs("img", exist_ok=True)

plt.savefig("img/task3.png", dpi=150, bbox_inches="tight")
plt.show()
