import csv
import argparse
import statistics
from prettytable import PrettyTable


import matplotlib.pyplot as plt




def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--theory',
                        help='Theory to use',
                        required=True)
    args = parser.parse_args()
    return args


def pre_time(name, solver):
    val = float(pre_data[name][1 if solver[0]=='z' else 3])
    if val == 0:
        return 0.005
    else:
        return val
def tool_time(name):
    return float(tool_times[name][0])
def solver_time(name, solver):
    val = float(solver_times[name][0 if solver[0]=='z' else 1])
    if val == 0:
        return 0.005
    else:
        return val
def check_time(name):
    return float(check_results[name][0])

def is_good(name):
    if not name in check_results:
        return False
    else:
        return check_results[name][1] == "true"
    
def is_good_slot(name):
    return (name in slot_stats)

def total_post_time(name, solver):
    return solver_time(name, solver) + tool_time(name) + check_time(name)

def portfolio_post_time(name, solver):
    if is_good(name):
        return min(pre_time(name, solver), total_post_time(name, solver))
    else:
        return pre_time(name, solver)

def prop_speedup(name, solver):
    return pre_time(name, solver) / total_post_time(name, solver)

def portfolio_prop_speedup(name, solver):
    return pre_time(name, solver) / portfolio_post_time(name, solver)

def time_saved(name, solver):
    return pre_time(name, solver) - portfolio_post_time(name, solver)


def portfolio_speedup(name, solver):
    if not is_good(name):
        return 1
    else:
        return portfolio_prop_speedup(name, solver)
    
    
def slot_time(name):
    return float(slot_stats[name][9]) + float(slot_stats[name][10]) + float(slot_stats[name][11])

def slot_post_time(name, solver):
    val = float(slot_res[name][0 if solver[0]=='z' else 1])
    if val == 0:
        return 0.005
    else:
        return val
    
    
    
def total_post_time_slot(name, solver):
    return slot_post_time(name, solver) + slot_time(name) + tool_time(name) + check_time(name)

def portfolio_post_time_slot(name, solver):
    if is_good_slot(name):
        return min(pre_time(name, solver), total_post_time_slot(name, solver))
    else:
        return pre_time(name, solver)

def prop_speedup_slot(name, solver):
    return pre_time(name, solver) / total_post_time_slot(name, solver)

def portfolio_prop_speedup_slot(name, solver):
    return pre_time(name, solver) / portfolio_post_time_slot(name, solver) 

def portfolio_speedup_slot(name, solver):
    if not is_good_slot(name):
        return 1
    else:
        return portfolio_prop_speedup_slot(name, solver)
    
    
    
    
    



def all_names(interval=None):
    if interval:
        return list(filter(lambda x: pre_time(x, interval[2]) >= interval[0] and pre_time(x, interval[2]) <= interval[1], pre_data.keys()))
    else:
        return pre_data.keys()

def good_cases(interval=None):
    return list(filter(lambda x: is_good(x), all_names(interval)))

def good_cases_slot(interval=None):
    return list(filter(lambda x: is_good_slot(x), all_names(interval)))

def cases_ultimate(good=False):
    if good:
        return list(map(lambda x: x[0], filter(lambda x: x[5] == "1", ultimate_res)))
    else:
        return list(map(lambda x: x[0], ultimate_res))

def speedup_ultimate(good=False):
    dat = []
    if good:
        dat = list(map(lambda x: float(x[3])/float(x[4]), filter(lambda x: x[5] == "1", ultimate_res)))
    else:
        dat = list(map(lambda x: float(x[3])/float(x[4]), ultimate_res))
        
    return statistics.geometric_mean(dat)

def tractability_ultimate(good=False):
    dat = []
    if good:
        #Timeout check based on Ultimate Automizer default settings
        dat = list(map(lambda x: float(x[3])/float(x[4]), filter(lambda x: x[5] == "1" and float(x[3])*1000 > 12000, ultimate_res)))
    else:
        dat = list(map(lambda x: float(x[3])/float(x[4]), ultimate_res))
        
    return len(dat)


args = parse_args()

pre_data = {}
tool_times = {}
solver_times = {}
check_results = {}
slot_stats = {}
slot_res = {}
ultimate_res = []

with open("pre-"+args.theory+".csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        pre_data[row[0]] = row[1:]
        #pre_data.append(row)
        
with open(args.theory+"-tool-times.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        tool_times[row[0]] = row[1:]
        
with open(args.theory+"-solver-times.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        solver_times[row[0]] = row[1:]
        
with open(args.theory+"-check-results.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        check_results[row[0]] = row[1:]
        
with open(args.theory+"-slot-stats.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        slot_stats[row[0]] = row[1:]
        
with open(args.theory+"-slot-solver-times.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        slot_res[row[0]] = row[1:]
        
        
if args.theory == 'nia':
    with open("ultimate-res.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            ultimate_res.append(row)


    

#print(good_cases_slot())
#print(is_good_slot("./QF_NIA/AProVE/aproveSMT4771973489260118271.smt2"))


print("z3 tractability: "+str(len(good_cases((300,400, "z3")))))
print("cvc tractability: "+str(len(good_cases((300,400, "cvc")))))

all_cases = list(set(good_cases((300,400, "z3"))) & set(good_cases((300,400, "cvc"))))
print("both tractability :"+str(len(all_cases)))






original = list(map(lambda x: pre_time(x, 'z3'), good_cases()))
final = list(map(lambda x: portfolio_post_time(x, 'z3'), good_cases()))



fig1, ax = plt.subplots()


ax.scatter(original, final, c='black', marker='.')

if args.theory == 'nia' or args.theory == 'lia':
    ax.set_xlim(-10, 310)
    ax.set_ylim(-10, 310)
elif args.theory == 'nra' or args.theory == 'lra':
    if args.theory == 'nra':
        ax.set_xlim(0.005, 400)
        ax.set_ylim(0.005,400)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_aspect('equal')
    
    
    
ax.set_box_aspect(1)
#ax.set_xlabel("Original Solving Time (Unbounded Theory)")
#ax.set_ylabel("Final Solving Time (Bounded Theory)")



plt.savefig('plots/scatter-'+args.theory+'-z3.png', format = 'png', dpi=300, bbox_inches='tight', pad_inches=0)



original = list(map(lambda x: pre_time(x, 'cvc'), good_cases()))
final = list(map(lambda x: portfolio_post_time(x, 'cvc'), good_cases()))

fig2, ax2 = plt.subplots()

ax2.scatter(original, final, c='black', marker='.')

if args.theory == 'nia' or args.theory == 'lia':
    ax2.set_xlim(-10, 310)
    ax2.set_ylim(-10, 310)
    
elif args.theory == 'nra' or args.theory == 'lra':
    if args.theory == 'nra':
        ax2.set_xlim(0.005, 400)
        ax2.set_ylim(0.005,400)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_aspect('equal')

ax2.set_box_aspect(1)
#ax2.set_xlabel("Original Solving Time (Unbounded Theory)")
#ax2.set_ylabel("Final Solving Time (Bounded Theory)")



plt.savefig('plots/scatter-'+args.theory+'-cvc.png', format = 'png', dpi=300, bbox_inches='tight', pad_inches=0)



for sol in ["z3", "cvc"]:

    tos = [0, 1, 60, 180]
    myTable = PrettyTable(["time interval", "good #", "good x", "good slot x", "overall #", "overall x", "overall slot x"])
    for r in tos:
        good_list = list(map(lambda x: portfolio_prop_speedup(x,sol), good_cases((r,350, sol))))
        all_list = list(map(lambda x: portfolio_speedup(x,sol), all_names((r,350, sol))))
        good_slot_list = list(map(lambda x: portfolio_prop_speedup_slot(x,sol), good_cases_slot((r,350, sol))))
        all_slot_list = list(map(lambda x: portfolio_speedup_slot(x,sol), all_names((r,350, sol))))
        
        
        #w_post_list = list(map(lambda x: portfolio_post_time(x,sol), all_names((r,350, sol))))
        #w_pre_list = list(map(lambda x: pre_time(x,sol), all_names((r,350, sol))))
        myTable.add_row([str(r), \
            str(len(good_cases((r,350, sol)))),\
            round(statistics.geometric_mean(good_list),3) if len(good_list) > 0 else "-", \
            round(statistics.geometric_mean(good_slot_list),3) if len(good_slot_list) > 0 else "-", \
            str(len(all_names((r,350, sol)))),\
            round(statistics.geometric_mean(all_list),3) if len(all_list) > 0 else "-", \
            round(statistics.geometric_mean(all_slot_list),3) if len(all_slot_list) > 0 else "-"])
    print(sol)
    print(myTable)
    
if args.theory == 'nia':

    
    print("Ultimate Automizer:")
    print("Count: " + str(len(cases_ultimate())))
    print("Good count: " + str(len(cases_ultimate(True))))
    print("Timeout: " + str(tractability_ultimate(True)))
    print("Speedup for good cases: " + str(round(speedup_ultimate(True), 2)))
    print("Speedup for all cases: " + str(round(speedup_ultimate(), 3)))

        
exit()   
     