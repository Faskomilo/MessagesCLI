import csv

with open('test.csv', "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x in reader:
        print(x[0])