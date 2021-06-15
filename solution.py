'''
1. Calculate effective fees, weight and parents of each transaction by storing the sum of fees, weight n list of parents of their parents
2. knapsack approach on effective fees n weight would have been better
	but I instead sorted the transactions n took the ones with highest fees obviously taking in account their parents too.
3. I have updated the parameter for sort function as the effective fees per weight


'''

# tx_id,fee,weight,parents


import csv
import sys
sys.setrecursionlimit(10**5)
cost_limit = 4000000
visited = {}
tmap = {}

'''
#TODO: Make this function iterative instead of recursive
def knapsack(tlist, n, w):
    global tmap
    print(n)
    if(n == 0 or w == 0):
        return [0, ['']]
    if tuple([tuple(tlist), n, w]) in visited.keys():
        return visited[tuple(tuple(tlist), n, w)]
    tid = tlist[n]
    if tmap[tid][1] > w:
        return(knapsack(tlist, n-1, w))
    temp = tlist.copy()
    tresult = []
    tw = w-tmap[tid][1]
    l = len(tmap[tid][2])
    for i in tmap[tid][2]:
        if i == '':
            l = 0
            break

        if i not in temp:
            tw += tmap[i][1]
        else:
            temp.remove(i)
            tresult.append(i)
    selected = knapsack(temp, n-1-l, tw)
    selected[0] += tmap[tlist[tid][0]]
    notselected = knapsack(tlist, n-1, w)
    if selected[0] > notselected[0]:
        selected[1].append(tid)
        selected[1].extend(tresult)
        visited[tuple([tuple(tlist), n, w])] = selected
        return selected
    visited[tuple([tuple(tlist), n, w])] = notselected
    return notselected
'''

def effmap(tid):
    global tmap
    if tmap[tid][3] != -1:  # check if effective has been calculated
        return tmap[tid][3:6] #return effective fees weight and parents
    w, f = 0, 0  # initialise weight and fees
    p = []  # initialise parent list
    for j in tmap[tid][2]:  # iterating through parents
        if j != '':
            x = effmap(j)
            f += x[0]
            w += x[1]
            p.extend(x[2])  # appending the parents
    f += int(tmap[tid][0])
    w += int(tmap[tid][1])
    p.extend(tmap[tid][2])
    tmap[tid][3] = f #fees
    tmap[tid][4] = w #weight
    tmap[tid][5] = p #parents
    tmap[tid][6]=f/w # effective fees per 1 wt
    return[f, w, p]


def main():
	
	#Parsing the csv file
    filename = "mempool.csv"
    global tmap, cost_limit
    fields = []

    with open(filename, 'r') as csvfile:

        csvreader = csv.reader(csvfile)

        fields = next(csvreader)

        for row in csvreader:
            tmap[row[0]] = list(map(int, row[1:3]))
            tmap[row[0]].append(row[3].split(';'))
            tmap[row[0]].extend([-1, -1, [],-1]) #fees, weight, parents, effective fees per weight
	
#Calculating Efficiency
    for i in tmap.keys():
        effmap(i)
# sorting with the effective fees per wt
    tmap = dict(sorted(tmap.items(), key=lambda item: item[1][6],reverse=True)) 
    tmap_og = tmap.copy()
    max_tid = []
    l = list(tmap.keys())
    
#call for the knapsack function 
    # z = knapsack(l, len(l)-1, cost_limit)
#     print(z[1])
    for t in l:
        if cost_limit<1:
            break
        if t in tmap.keys():
            if int(tmap[t][1]) > cost_limit: # if fees > cost_limit
                continue
            cost_limit -= int(tmap[t][1]) # subtract fees from the cost_limit
            for i in tmap[t][2][::-1]: #reverse so that the oldest parents always come first
                if i != '': #if the list of parents does not contain an empty string
                    max_tid.append(i)
                    parent = tmap.pop(i, None) # remove the parent after its considered
                    if parent == None: # None would signify that it has already been removed earlier
                        cost_limit += tmap_og[i][1] # fees of parent of 2 transactions will only be considered once
                    else:
                        l.remove(i) # remove parent from the iteration list as it has been considered
            max_tid.append(t)
    
    f=open("block.txt","w")
    for i in max_tid:
        f.write(i+"\n")
    f.close()
    
if __name__ == "__main__":
    main()
