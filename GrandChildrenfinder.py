import geopy
import xlsxwriter as xw
from datetime import datetime
from geopy import distance
from geopy.distance import great_circle

fileopen = open("Parent_Child.csv")
fileopen.readline()
file1 = fileopen.readlines()
file2 = open("data1.csv").readlines()

#fingure out how to write to exisitng file
workbook = xw.Workbook('GCData.xlsx')
outsheet = workbook.add_worksheet(name="Data1")
outsheet.write("A1", "Parent Incident Date") #(y,0)
outsheet.write("B1", "Children Incident Date") #(y,1)
outsheet.write("C1", "Latitude")
outsheet.write("D1", "Longitude")
outsheet.write("E1", "Duration")#(y,2)
outsheet.write("F1", "Distance from Parent")#(y,3)
outsheet.write("G1", "Grandchild Incident Date")
outsheet.write("H1", "Latitude")
outsheet.write("I1", "Longitude")
outsheet.write("J1","Duration")
outsheet.write("K1","Distance from Children")

def fac(x):
    prd = 1
    for i in range(1,x+1):
        prd = prd*i
    return prd
num = 0
for line in file1:
    num += 1
count = 0
y_index = 0
currenttime = 0
while count < num:              #1 are parents, #2 are children
    for line in file1:
        line = line.rstrip()
        parentdate,childrendate,latt,long,duration1,distance1 = line.split(',')
        datetime1 = datetime.strptime(childrendate,'%d-%b-%y')
        loc1 = (float(latt),float(long))
        count += 1
        for row in file2:
            row = row.rstrip()
            time2,latt2,long2 = row.split(',')
            datetime2 = datetime.strptime(time2,'%d-%b-%y')
            loc2 = (float(latt2),float(long2))
            duration = (datetime2-datetime1).days
            if duration < 0:
                continue
            dist = great_circle(loc1,loc2).kilometers
            if dist > 0 and dist < 10 and duration > 0 and duration <= 5:
                y_index += 1
                if currenttime != childrendate:
                    outsheet.write(y_index, 1, childrendate)
                    outsheet.write(y_index, 2, latt)
                    outsheet.write(y_index, 3, long)
                    currenttime = childrendate
                outsheet.write(y_index, 0, parentdate)
                outsheet.write(y_index, 4, duration1)
                outsheet.write(y_index, 5, distance1)
                outsheet.write(y_index, 6, time2)
                outsheet.write(y_index, 7, latt2)
                outsheet.write(y_index, 8, long2)
                outsheet.write(y_index, 9, duration)
                outsheet.write(y_index, 10, dist)


workbook.close()


