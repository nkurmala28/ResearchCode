from datetime import datetime
from geopy.distance import great_circle
from anytree import Node, RenderTree

parentslist = []
parentslistID = []
childlistID = []

def parentfinder(filename):
    fileopen = open(filename)
    dataset = fileopen.readlines()
    count = 0
    for parent in dataset:
        parent = parent.strip()
        id1,time1,latt,long = parent.split(',')
        parent = parent.split(',')
        if int(id1) in childlistID:
            continue
        if int(id1) in parentslistID:
            continue
        datetime1 = datetime.strptime(time1,'%d-%b-%y')
        loc1 = (float(latt),float(long))
        count += 1
        internalcount = count
        for child in dataset[count:]:
            internalcount += 1
            child = child.strip()
            id2,time2,latt2,long2 = child.split(',')
            if int(id2) in childlistID:
                continue
            child = child.split(',')
            datetime2 = datetime.strptime(time2,'%d-%b-%y')
            loc2 = (float(latt2),float(long2))
            duration = (datetime2-datetime1).days
            if duration < 0:
                continue
            dist = great_circle(loc1,loc2).kilometers
            if 0 < dist < 10 and 0 < duration <= 5:
                parentnode = Node(str(parent[0]))                          #how do I store my data on the nodes? do a .latt? .long?
                if int(id1) not in parentslistID:
                    parentslistID.append(int(id1))
                    parentslist.append(parentnode)
                childfinder(dataset[internalcount-2:],parentnode,parent)

def childfinder(trial,parentnode,parent):
    count = 0
    for otherchildren in trial:
        count += 1
        otherchildren = otherchildren.strip()
        id2, time2, latt2, long2 = otherchildren.split(',')
        otherchildren = otherchildren.split(',')
        if int(id2) in childlistID:
            continue
        datetime1 = datetime.strptime(parent[1], '%d-%b-%y')
        datetime2 = datetime.strptime(time2, '%d-%b-%y')
        loc1 = (float(parent[2]),float(parent[3]))
        loc2 = (float(latt2), float(long2))
        duration = (datetime2 - datetime1).days
        if duration < 0:
            continue
        if duration > 5:
            break
        dist = great_circle(loc1, loc2).kilometers
        if 0 < dist < 10 and 0 < duration <= 5:
            childlistID.append(int(otherchildren[0]))
            childnode = Node(str(otherchildren[0]),parent=parentnode)
            childfinder(trial[count+1:],childnode,otherchildren)
            continue


parentfinder("trialdata.csv")
for i in parentslist:
    for pre, fill, node in RenderTree(i):
        print("%s%s" % (pre, node.name))



""""
 for every child find, trigger the search, then when there arent any more children found, traverse back to the previous parent 
 and do the same, find if there are any other children for the given parent
"""