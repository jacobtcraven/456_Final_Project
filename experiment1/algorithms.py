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
    sorted_ws = sorted(weights)
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
            w -= w_ints[i - 1]
            k -= 1
            i -= 1

    return res[::-1]
