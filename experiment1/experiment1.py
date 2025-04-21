# experiment1.py

import csv
import random

from algorithms import load_data, knapsack, greedy

# Node order (hub MUC first, then the 9 delivery buildings)
EXP_NODES_ORDER = [
    "MUC", "Rendleman Hall", "Dunham Hall", "Library",
    "Founders/Alumni Hall", "Vadalabene Center",
    "Science East", "Science West", "Engineering Building", "Art and Design"
]

# 10×10 adjacency matrix (feet)
NODES = EXP_NODES_ORDER
MATRIX = [
    [   0,  300,  590, 1140, 1325, 1880, 1320, 1040,  790,  550],
    [ 300,    0,  625, 1355, 1565, 2300,  400,  450,  910, 1025],
    [ 590,  625,    0,  645,  625, 1200,  570,  290,  375,  430],
    [1140, 1355,  645,    0,  300, 1355,  645,  575,  940,  985],
    [1325, 1565,  625,  300,    0, 1085,  400,  450,  910, 1025],
    [1880, 2300, 1200, 1355, 1085,    0,  720,  920, 1105, 1345],
    [1320,  400,  570,  645,  400,  720,    0,  280,  695,  885],
    [1040,  450,  290,  575,  450,  920,  280,    0,  460,  625],
    [ 790,  910,  375,  940,  910, 1105,  695,  460,    0,  245],
    [ 550, 1025,  430,  985, 1025, 1345,  885,  625,  245,    0],
]
# Build distance lookup
DIST = {
    NODES[i]: { NODES[j]: MATRIX[i][j] for j in range(len(NODES)) }
    for i in range(len(NODES))
}


def simulate_delivery(assignments, capacity):
    """
    Given a fixed list of (node, weight) to deliver, split into
    as many load‐up trips as needed (greedily by order), then for each
    trip record every segment (from→to, distance, load, speed, time).
    """
    # Break into capacity‐constrained trips in assignment order
    trips = []
    curr_trip = []
    curr_w = 0.0
    for node, w in assignments:
        if curr_w + w <= capacity:
            curr_trip.append((node, w))
            curr_w += w
        else:
            trips.append(curr_trip)
            curr_trip = [(node, w)]
            curr_w = w
    if curr_trip:
        trips.append(curr_trip)

    segments = []
    for ti, trip in enumerate(trips, start=1):
        # Only visit the nodes in this trip, in EXP_NODES_ORDER
        to_visit = [n for n, _ in trip]
        visit_seq = [n for n in EXP_NODES_ORDER if n in to_visit]

        # Start at hub, do all deliveries, return
        path = ["MUC"] + visit_seq + ["MUC"]
        load = sum(w for _, w in trip)
        onboard = {n: w for n, w in trip}

        for i in range(len(path) - 1):
            frm, to = path[i], path[i + 1]
            d = DIST[frm][to]
            speed = 65 - (20 * (load / 20))
            t = d / speed

            segments.append({
                "trip":       ti,
                "from":       frm,
                "to":         to,
                "distance_ft":d,
                "load_lb":    load,
                "speed_ftps": speed,
                "time_s":     t
            })

            # drop off if it's one of our packages
            if to in onboard:
                load -= onboard[to]
                del onboard[to]

    reloads = len(trips) - 1
    total_time = sum(s["time_s"] for s in segments)
    return segments, reloads, total_time


def run_experiment():
    all_weights = load_data("amazon_weights.txt")
    capacity = 20.0

    # Prepare CSV writers
    seg_file = open("experiment1_results.csv", "w", newline="")
    seg_cols = ["algorithm", "k", "trip", "from", "to", "distance_ft", "load_lb", "speed_ftps", "time_s"]
    seg_writer = csv.DictWriter(seg_file, fieldnames=seg_cols)
    seg_writer.writeheader()

    sum_file = open("experiment1_summary.csv", "w", newline="")
    sum_cols = ["algorithm", "k", "reloads", "total_time_s"]
    sum_writer = csv.DictWriter(sum_file, fieldnames=sum_cols)
    sum_writer.writeheader()

    # For k = 2…10, sample once and assign once
    for k in range(2, len(EXP_NODES_ORDER) + 1):
        # 1) pick k random weights
        sample_weights = random.sample(all_weights, k)

        # 2) assign in a fixed order to the first k delivery nodes
        delivery_nodes = EXP_NODES_ORDER[1:k]  # skip “MUC”
        assignments = list(zip(delivery_nodes, sample_weights))

        # 3) run both algorithms on that identical assignment
        for name, algo in [("knapsack", knapsack), ("greedy", greedy)]:
            # note: we still call algo(...) to let it reorder sample_weights if needed;
            # but it sees *exactly* the same k weights.
            selected = algo(sample_weights, capacity, k)

            # we need to filter assignments down to only those packages chosen
            chosen_set = set(selected)
            chosen_assign = [(n, w) for (n, w) in assignments if w in chosen_set]

            segs, reloads, tot = simulate_delivery(chosen_assign, capacity)

            # write segments
            for s in segs:
                seg_writer.writerow({
                    "algorithm": name,
                    "k":         k,
                    **s
                })

            # summary
            sum_writer.writerow({
                "algorithm":   name,
                "k":           k,
                "reloads":     reloads,
                "total_time_s":tot
            })

    seg_file.close()
    sum_file.close()


if __name__ == "__main__":
    run_experiment()
