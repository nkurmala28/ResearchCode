# import geopandas
# import xlsxwriter as xw
#
# # input your own directory and name where the result will be saved
#
# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# names = world["name"]
#
# workbook = xw.Workbook('C:/Users/k2kis/Desktop/Research/Code/Results/GP_Countrylist.xlsx')
# outsheet = workbook.add_worksheet(name="Countries")
# outsheet.write("A1", "Family ID")
# yindex = 0
# for country in names:
#     yindex += 1
#     outsheet.write(yindex,0,country)
#
# workbook.close()

a = []
if not a:
    print(1)
else:
    print(2)