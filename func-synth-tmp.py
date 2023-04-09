import csv

def foo(n):
    return 2 * n + 2

domain = range(0, 10)

with open("func-synth-tmp.csv", "w+") as file:
    w = csv.writer(file)
    for x in domain:
        w.writerow([x, foo(x)])