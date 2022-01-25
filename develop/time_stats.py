import subprocess
import json
from time import sleep

loopsizes = [5, 10, 15, 20, 25]
measures = {
    5: list(),
    10: list(),
    15: list(),
    20: list(),
    25: list()
}
for i in range(0, 300):
    if i%5 == 0:
        print(i)
    for loopsize in loopsizes:
        ret = subprocess.run(["./t2", str(loopsize)], capture_output=True)
        delta = int(ret.stdout)
        measures[loopsize].append(delta)
        sleep(1)
with open("time_stats.json", "w", encoding="utf8") as file:
    json.dump(measures, file)