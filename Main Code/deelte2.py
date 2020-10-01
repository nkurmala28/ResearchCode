import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas
import numpy as np
from itertools import cycle

def createcolorcolumn(data):
    NUM_COLORS = 15
    clrs = sns.color_palette('husl', n_colors=NUM_COLORS)
    famids = data["Family ID"].unique()
    zip_list = zip(famids, cycle(clrs)) if len(famids) > len(clrs) else zip(cycle(famids), clrs)
    colourlist = list(zip_list)
    colours = {}
    for id, colour in colourlist:
        colours[id] = colour
    colourvalues = [colours[i] for i in list(data["Family ID"])]
    data["colours"] = colourvalues
    return data


NUM_COLORS = 15

sns.reset_orig()  # get default matplotlib styles back
clrs = sns.color_palette('husl', n_colors=NUM_COLORS)  # a list of RGB tuples
# for i in range(NUM_COLORS):
    # print(clrs[i])


data = pd.read_csv("../results/1yeardatanigeria.csv")

a = data["Date"][0]
b = "1-Jan-00"
print(int("05"))
print(b)
print(a==b)
# data = data
# A = data["Family ID"].unique()
# zip_list = zip(A, cycle(clrs)) if len(A) > len(clrs) else zip(cycle(A), clrs)
# ans = list(zip_list)
# colours = {}
# for id,colour in ans:
#     colours[id] = colour
# # print(colours)
#
# # data["colours"] = np.where(colours[data["Family ID"]])
# values = [colours[i] for i in list(data["Family ID"])]
# data["colours"] = values
# print(data.head())
#
# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# country = world[world['name'] == "Nigeria"]
# ax = country.plot(color='white', edgecolor='black')
#
# data.plot(ax=ax, kind="scatter", x="Longitude", y="Latitude",
#               s="Casualties", c="colours")
# plt.show()