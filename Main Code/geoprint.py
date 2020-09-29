import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import glob
import cv2


# input only csv files not xlsx files

def data_mapper(csv_file, countryname,imagenumber,start,end):
    countryname = countryname.capitalize()
    data = pd.read_csv(csv_file)

    uniqueIDs = data["Family ID"].unique()
    # print(len(data["Family ID"].unique()))

    data = data[start:end+1]
    startdate = data["Date"][start]
    enddate = data["Date"][end]
    # adding 5 to the casualties in order to make sure points with they appear
    data["Casualties"] = data["Casualties"] + 5
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    country = world[world['name'] == countryname]
    ax = country.plot(color='white', edgecolor='black')
    data.plot(ax=ax, kind="scatter", x="Longitude", y="Latitude",
              s="Casualties", c="Family ID", cmap=plt.get_cmap("jet"), colorbar=True,
              alpha=1)
    title = str(countryname) + "\n" + str(startdate) + ' - ' + str(enddate)
    plt.title(title)

    # diagram_dir = "../results/" + str(title) + ".png"
    # plt.savefig(diagram_dir.replace("\n","-"))

    nametitle = "../results/NigeriaImages/1999/" + str(countryname) + str(imagenumber) + ".png"
    plt.savefig(nametitle)


def mapcreate(step,lengthoffile):
    start = 0
    end = step
    imagenumber = 0
    while step <= lengthoffile:
        lengthoffile -= step
        imagenumber += 1
        data_mapper("../results/20yearfamilydata_Nigeria.csv", "nigeria",imagenumber, start,end)
        start += step
        end += step
    if lengthoffile != 0:
        imagenumber += 1
        data_mapper("../results/20yearfamilydata_Nigeria.csv", "nigeria",imagenumber,start, start + lengthoffile)

# 14489 length, 2306 unique family ids
# create unique colours for each family id
#SLIDE SHOW SHOULD ALSO HAVE DAYS WHERE NOTHING HAPPENED

mapcreate(1,1)

# img_array = []
# for filename in glob.glob('C:/New folder/Images/*.jpg'):
#     img = cv2.imread(filename)
#     height, width, layers = img.shape
#     size = (width, height)
#     img_array.append(img)
#
# out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
#
# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()










