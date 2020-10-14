import geopandas
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta, date
from itertools import cycle
import seaborn as sns
import subprocess

# input only csv files not xlsx files

imagenumber = 0


def data_mapper(data, countryname, date, datelist, notemptydata):
    global imagenumber
    # countryname = countryname.capitalize()
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    country = world[world['name'] == countryname]
    ax = country.plot(color='white', edgecolor='black')
    title = str(countryname) + "\n" + str(date)
    plt.title(title)
    if notemptydata:
        for time in datelist.keys():
            newdata = data[data["Date"] == time]
            if not newdata.empty:
                alpha = datelist[time]
                newdata.plot(ax=ax, kind="scatter", x="Longitude", y="Latitude",
                      s="Casualties", c="Colour", colorbar=False, alpha=alpha)
    else:
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
    imagenumber += 1
    imagename = countryname.replace(".",'').replace(" ",'-')
    picture_storage_location = "../Results/DemRepCongo/Images/" + str(imagename) + "." + str(imagenumber).zfill(
        6) + ".png"
    plt.savefig(picture_storage_location)
    plt.close()


def mapcreate(datafile, country, date):
    result,datelist = addtransparency(datafile,date)
    date = dateconvertback(date)
    if not result.empty:
        data_mapper(result, country, date, datelist, True)
    else:
        data_mapper(result, country, date,datelist, False)

def addtransparency(data,date):
    prevdate = date - timedelta(days=1)
    daybefore = prevdate - timedelta(days=1)
    dates = [dateconvertback(daybefore),dateconvertback(prevdate),dateconvertback(date)]
    trans = [0.2,0.45,0.75]
    dic_trans = {a:b for a,b in zip(dates,trans)}
    finaldata = []
    for DATE in dates:
        newdata = data[data["Date"] == DATE]
        if not newdata.empty:
            finaldata.append(newdata)
    if len(finaldata) != 0:
        result = pd.concat(finaldata)
    else:
        result = pd.DataFrame()
    return result,dic_trans



def addcolorcolumn(data):
    clrs = sns.color_palette("Set1")
    famids = data["Family ID"].unique()
    zip_list = zip(famids, cycle(clrs)) if len(famids) > len(clrs) else zip(cycle(famids), clrs)
    colourlist = list(zip_list)
    colours = {}
    for id, colour in colourlist:
        colours[id] = colour
    colours[0] = "black"
    colourvalues = [colours[i] for i in list(data["Family ID"])]
    data["Colour"] = colourvalues
    return data


def datechange(date):
    # 2000-12-22
    return datetime.strptime(date, '%d-%b-%y').date()


def dateconvertback(date):
    # 27-May-00
    months = {1: 'Jan',
              2: 'Feb',
              3: 'Mar',
              4: 'Apr',
              5: 'May',
              6: 'Jun',
              7: 'Jul',
              8: 'Aug',
              9: 'Sep',
              10: 'Oct',
              11: 'Nov',
              12: 'Dec'}
    datelist = str(date).split("-")
    return str(int(str(datelist[-1]))) + "-" + str(months[int(datelist[1])]) + "-" + str(datelist[0][2:])


def start_end_date_return(data):
    firstdate = data["Date"].iloc[0]
    lastdate = data["Date"].iloc[-1]
    start = str(datechange(firstdate)).split("-")
    end = str(datechange(lastdate)).split("-")
    start_date = date(int(start[0]), int(start[1]), int(start[2]))
    end_date = date(int(end[0]), int(end[1]), int(end[2]))
    return start_date, end_date


def init(csv_file, country):
    data = pd.read_csv(csv_file)
    data = addcolorcolumn(data)
    data["Casualties"] = data["Casualties"] + 5
    start_date, end_date = start_end_date_return(data)
    delta = timedelta(days=1)
    end_date = end_date + delta + delta
    while start_date <= end_date:
        mapcreate(data, country, start_date)
        start_date += delta
    print("Done Creating Images")


def videocreate():
    # input has to change based on the country used
    input = r"C:\Users\k2kis\Desktop\Research\Code\Results\DemRepCongo\Images\Dem-Rep-Congo.%06d.png"
    output = r"C:\Users\k2kis\Desktop\Research\Code\Results\DemRepCongo\20y_Congo_Video.mp4"
    frame_rate = 6
    cmd = f'ffmpeg -framerate {frame_rate} -i "{input}" "{output}"'
    subprocess.check_output(cmd, shell=True)


def main():
    print(datetime.now())
    # must be csv
    init("../Results/CongoData.csv", "Dem. Rep. Congo")
    videocreate()
    print(datetime.now())
    print("End of Script")


if __name__ == "__main__":
    main()

#TAKE NOTE
#When Country NAME HAS . IN IT, DONT USE THE CAPITALISE FUNCTION

# IMPROVEMENTS
# need to add argument in mapper to plot points of natural resources

# CHANGES WHEN NEEDED
# change the string of storage location of nametitle inside data_mapper function (location where the pic are stored)
# change the init string inside main function based on the location of the datafile
# change the input and output string in videocreate function


#     took 30 mins for 20 year video
