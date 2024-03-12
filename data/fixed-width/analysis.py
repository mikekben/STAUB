import csv
import argparse
import statistics
from prettytable import PrettyTable


import matplotlib.pyplot as plt


def cases(theory):
    return list(filter(lambda x: theory in x, uni_list))

def orig_time(name):
    return float(orig_list[name][0])

def orig_result(name):
    return orig_list[name][1]

def at_time(name, width):
    return float(res_lists[width][name][0])

def at_result(name, width):
    return res_lists[width][name][1]

def good_cases(width, theory):
    return list(filter(lambda x: theory in x, res_lists[width].keys()))


uni_list = []
res_lists = {16: {}, 32: {}, 64: {}, 128: {}}

orig_list = {}

with open("uni-list.txt", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        uni_list.append(row[0])
        
for width in [16, 32, 64, 128]:
    with open("uni-res-"+str(width)+".csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            res_lists[width][row[0].replace(".smt2-"+str(width)+".smt2", ".smt2")] = row[1:]
            
with open("solver-res.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        orig_list[row[0]] = row[1:]


for theory in ['QF_NIA', 'QF_LIA', 'QF_NRA', 'QF_LRA']:
    print("good cases: " + str(len(good_cases(16,'QF_NIA'))))
    #print("average time: " +)

    widths = [16, 32, 64, 128]
    myTable = PrettyTable(["width", "average time", "# timeouts", "differences"])
    for r in widths:
        myTable.add_row([str(r), \
            round(statistics.geometric_mean(list(map(lambda x: at_time(x, r), good_cases(r,theory)))), 1), \
            len(list(filter(lambda x: at_result(x, r) == 'timeout', good_cases(r, theory)))),
            round(len(list(filter(lambda x: at_result(x, r) != orig_result(x) and at_result(x, r) != 'timeout' and orig_result(x) != 'timeout', good_cases(r, theory))))/len(good_cases(r, theory))*100.0,1)  
             ])
            
    print(theory)
    print(myTable)

