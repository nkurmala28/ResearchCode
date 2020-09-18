import xlsxwriter as xw
from datetime import datetime
from geopy.distance import great_circle

workbook = xw.Workbook('pleasework2.4.xlsx')
outsheet = workbook.add_worksheet(name="Data")
pcset = {}
y_index = 0

def main():
    excel_init()
    parent_child_finder("trialdata.csv")
    workbook.close()
    pass

def parent_child_finder(filename):
    fileopen = open(filename)
    dataset = fileopen.readlines()
    count = 0
    fam_id = 0
    rel_id = 000000
    for parent in dataset:
        fam_id +=1
        rel_id += 1000
        count += 1
        depth = 0
        childfinder(dataset[count + 1:], parent, depth,fam_id,rel_id)
        continue


def childfinder(trial,parent,depth,fam_id,rel_id):
    global y_index, pcset
    id1, time1, latt1, long1 = data_split(parent)
    loc1 = (latt1, long1)
    count = 0
    depth += 1
    for otherchildren in trial:
        count += 1
        id2, time2, latt2, long2 = data_split(otherchildren)
        if id1 in pcset and pcset[id1] == id2:
            continue
        loc2 = (latt2,long2)
        duration = (time2 - time1).days
        if duration < 0:
            continue
        if duration > 5:
            break
        dist = great_circle(loc1, loc2).kilometers
        if dist > 0 and dist < 10 and duration > 0 and duration <= 5:
            # relationship id
            y_index += 1
            pcset[id1] = id2
            rel_id += 1
            result_excel(rel_id,fam_id,id1,id2,depth,latt1,long1,latt2,long2,duration,dist)
            childfinder(trial[count+1:], otherchildren,depth,fam_id,rel_id)
            continue


def data_split(node):
    parent = node.strip()
    id, time, latt, long = parent.split(',')
    return int(id), datetime.strptime(time, '%d-%b-%y'), float(latt), float(long)


def excel_init():
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



def result_excel(Rel_ID, Fam_ID, P_ID, C_ID, Depth, P_latt, P_long, C_latt, C_long, Dur, Dist):
    outsheet.write(y_index,0, Rel_ID)  # (y,0)
    outsheet.write(y_index,1, Fam_ID)  # (y,1)
    outsheet.write(y_index,2, P_ID)
    outsheet.write(y_index,3, C_ID)
    outsheet.write(y_index,4, Depth)  # (y,2)
    outsheet.write(y_index,5, P_latt)  # (y,3)
    outsheet.write(y_index,6, P_long)
    outsheet.write(y_index,7, C_latt)
    outsheet.write(y_index,8, C_long)
    outsheet.write(y_index,9, Dur)
    outsheet.write(y_index,10, Dist)


#     direction
if __name__ == "__main__":
    main()


""""
 for every child find, trigger the search, then when there arent any more children found, traverse back to the previous parent 
 and do the same, find if there are any other children for the given parent
"""
