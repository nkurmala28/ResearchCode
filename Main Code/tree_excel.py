import xlsxwriter as xw
from datetime import datetime
from geopy.distance import great_circle

# ALWAYS MAKE SURE THE DATA IS ALREADY PRE ARRANGED FROM PAST TO PRESENT DATE-WISE
# and delete first row if column headers

# input your own dire and name
workbook = xw.Workbook('C:/Users/k2kis/Desktop/Research/Code/results/trialagainA.xlsx')
outsheet = workbook.add_worksheet(name="Data")
pcset = {}
y_index = 0


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
        childfinder(dataset[count + 1:], parent, depth, fam_id, rel_id)
        continue


def childfinder(trial, parent, depth, fam_id, rel_id):
    global y_index, pcset
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
        loc2 = (latt2, long2)
        duration = (time2 - time1).days
        if duration < 0:
            continue
        if duration > 5:
            break
        dist = great_circle(loc1, loc2).kilometers
        if dist >= 0 and dist < 10 and duration > 0 and duration <= 5:
            # relationship id
            y_index += 1
            pcset[id1] = id2
            rel_id += 1
            result_excel(rel_id, fam_id, id1, id2, depth, latt1, long1, latt2, long2, date1, date2, duration, dist,
                         deaths1 + deaths2)
            childfinder(trial[count + 1:], otherchildren, depth, fam_id, rel_id)
            continue


def data_split(node):
    parent = node.strip()
    id, date, latt, long, deaths = parent.split(',')
    return int(id), date, float(latt), float(long), int(deaths)


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
    outsheet.write("J1", "Parent Date")
    outsheet.write("K1", "Child Date")
    outsheet.write("L1", "Duration")
    outsheet.write("M1", "Distance from Children")
    outsheet.write('N1', "Casualties")


def result_excel(Rel_ID, Fam_ID, P_ID, C_ID, Depth, P_latt, P_long, C_latt, C_long, P_date, C_date, Dur, Dist,
                 Casualties):
    outsheet.write(y_index, 0, Rel_ID)  # (y,0)
    outsheet.write(y_index, 1, Fam_ID)  # (y,1)
    outsheet.write(y_index, 2, P_ID)
    outsheet.write(y_index, 3, C_ID)
    outsheet.write(y_index, 4, Depth)  # (y,2)
    outsheet.write(y_index, 5, P_latt)  # (y,3)
    outsheet.write(y_index, 6, P_long)
    outsheet.write(y_index, 7, C_latt)
    outsheet.write(y_index, 8, C_long)
    outsheet.write(y_index, 9, P_date)
    outsheet.write(y_index, 10, C_date)
    outsheet.write(y_index, 11, Dur)
    outsheet.write(y_index, 12, Dist)
    outsheet.write(y_index, 13, Casualties)
    # direction


if __name__ == "__main__":
    main()

