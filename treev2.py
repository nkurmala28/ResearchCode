from datetime import datetime
from geopy.distance import great_circle
from anytree import Node, RenderTree
import xlsxwriter as xw

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
        id1, time1, latt, long = parent.split(',')
        parent = parent.split(',')
        if int(id1) in childlistID:
            continue
        if int(id1) in parentslistID:
            continue
        datetime1 = datetime.strptime(time1, '%d-%b-%y')
        loc1 = (float(latt), float(long))
        count += 1
        internalcount = count
        for child in dataset[count:]:
            internalcount += 1
            child = child.strip()
            id2, time2, latt2, long2 = child.split(',')
            if int(id2) in childlistID:
                continue
            child = child.split(',')
            datetime2 = datetime.strptime(time2, '%d-%b-%y')
            loc2 = (float(latt2), float(long2))
            duration = (datetime2 - datetime1).days
            if duration < 0:
                continue
            dist = great_circle(loc1, loc2).kilometers
            if 0 < dist < 10 and 0 < duration <= 5:
                parentnode = Node(str(parent[0]))  # how do I store my data on the nodes? do a .latt? .long?
                if int(id1) not in parentslistID:
                    parentslistID.append(int(id1))
                    parentslist.append(parentnode)
                childfinder(dataset[internalcount - 2:], parentnode, parent)


def childfinder(trial, parentnode, parent):
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
        loc1 = (float(parent[2]), float(parent[3]))
        loc2 = (float(latt2), float(long2))
        duration = (datetime2 - datetime1).days
        if duration < 0:
            continue
        if duration > 5:
            break
        dist = great_circle(loc1, loc2).kilometers
        if 0 < dist < 10 and 0 < duration <= 5:
            childlistID.append(int(otherchildren[0]))
            childnode = Node(str(otherchildren[0]), parent=parentnode)
            childfinder(trial[count + 1:], childnode, otherchildren)
            continue


parentfinder("trialdata.csv")
for i in parentslist:
    for pre, fill, node in RenderTree(i):
        print("%s%s" % (pre, node.name))

# .....................


def excelResult_init():
    workbook = xw.Workbook('GCData.xlsx')
    outsheet = workbook.add_worksheet(name="Data1")
    outsheet.write("A1", "Relationship ID")  # (y,0)
    outsheet.write("B1", "Family ID")  # (y,1)
    outsheet.write("C1", "Parent ID")
    outsheet.write("D1", "Child ID")
    outsheet.write("E1", "Depth")  # (y,2)
    outsheet.write("F1", "Parent Latitude")  # (y,3)
    outsheet.write("G1", "Parent Longitude")
    outsheet.write("H1", "Child Latitude")
    outsheet.write("I1", "Child Longitude")
    outsheet.write("J1", "Duration")
    outsheet.write("K1", "Distance from Children")
    return outsheet


def result_excel(outsheet,Rel_ID,Fam_ID,P_ID,C_ID,Depth,P_latt,P_long,C_latt,C_long,Dur,Dist):
    outsheet.write("A1", Rel_ID)  # (y,0)
    outsheet.write("B1", Fam_ID)  # (y,1)
    outsheet.write("C1", P_ID)
    outsheet.write("D1", C_ID)
    outsheet.write("E1", Depth)  # (y,2)
    outsheet.write("F1", P_latt)  # (y,3)
    outsheet.write("G1", P_long)
    outsheet.write("H1", C_latt)
    outsheet.write("I1", C_long)
    outsheet.write("J1", Dur)
    outsheet.write("K1", Dist)
#     direction


""""
 for every child find, trigger the search, then when there arent any more children found, traverse back to the previous parent 
 and do the same, find if there are any other children for the given parent
"""
