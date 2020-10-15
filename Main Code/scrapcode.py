
import geopandas
from matplotlib import pyplot as plt
from descartes import PolygonPatch
import seaborn as sns
from itertools import cycle

clrs = sns.color_palette("Set1")
print(list(clrs))
# def plotCountryPatch( axes, country_name, fcolor ):
#     # plot a country on the provided axes
#     nami = world[world.name == country_name]
#     namigm = nami.__geo_interface__['features']  # geopandas's geo_interface
#     namig0 = {'type': namigm[0]['geometry']['type'], \
#               'coordinates': namigm[0]['geometry']['coordinates']}
#     axes.add_patch(PolygonPatch( namig0, fc=fcolor, ec="black", alpha=0.15, zorder=2 ))


# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# ax = world[world.continent == "Africa"].plot(color='white', edgecolor='black')
# plt.xlim(right=41)
# plt.xlim(left=12)
# plt.ylim(top=5.1)
# plt.ylim(bottom=-13.2)
#
# plotCountryPatch(ax, 'Tanzania', 'grey')
# plotCountryPatch(ax, 'Burundi', 'grey')
# plotCountryPatch(ax, 'Rwanda', 'grey')
# plotCountryPatch(ax, "Dem. Rep. Congo", 'grey')
# plotCountryPatch(ax, 'Uganda', 'grey')
