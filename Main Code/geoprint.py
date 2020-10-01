import geopandas
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta, date
from itertools import cycle
import seaborn as sns
import glob
import cv2
import subprocess

imagenumber = 0
import numpy as np

# input only csv files not xlsx files

def data_mapper(data, countryname,date,notemptydata):
    global imagenumber
    countryname = countryname.capitalize()
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    country = world[world['name'] == countryname]
    ax = country.plot(color='white', edgecolor='black')
    title = str(countryname) + "\n" + str(date)
    plt.title(title)
    if notemptydata:
        data.plot(ax=ax, kind="scatter", x="Longitude", y="Latitude",
                  s="Casualties", c="colour", colorbar=False,alpha=0.6)
    else:
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
    imagenumber += 1
    nametitle = "../results/NigeriaImages/year1/" + str(countryname) + "." + str(imagenumber).zfill(5) + ".png"
    plt.savefig(nametitle)
    plt.close()

def mapcreate(datafile,country,date):
    data = datafile[datafile["Date"] == date]
    if data.empty:
        data_mapper(data,country,date,False)
    else:
        data_mapper(data,country,date,True)

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
    data["colour"] = colourvalues
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

def init(csv_file,country):
    data = pd.read_csv(csv_file)
    data = addcolorcolumn(data)
    data["Casualties"] = data["Casualties"] + 5
    delta = timedelta(days=1)
    # firstdate index should be index 0
    firstdate = data["Date"].iloc[0]
    lastdate = data["Date"].iloc[-1]
    start = str(datechange(firstdate)).split("-")
    end = str(datechange(lastdate)).split("-")
    start_date = date(int(start[0]), int(start[1]), int(start[2]))
    end_date = date(int(end[0]), int(end[1]), int(end[2]))
    while start_date <= end_date:
        converteddate = dateconvertback(start_date)
        mapcreate(data,country,converteddate)
        start_date += delta
    print("Done")


def videocreate():
    input = r"C:\Users\k2kis\Desktop\Research\Code\results\NigeriaImages\year1\Nigeria.%05d.png"
    output = r"C:\Users\k2kis\Desktop\Research\Code\results\out.mp4"
    frame_rate = 6
    cmd = f'ffmpeg -framerate {frame_rate} -i "{input}" "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=True)

def main():
    print(datetime.now())
    init("../results/1yeardatanigeria.csv","Nigeria")
    videocreate()
    print(datetime.now())






