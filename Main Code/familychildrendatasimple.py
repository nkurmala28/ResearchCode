import xlsxwriter as xw
from datetime import datetime
from geopy.distance import great_circle

# ALWAYS MAKE SURE THE DATA IS ALREADY PRE ARRANGED FROM PAST TO PRESENT DATE-WISE
# and delete first row if column headers

# input your own dire and name
workbook = xw.Workbook('C:/Users/k2kis/Desktop/Research/Code/results/trialagainB2.xlsx')
outsheet = workbook.add_worksheet(name="Data")
pcset = {}
y_index = 0
orphan = True
notorphans = set()

def main():
    print(datetime.now())
    excel_init()
    parent_child_finder("../Data/Nigeria20years.csv")
    workbook.close()
    print(datetime.now())
    pass


def parent_child_finder(filename):
    fileopen = open(filename)
    dataset = fileopen.readlines()
    count = 0
    fam_id = 0
    rel_id = 0
    for parent in dataset:
        fam_id += 1
        rel_id += 1000
        count += 1
        depth = 0
        global orphan, y_index, notorphans
        orphan = True
        id1, date1, latt1, long1, deaths1 = data_split(parent)
        if id1 in notorphans:
            continue
        childfinder(dataset[count:], parent, depth, fam_id, rel_id)
        if not orphan:
            y_index += 1
            notorphans.add(id1)
            result_excel(fam_id, latt1, long1, date1, deaths1,id1)
        else:
            y_index += 1
            result_excel(0, latt1, long1, date1, deaths1,id1)
        continue


def childfinder(trial, parent, depth, fam_id, rel_id):
    global y_index, pcset,orphan, notorphans
    id1, date1, latt1, long1, deaths1 = data_split(parent)
    time1 = datetime.strptime(date1, '%d-%b-%y')
    loc1 = (latt1, long1)
    count = 0
    depth += 1
    for otherchildren in trial:
        count += 1
        id2, date2, latt2, long2, deaths2 = data_split(otherchildren)
        time2 = datetime.strptime(date2, '%d-%b-%y')
        if id1 in pcset and pcset[id1] == id2:
            continue
        if id2 in notorphans:
            continue
        # look into the above checks for tree_exvel
        loc2 = (latt2, long2)
        duration = (time2 - time1).days
        if duration < 0:
            continue
        if duration > 5:
            break
        dist = great_circle(loc1, loc2).kilometers
        if dist >= 0 and dist <= 10 and duration >= 0 and duration <= 5:
            # fix the above in tree excel
            y_index += 1
            pcset[id1] = id2
            rel_id += 1
            orphan = False
            result_excel(fam_id, latt2, long2, date2, deaths2,id2)
            notorphans.add(id2)
            childfinder(trial[count:], otherchildren, depth, fam_id, rel_id)
            continue



def data_split(node):
    parent = node.strip()
    id, date, latt, long, deaths = parent.split(',')
    return int(id), date, float(latt), float(long), int(deaths)


def excel_init():
    outsheet.write("A1", "Family ID")  # (y,1)
    outsheet.write("B1", "Latitude")  # (y,3)
    outsheet.write("C1", "Longitude")
    outsheet.write("D1", "Date")
    outsheet.write('E1', "Casualties")
    outsheet.write("F1","ID")


def result_excel(Fam_ID,P_latt, P_long,P_date,Casualties,ID):
    outsheet.write(y_index, 0, Fam_ID)  # (y,1)
    outsheet.write(y_index, 1, P_latt)  # (y,3)
    outsheet.write(y_index, 2, P_long)
    outsheet.write(y_index, 3, P_date)
    outsheet.write(y_index, 4, Casualties)
    outsheet.write(y_index,5,ID)
    # direction


if __name__ == "__main__":
    main()

