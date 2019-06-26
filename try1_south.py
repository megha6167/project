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

# choosing the year to convert
yr = input("enter the year")
def year():
    return yr


    #for future edits

"""lat_num=0
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
    return lon_num"""



#creating the nc file
root_grp = Dataset("IND_Rainfall_south"+year()+".nc", "w", format="NETCDF4")
print (root_grp.data_model)


#creating dimensions

day = root_grp.createDimension("day", 365)
lat = root_grp.createDimension("lat", 38)
lon = root_grp.createDimension("lon", 51)
#print (root_grp.dimensions)



day = root_grp.createVariable("day","i4",("day",))
latitudes = root_grp.createVariable("lat","f4",("lat",))
longitudes = root_grp.createVariable("lon","f4",("lon",))
latitudes.units = "degrees north"
longitudes.units = "degrees east"
day.units = "number of days since the start if the year"

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
    count = 0
    while ( count < 38 ):
        array2.insert( count , data[0][count+1] )
        count = count +1
    latitudes[:] = array2


    # for longitudes
    count = 0
    while ( count < 51 ):
        array1.insert( count , data[count+23][0] )
        count = count +1
    longitudes[:] = array1

    #for day
    days = np.arange(1,366,1)
    array3 = np.zeros((365,38,51))
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
            if (count1<(130*day_count+38)):
                while (count2 < 51):
                    array3[ day_count , count3 , count2 ] = data[count2 + 23][count1]
                    if (array3[ day_count , count3 , count2 ] < 0):
                        array3[ day_count , count3 , count2 ] = 0.0
                    count2 = count2 + 1
            count1 = count1 + 1
            count3 = count3 + 1
        if (day_count == 364):
            break
    rain[:,:,:] = array3
    f.close()
    # to plot the values
    map = Basemap(projection='merc',llcrnrlon=72.0,llcrnrlat=6.5,urcrnrlon=84.5,urcrnrlat=15.75,resolution='i')

  #  map.drawcoastlines()
    map.drawstates()
    map.drawcountries()
    x = longitudes[:]
    y = latitudes[:]
    val= int(input("enter day:"))
    xx, yy = meshgrid(x, y)

    ny=38
    nx=51
    lon, lat = map.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
    x, y = map(lon, lat) # compute map proj coordinates.
    clevs = [0,0.00001,25,50,100,150,200,250,300,350,400,450,500] #considering high rainfall only
    onthemap = map.contourf(x,y,rain[(val-1),:,:], clevs ,colors=['#ffffff','#87ceeb','#0000FF','#008000','#FFFF00','#FFA500','#FF0000','#800080','#ff0090','#39ff14','#b47767','#000000'], corner_mask =  True)
    cb = map.colorbar(onthemap,"bottom", size="5%", pad="2%")
    plt.title("rain")
    cb.set_label("rain(mm)")
    plt.show()




root_grp.close()
print ("END")
print ("check the file in your working directory")
#file will be saved in the working directory
#the resulting array will be in the form of arr(day,lat,lon) where day, lat ,lon are indexes of the required data
#os.remove("/home/lydia/IND_Rainfall_south"+year()+".nc")
