import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import geoplot
import mapclassify

data_nig = pd.read_csv("../results/20yeardata.csv")
data_nig.drop(["Depth","Child Date"],axis=1,inplace=True)
# data_nig = data_nig[:25]
# adding 5 to the casualties in order to make sure they appear
data_nig["Casualties"] = data_nig["Casualties"] + 5
print(data_nig)

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
nig = world[world['name'] == "Nigeria"]
ax = nig.plot(color='white', edgecolor='black')
data_nig.plot(ax=ax, kind="scatter", x="Parent Longitude", y="Parent Latitude",
              s=data_nig["Casualties"], c=data_nig["Family ID"]/100,cmap=plt.get_cmap("jet") ,colorbar=True, alpha = 0.6)

plt.show()




# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# nig = world[world['name'] == "Nigeria"]
# gdf = geopandas.GeoDataFrame(data_nig[:], geometry=geopandas.points_from_xy(data_nig['Parent Longitude'][:], data_nig["Parent Latitude"][:]))
# ax = nig.plot(color='white', edgecolor='black')
# gdf.plot(ax=ax, color='red', markersize=6)
#
# plt.ylabel("Latitude", fontsize=14)
# plt.xlabel("Longitude", fontsize=14)
# plt.show()









# ........................................................
# variable markersize workaround
# for i in range(0,len(GeoDataFrame)):
# GeoDataFrame.geometry.iloc[i:i+1].plot(ax = ax, markersize = GeoDataFrame['Marker Size'].iloc[i])


