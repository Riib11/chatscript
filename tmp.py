import csv
    
def fql(n):
    return n * n

domain = range(0, 7, 2)

with open("tmp.csv") as file:
    w = csv.writer(file)
    for x in domain:
        w.writerow([x, fql(x)])