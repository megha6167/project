#!/usr/bin/env python3

"""BY megha sharma
to convert text files into netCDF files
considering map of india by using data provided in ascii format with spaces as delimiter
"""

# import important libraries mainly netCDF4(Dataset) and numpy
from netCDF4 import Dataset
import numpy as np
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
root_grp = Dataset("IND_Rainfall_"+year()+".nc", "w", format="NETCDF4")
print (root_grp.data_model)


#creating dimensions

time = root_grp.createDimension("time", 365)
lat = root_grp.createDimension("lat", 129)
lon = root_grp.createDimension("lon", 135)
#print (root_grp.dimensions)

#variables
times = root_grp.createVariable("time","i4",("time",))
latitudes = root_grp.createVariable("lat","f4",("lat",))
longitudes = root_grp.createVariable("lon","f4",("lon",))


# two dimensions unlimited
prcp = root_grp.createVariable('prcp',"f4",('time','lat','lon'))


#attributes
root_grp.description = "a netCDF4 file containing information about the daily rainfall pattern of india of year" + year()
root_grp.history = "created in july 2019 as a summer project"
root_grp.source = "created by using data provided by IMD"
latitudes.units = "degrees north"
longitudes.units = "degrees east"
times.units = "number of days since the start of the year"
times.description = "a day starts at 0300 UTC, which is, 0830 am in India.So,for an example, the rainfall data of 16 August 2018 is the amount of rainfall since 15 August 2018 0300 UTC till 16 August 2018 0300 UTC"
prcp.units = "millimetres of rainfall on the specified day"

root_grp.set_auto_mask(False)


# to put in values
array1 = []  #array1 is the array which will store variable values for longitudes
array2 = []  #array2 is the array which will store variable values for latitudes


#TAKING OUT DATA AND PUTTING IN OUR FILE

#taking data from text file
with open("/home/lydia/Desktop/project/IND"+year()+"_rfP25.TXT",'r') as f:
    data = np.loadtxt(f, dtype = 'f4', unpack = True)


    # for latitudes
    count = 0
    while ( count < 129 ):
        array2.insert( count , data[0][count+1] )
        count = count +1
    latitudes[:] = array2


    # for longitudes
    count = 0
    while ( count < 135 ):
        array1.insert( count , data[count+1][0] )
        count = count +1
    longitudes[:] = array1


    #for time
    times = np.arange(1,366,1)


    #assigning rainfall values
    array3 = np.zeros((365,129,135))
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
    prcp[:,:,:] = array3
    f.close()





# PLOTTING THE DATA ON THE MAP


    #creating the map
    map = Basemap(projection='merc',llcrnrlon=66.5,llcrnrlat=6.5,urcrnrlon=100,urcrnrlat=38.5,resolution='i')


    #details
    map.drawcoastlines(linewidth = 1,color='#000000')
    map.drawstates(linewidth = 1,color='#000000')
    map.drawcountries(linewidth = 1,color='#000000')
    #to draw longitudes
    map.drawmeridians(np.arange(66.5,100,2),color='#414141',labels=[0,0,0,1],linewidth=0.5)
    #to draw latitudes
    map.drawparallels(np.arange(6.5,38.5,2),color='#414141',labels=[1,0,0,0],linewidth = 0.5)

    val= int(input("enter day:"))

    #plotting contour
    ny = prcp.shape[1]
    nx = prcp.shape[2]
    lon, lat = map.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
    x, y = map(lon, lat) # compute map proj coordinates.
    clevs = [0,0.00001,25,50,100,150,200,250,300,350,400,450,500] #changed after suggestion
    onthemap = map.contourf(x,y,prcp[(val-1),:,:], clevs ,colors=['#ffffff','#87ceeb','#0000FF','#008000','#FFFF00','#FFA500','#FF0000','#800080','#ff0090','#39ff14','#b47767','#000000'], corner_mask =  True)
    cb = map.colorbar(onthemap,"right", size="5%", pad="2%")
    plt.title("Precipitation")
    cb.set_label("prcp(mm)")
    plt.show()




root_grp.close()
print ("END")
print ("check the file in your working directory")
#file will be saved in the working directory
#the resulting array will be in the form of arr(day,lat,lon) where day, lat ,lon are indexes of the required data
#os.remove("/home/lydia/IND_Rainfall_"+year()+".nc")
