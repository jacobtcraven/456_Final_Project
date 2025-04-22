import csv
import random
from algorithms import load_data, knapsack, greedy

# Drone parameters
PACKAGE_LIMIT = 20     # max # of packages per trip
CAPACITY_LB = 15.0     # max weight per trip (lb)

# Node list (hub + delivery)
NODES = [
    "MUC", "Rendleman Hall", "Dunham Hall", "Library",
    "Founders/Alumni Hall", "Vadalabene Center",
    "Science East", "Science West", "Engineering Building", "Art and Design"
]

# Adjacency matrix (feet)
MATRIX = [
    [   0,  485,  745, 1140, 1325, 1880, 1320, 1040,  790,  550, 1450],
    [ 485,    0, 1090, 1330, 1565, 2300, 1675, 1400, 1250, 1025, 1930],
    [ 745, 1090,    0,  590,  625, 1200,  570,  290,  375,  430, 1130],
    [1140, 1330,  590,    0,  300, 1355,  645,  575,  940,  985, 1635],
    [1325, 1565,  625,  300,    0, 1085,  400,  450,  910, 1025, 1480],
    [1880, 2300, 1200, 1355, 1085,    0,  720,  920, 1105, 1345,  960],
    [1320, 1675,  570,  645,  400,  720,    0,  280,  695,  885, 1110],
    [1040, 1400,  290,  575,  450,  920,  280,    0,  460,  625, 1060],
    [ 790, 1250,  375,  940,  910, 1105,  695,  460,    0,  245,  780],
    [ 550, 1025,  430,  985, 1025, 1345,  885,  625,  245,    0,  930],
    [1450, 1930, 1130, 1635, 1480,  960, 1110, 1060,  780,  930,    0],
]
DIST = {
    NODES[i]: {NODES[j]: MATRIX[i][j] for j in range(len(NODES))}
    for i in range(len(NODES))
}


def simulate_all_deliveries(algo, assignments, capacity, package_limit, nodes_order):
    """
    Repeated trips until all assignments delivered, following full loop of `nodes_order`.
    Ensures progress by delivering at least the lightest if algo returns empty.
    """
    remaining = assignments.copy()
    trip_idx = 0
    segments = []
    while remaining:
        trip_idx += 1
        ws = [w for _, w in remaining]
        loads = algo(ws, capacity, package_limit)
        if not loads:
            loads = [min(ws)]
        trip_assign = []
        for lw in loads:
            for idx, (node, wgt) in enumerate(remaining):
                if wgt == lw:
                    trip_assign.append((node, wgt))
                    del remaining[idx]
                    break
        path = ["MUC"] + nodes_order + ["MUC"]
        load = sum(w for _, w in trip_assign)
        onboard = {n: w for n, w in trip_assign}
        for i in range(len(path) - 1):
            frm, to = path[i], path[i+1]
            d = DIST[frm][to]
            speed = 65 - (20 * (load / 20))
            t = d / speed
            segments.append({
                "trip": trip_idx,
                "from": frm,
                "to": to,
                "distance_ft": d,
                "load_lb": load,
                "speed_ftps": speed,
                "time_s": t
            })
            if to in onboard:
                load -= onboard[to]
                del onboard[to]
    reloads = trip_idx - 1
    total_time_s = sum(seg["time_s"] for seg in segments)
    return segments, reloads, total_time_s


def run_experiment():
    all_weights = load_data("amazon_weights.txt")
    X = 2000
    pool = random.sample(all_weights, X)

    # CSV setup
    with open("experiment_results.csv", "w", newline="") as sf, \
         open("experiment_summary.csv", "w", newline="") as sumf:
        # detailed per‐segment file stays the same
        seg_cols = ["k","algorithm","trip","from","to","distance_ft",
                    "load_lb","speed_ftps","time_s"]
        seg_w = csv.DictWriter(sf, fieldnames=seg_cols)
        seg_w.writeheader()

        # new summary: one row per k, side‐by‐side metrics
        sum_cols = [
            "k",
            "greedy_reloads","greedy_time_s",
            "knapsack_reloads","knapsack_time_s"
        ]
        sum_w = csv.DictWriter(sumf, fieldnames=sum_cols)
        sum_w.writeheader()

        # loop over k = 2…len(NODES)
        for k in range(2, len(NODES) + 1):
            nodes_k = NODES[1:k]
            assignments = [(random.choice(nodes_k), w) for w in pool]

            # greedy run
            _, rel_g, tot_g = simulate_all_deliveries(
                greedy, assignments.copy(), CAPACITY_LB, PACKAGE_LIMIT, nodes_k
            )
            # knapsack run
            _, rel_k, tot_k = simulate_all_deliveries(
                knapsack, assignments.copy(), CAPACITY_LB, PACKAGE_LIMIT, nodes_k
            )

            # write detailed segments for BOTH algos
            for name, algo in [("greedy", greedy), ("knapsack", knapsack)]:
                segs, _, _ = simulate_all_deliveries(
                    algo, assignments.copy(), CAPACITY_LB, PACKAGE_LIMIT, nodes_k
                )
                for seg in segs:
                    seg_w.writerow({"k": k, "algorithm": name, **seg})

            # write ONE summary row per k
            sum_w.writerow({
                "k":                k,
                "greedy_reloads":   rel_g,
                "greedy_time_s":    tot_g,
                "knapsack_reloads": rel_k,
                "knapsack_time_s":  tot_k
            })

if __name__ == "__main__":
    run_experiment()