def valid_value(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

filename = "output2.csv"

cleaned_weights = []
with open(filename, "r") as file:


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
            words[0] = float(words[0]) * 16
        if float(words[0]) > 320:
            continue

        cleaned_weights.append(words[0])


    print(len(cleaned_weights))
    file.close()

with open("amazon_weights.txt", "w") as file:
    for weight in cleaned_weights:
        file.write(f"{weight}\n")
    file.close()