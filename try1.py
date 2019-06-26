#!/usr/bin/env python3

"""BY megha sharma
to convert text files into netCDF files
considering map of india by using data provided in ascii format with spaces as delimiter
"""

# import important libraries mainly netCDF4(Dataset) and numpy
from netCDF4 import Dataset
import numpy as np
import os
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import meshgrid


count = 0

# choosing the year to convert
yr = input("enter the year")
def year():
    return yr
lat_num=0
lon_num=0
def get_lat(value_lat):
    while(lat_num<129):
        if(latitudes[lat_num] == value_lat):
            break
    return lat_num
def get_lon(value_lon):
    while(lon_num<135):
        if(longitudes[lon_num] == value_lon):
            break
    return lon_num



#creating the nc file
root_grp = Dataset("IND_Rainfall_"+year()+".nc", "w", format="NETCDF4")
print (root_grp.data_model)


#creating dimensions

day = root_grp.createDimension("day", 365)
lat = root_grp.createDimension("lat", 129)
lon = root_grp.createDimension("lon", 135)
#print (root_grp.dimensions)


day = root_grp.createVariable("day","i4",("day",))
latitudes = root_grp.createVariable("lat","f4",("lat",))
longitudes = root_grp.createVariable("lon","f4",("lon",))
latitudes.units = "degrees north"
longitudes.units = "degrees east"
day.units = "number of days since the start of the year"

# two dimensions unlimited
rain = root_grp.createVariable('rain',"f4",('day','lat','lon'))
#print(root_grp.variables)

# to put in values
array1 = []  #array1 is the array which will store variable values for longitudes
array2 = []  #array2 is the array which will store variable values for latitudes




#taking data from text file
with open("/home/lydia/Desktop/project/IND"+year()+"_rfP25.TXT",'r') as f:
    data = np.loadtxt(f, dtype = 'f4', unpack = True)


    # for latitudes
    while ( count < 129 ):
        array2.insert( count , data[0][count+1] )
        count = count +1
    latitudes[:] = array2
#    print (latitudes[20])


    # for longitudes
    count = 0
    while ( count < 135 ):
        array1.insert( count , data[count+1][0] )
        count = count +1
    longitudes[:] = array1
#    print (longitudes[20])

    #for day
    days = np.arange(1,366,1)
    array3 = np.zeros((365,129,135))
    #assigning rainfall values
    day_count = 0
    count1 = 0
    count3 = 0
    while (day_count<365):
        while (count1 < 47450):
            if ((count1)%130 == 0 ):
                if (count1 != 0 ):
                    day_count = day_count +1
                count1 = count1 + 1
                count3 = 0
            count2 = 0
            while (count2 < 135):
                array3[ day_count , count3 , count2 ] = data[count2 + 1][count1]
                if (array3[ day_count , count3 , count2 ] < 0):
                    array3[ day_count , count3 , count2 ] = 0.0
                count2 = count2 + 1
            count1 = count1 + 1
            count3 = count3 + 1
        if (day_count == 364):
            break
    rain[:,:,:] = array3
    print(rain[227,50,52])
    f.close()
    # to plot the values
"""    map = Basemap(projection='merc',llcrnrlon=66.5,llcrnrlat=6.5,urcrnrlon=100,urcrnrlat=38.5,resolution='i')

    map.drawcoastlines(linewidth = 1,color='#000000')
    map.drawstates(linewidth = 1,color='#000000')
    map.drawcountries(linewidth = 1,color='#000000')
    x = longitudes[:]
    y = latitudes[:]
    val= int(input("enter day:"))
    xx, yy = meshgrid(x, y)

    ny = rain.shape[1]
    nx = rain.shape[2]
    lon, lat = map.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
    x, y = map(lon, lat) # compute map proj coordinates.
    clevs = [0,0.00001,25,50,100,150,200,250,300,350,400,450,500] #considering high rainfall only
    onthemap = map.contourf(x,y,rain[(val-1),:,:], clevs ,colors=['#ffffff','#87ceeb','#0000FF','#008000','#FFFF00','#FFA500','#FF0000','#800080','#ff0090','#39ff14','#b47767','#000000'], corner_mask =  True)
    cb = map.colorbar(onthemap,"bottom", size="5%", pad="2%")
    plt.title("rain")
    cb.set_label("rain(mm)")
    plt.figure(figsize=(20,10))
    plt.show()
"""



root_grp.close()
print ("END")
print ("check the file in your working directory")
#file will be saved in the working directory
#the resulting array will be in the form of arr(day,lat,lon) where day, lat ,lon are indexes of the required data
#os.remove("/home/lydia/IND_Rainfall_"+year()+".nc")
