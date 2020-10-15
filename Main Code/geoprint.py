import geopandas
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta, date
from itertools import cycle
import seaborn as sns
import subprocess

# input only csv files not xlsx files

imagenumber = 0


def data_mapper(data, countryname, date, notemptydata):
    global imagenumber
    # countryname = countryname.capitalize()
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    country = world[world['name'] == countryname]
    ax = country.plot(color='white', edgecolor='black')
    title = str(countryname) + "\n" + str(date)
    plt.title(title)
    if notemptydata:
        data.plot(ax=ax, kind="scatter", x="Longitude", y="Latitude",
                  s="Casualties", c="Colour", colorbar=False, alpha=0.6)
    else:
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
    imagenumber += 1
    imagename = countryname.replace(".",'').replace(" ","-")
    picture_storage_location = "../Results/DemRepCongo/Images/" + str(imagename) + "." + str(imagenumber).zfill(
        6) + ".png"
    plt.savefig(picture_storage_location)
    plt.close()


def mapcreate(datafile, country, date):
    data = datafile[datafile["Date"] == date]
    if data.empty:
        data_mapper(data, country, date, False)
    else:
        data_mapper(data, country, date, True)



def addcolorcolumn(data):
    clrs = sns.color_palette("Paired")
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
    data = data[:100]
    data = addcolorcolumn(data)
    data["Casualties"] = data["Casualties"] + 5
    start_date, end_date = start_end_date_return(data)
    delta = timedelta(days=1)
    #do a ting where add 2 extra dates to start date and check if you can print 3 days each time
    #check if you can do varying transparency like how we did colours = id
    #CHANGE OF PLAN
    # DO THE DATE thing at the map create function since the data we parse doesnt have all the dates in
    #we can individual just add them to a different dataframe for analysis
    while start_date <= end_date:
        converteddate = dateconvertback(start_date)
        mapcreate(data, country, converteddate)
        start_date += delta
    print("Done")


def videocreate():
    # input has to change based on the country used
    input = r"C:\Users\k2kis\Desktop\Research\Code\Results\DemRepCongo\Images\Dem Rep Congo.%06d.png"
    output = r"C:\Users\k2kis\Desktop\Research\Code\Results\DemRepCongo\300km_Congo_Video.mp4"
    frame_rate = 5
    cmd = f'ffmpeg -framerate {frame_rate} -i "{input}" "{output}"'
    subprocess.check_output(cmd, shell=True)


def main():
    print(datetime.now())
    # must be csv
    init("../Results/CongoData.csv", "Dem. Rep. Congo")
    videocreate()
    print(datetime.now())


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
