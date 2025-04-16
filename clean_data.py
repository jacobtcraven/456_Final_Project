import pandas as pd
import numpy as np

def valid_value(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

filename = "output2.csv"

cleaned_weights = []
with open(filename, "r") as file:
    # lines = file.readlines()
    # lines = [line.strip() for line in lines]
    # lines = [line.split(",") for line in lines]
    # results = []
    # for line in lines:
    #     weight = line[13].split()
    #     if weight == "" or len(weight) < 2:
    #         continue
    #     if  (weight[1] != "ounces" and weight[1] != "pounds"):
    #         continue
    #     if float(weight[0]) > 20 and weight[1] == "pounds":
    #         continue
    #     results.append(weight)
    #     print(weight)
    # print(len(results))
    # file.close()

    # df = pd.read_csv(filename, header=None)
    # print(df.head())
    # df[0] = df[0].str.strip('"')
    # weights = df.dropna()
    # print(weights)

    lines = file.readlines()
    weights = lines[0].split(",")
    cleaned_weights = []

    for weight in weights:
        if weight == "nan":
            continue

        weight = weight.strip()
        
        if weight == "":
            continue

        words = weight.split()
        if len(words) < 2:
            continue
        if words[1] not in ["ounces", "pounds"]:
            continue
        if not valid_value(words[0]):
            continue
        if words[1] == "pounds":
            # print(words[0])
            words[0] = float(words[0]) * 16
        if float(words[0]) > 320:
            continue

        cleaned_weights.append(words[0])

    # for weight in cleaned_weights:
    #     print(weight)

    print(len(cleaned_weights))
    file.close()

with open("amazon_weights.txt", "w") as file:
    for weight in cleaned_weights:
        file.write(f"{weight}\n")
    file.close()