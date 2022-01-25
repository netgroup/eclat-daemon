import matplotlib.pyplot as plt
import json

with open("time_stats.json", "r", encoding="utf8") as file:
    measures = json.load(file)
for key in measures:
    plt.plot(measures[key], label=key)
plt.legend()
plt.savefig("measures.png", dpi=200)