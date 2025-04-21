from itertools import batched
import numpy as np
import math
import csv

MAX_WEIGHT = 20
MAX_PACKAGES = 15
DRONE_PATH_DISTANCES = [300, 625, 290, 920, 960, 780, 245, 550, 485, 1330]

#Returns (algorithm, number of drones, utilization percentage, maximum duration)
def experiment_two(weights, capacity, packagelimit, numdrones):
    utilizations = []

    for drones in range(1, numdrones+1):
        #Use "upside-down floor division" to avoid FP rounding errors when preforming a ceiling operation
        numpackages = -(len(weights)//-drones)
        packages = list(batched(weights, numpackages))

        utilization = 0
        durations = []
        for drone in range(0, drones):
            current_flight_duration = 0
            packagelist = list(packages[drone])
            while(len(packagelist) > 0):
                current_flight_duration = current_flight_duration + calculate_flight_duration(greedy(packagelist, capacity, packagelimit))
            utilization = utilization + current_flight_duration
            durations.append(current_flight_duration)
        utilization = utilization / (drones * max(durations))
        utilizations.append({
                "algorithm":   "greedy",
                "numdrones":   drones,
                "utilization": utilization,
                "maxduration": max(durations)
            })

        for drone in range(0, drones):
            current_flight_duration = 0
            packagelist = list(packages[drone])
            while(len(packagelist) > 0):
                current_flight_duration = current_flight_duration + calculate_flight_duration(knapsack(packagelist, capacity, packagelimit))
            utilization = utilization + current_flight_duration
            durations.append(current_flight_duration)
        utilization = utilization / (drones * max(durations))
        utilizations.append({
                "algorithm":   "knapsack",
                "numdrones":   drones,
                "utilization": utilization,
                "maxduration": max(durations)
            })

    return utilizations

#Returns flight duration in seconds
def calculate_flight_duration(weights):
    duration = 0
    total_weight = sum(weights)
    if(total_weight > MAX_WEIGHT):
        print("OVERWEIGHT")
        #return -1
    for i in range(0, len(weights)):
        current_distance = DRONE_PATH_DISTANCES[i%len(DRONE_PATH_DISTANCES)]
        velocity = 65 - (20 * (total_weight)/20) # weight in lbs, velocity in fps
        duration = duration + current_distance/velocity
        total_weight = total_weight - weights[i]
    return duration

def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        weights = []
        for line in lines:
            val = float(line.strip())/16
            if(val <= MAX_WEIGHT):
                weights.append(val)
            else:
                print("Overweight")
        file.close()
    return weights

def greedy(weights, capacity, m):
    """
    Greedy loader (smallest-first).  
    Take up to m packages, stopping if adding the next would exceed capacity.
    """
    sorted_ws = sorted(weights)
    total = 0.0
    picked = []
    for w in sorted_ws:
        if len(picked) >= m:
            break
        if total + w <= capacity:
            picked.append(w)
            weights.remove(w)
            total += w
        else:
            break
    return picked


def knapsack(weights, capacity, m):
    """
    0–1 knapsack forced to pick exactly m items if possible.
    If no combination of m items ≤ capacity exists, fall back to greedy.
    Returns the list of selected weights.
    """
    # Pre‑convert for DP indexing
    w_ints = [int(w) for w in weights]
    cap = int(capacity)
    n = len(weights)

    # dp[i][k][w] = True if we can pick k of first i items to total int‑weight w
    dp = [[[False] * (cap + 1) for _ in range(m + 1)] for __ in range(n + 1)]
    dp[0][0][0] = True

    for i in range(1, n + 1):
        wi = w_ints[i - 1]
        for k in range(m + 1):
            for w in range(cap + 1):
                # skip item i
                if dp[i - 1][k][w]:
                    dp[i][k][w] = True
                # take item i
                if k > 0 and w >= wi and dp[i - 1][k - 1][w - wi]:
                    dp[i][k][w] = True

    # find all achievable total‑weights for exactly m items
    possible_ws = [w for w in range(cap + 1) if dp[n][m][w]]
    if not possible_ws:
        # no exact-m solution → fallback to greedy
        return greedy(weights, capacity, m)

    best_w = max(possible_ws)

    # backtrack to recover which items were used
    res = []
    i, k, w = n, m, best_w
    while i > 0 and k > 0:
        if dp[i - 1][k][w]:
            # item i-1 was NOT used
            i -= 1
        else:
            # item i-1 WAS used
            res.append(weights[i - 1])
            weights.remove(weights[i-1])
            w -= w_ints[i - 1]
            k -= 1
            i -= 1

    return res[::-1]

weights = load_data("amazon_weights.txt")
print(len(weights))
result = experiment_two(weights, MAX_WEIGHT, MAX_PACKAGES, 4)

seg_file = open("experiment2_results.csv", "w", newline="")
seg_cols = ["algorithm", "numdrones", "utilization", "maxduration"]
seg_writer = csv.DictWriter(seg_file, fieldnames=seg_cols)
seg_writer.writeheader()

for s in result:
                seg_writer.writerow({
                    **s
                })