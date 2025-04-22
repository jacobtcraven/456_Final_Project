# def load_data(filename):
#     with open(filename, 'r') as file:
#         weights = [float(line.strip()) / 16.0 for line in file]
#     return weights

# def knapsack(weights, capacity, m):
#     # For DP indices, cast weights & capacity to ints
#     w_ints = [int(w) for w in weights]
#     cap = int(capacity)
#     n = len(weights)

#     # dp[i][k][w] = True if we can pick k of first i items to total weight w
#     dp = [[[False] * (cap + 1) for _ in range(m + 1)] for __ in range(n + 1)]
#     dp[0][0][0] = True

#     for i in range(1, n + 1):
#         wi = w_ints[i - 1]
#         for k in range(m + 1):
#             for w in range(cap + 1):
#                 # skip item i
#                 if dp[i-1][k][w]:
#                     dp[i][k][w] = True
#                 # take item i
#                 if k > 0 and w >= wi and dp[i-1][k-1][w-wi]:
#                     dp[i][k][w] = True

#     # find the heaviest achievable w for exactly m items
#     best_w = max(w for w in range(cap + 1) if dp[n][m][w])

#     # backtrack to recover which items were used
#     res = []
#     i, k, w = n, m, best_w
#     while i > 0 and k > 0:
#         if dp[i-1][k][w]:
#             # didn’t use item i
#             i -= 1
#         else:
#             # used item i
#             res.append(weights[i-1])
#             w -= w_ints[i-1]
#             k -= 1
#             i -= 1

#     return res[::-1]



# def greedy(packages, capacity, m):
#     current_weight = 0
#     current_deliveries = []
#     for package in packages:
#         if len(current_deliveries) >= m:
#             break
#         if current_weight + package <= capacity:
#             current_weight += package
#             current_deliveries.append(package)
#             packages.remove(package)
#         else:
#             break 

# algorithms.py

def load_data(filepath):
    """
    Load package weights from a text file.
    Each line should contain a single number (int or float).
    """
    with open(filepath, 'r') as file:
        weights = [float(line.strip()) / 16.0 for line in file]
    return weights


def greedy(weights, capacity, m):
    """
    Greedy loader (smallest-first).  
    Take up to m packages, stopping if adding the next would exceed capacity.
    """
    sorted_ws = weights
    total = 0.0
    picked = []
    for w in sorted_ws:
        if len(picked) >= m:
            break
        if total + w <= capacity:
            picked.append(w)
            total += w
        else:
            break
    return picked


def knapsack(packages, capacity, package_limit):
    """
    0–1 knapsack: choose up to package_limit items maximizing total weight ≤ capacity.
    Quick greedy fallback for most cases, DP for precise packing.
    """
    # Quick greedy pre-check
    greedy_sel = greedy(packages.copy(), capacity, package_limit)
    if sum(greedy_sel) >= 0.9 * capacity:
        for p in greedy_sel:
            packages.remove(p)
        return greedy_sel

    # Convert to integer weights (tenths of lb) for DP
    scale = 10
    w_ints = [int(p * scale) for p in packages]
    cap = int(capacity * scale)
    n = len(w_ints)

    w_ints = [int(p) for p in packages]
    cap = int(capacity)
    n = len(w_ints)

    # DP table
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    pick = [[False] * (cap + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wi = w_ints[i - 1]
        prev = dp[i - 1]
        curr = dp[i]
        pick_row = pick[i]
        for w in range(cap + 1):
            no = prev[w]
            yes = prev[w - wi] + wi if w >= wi else -1
            if yes > no:
                curr[w] = yes
                pick_row[w] = True
            else:
                curr[w] = no

    # Backtrack
    w_best = max(range(cap + 1), key=lambda w: dp[n][w])
    res = []
    i = n
    count = 0
    while i > 0 and w_best > 0 and count < package_limit:
        if pick[i][w_best]:
            res.append(packages[i - 1])
            w_best -= w_ints[i - 1]
            count += 1
        i -= 1
    res.reverse()

    # Remove chosen
    for p in res:
        packages.remove(p)
    return res
