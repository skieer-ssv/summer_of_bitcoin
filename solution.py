'''
1. Calculate effective fees, weight and parents of each transaction by storing the sum of fees, weight n list of parents of their parents
2. knapsack approach on effective fees n weight would have been better
	but I instead sorted the transactions n took the ones with highest fees obviously taking in account their parents too.
 

'''

# tx_id,fee,weight,parents


import csv
cost_limit = 4000000

tmap = {}



def effmap(tid):
    global tmap
    if tmap[tid][3] != -1: #check if effective has been calculated
        return tmap[tid][3:6]
    w, f = 0, 0 #initialise weight n fees
    p = [] #initialise parent list
    for j in tmap[tid][2]: #iterating through parents
        if j != '':
            x = effmap(j)
            f += x[0]
            w += x[1]
            p.extend(x[2]) #appending the parents
    f += int(tmap[tid][0])
    w += int(tmap[tid][1])
    p.extend(tmap[tid][2])
    tmap[tid][3] = f
    tmap[tid][4] = w
    tmap[tid][5] = p
    return[f, w, p]



filename = "mempool.csv"

fields = []

with open(filename, 'r') as csvfile:

    csvreader = csv.reader(csvfile)


    fields = next(csvreader)


    for row in csvreader:
        tmap[row[0]] = row[1:3]
        tmap[row[0]].append(row[3].split(';'))
        tmap[row[0]].extend([-1, -1, []])
for i in tmap.keys():
    effmap(i)


tmap = dict(sorted(tmap.items(), key=lambda item: item[1][0], reverse=True))

tmap_og = tmap.copy()
max_tid = []
total_fees = 0
l = list(tmap.keys())
for t in l:
    if cost_limit<1:
        break
    if t in tmap.keys():
        if int(tmap[t][1]) > cost_limit:
            continue
        cost_limit -= int(tmap[t][1])
        for i in tmap[t][2][::-1]: #reverse so that the oldest parents always come first
            if i != '':
                max_tid.append(i)
                parent = tmap.pop(i, None) # remove the parent after its considered
                if parent == None:
                    cost_limit += tmap_og[i][1] # parent of 2 transactions will only be considered once
                l.remove(i)
        max_tid.append(t)

f=open("block.txt","w")

for i in max_tid:
    f.write(i+"\n")
f.close()
