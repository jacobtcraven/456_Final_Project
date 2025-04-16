# Jacob Craven, Kevin Endrijaitis, Braden Burgener, Adam Rich​
# CS 490 AA
# Final Project Code

import numpy as np

def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        weights = []
        for line in lines:
            weights.append(line.strip())
        file.close()
    return weights

def knapsack(packages, capacity, package_limit):
    num_rows = len(packages) + 1
    num_cols = capacity + 1
    matrix = np.zeros((num_rows, num_cols), dtype=int)
    for i in range(1,packages):
        packages[i] = float(packages[i]) / 16.0


def greedy(packages, capacity):
    current_weight = 0
    current_deliveries = []
    for package in packages:
        if current_weight + package <= capacity:
            current_weight += package
            current_deliveries.append(package)
            packages.remove(package)
        else:
            break
        

if __name__ == "__main__":
    weights = load_data("amazon_weights.txt")
    print(len(weights))
    knapsack(weights, 20, 2)