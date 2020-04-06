import csv
import random


def write_csv(path, input:dict):
    with open(path, 'w') as f:
        random_key = random.choice(list(input))
        writer = csv.DictWriter(f, [i for i in input[random_key]])
        writer.writeheader()
        for v in input.values():
            writer.writerow(v)
