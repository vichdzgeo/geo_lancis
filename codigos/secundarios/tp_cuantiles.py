import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import osr

def ecuacion_class(cortes):
    n_cortes = len(cortes)
    ecuacion =''
    for i in range(n_cortes):
        if i < n_cortes-2: 
            ecuacion+='logical_and(A>='+str(cortes[i])+',A<='+str(cortes[i+1])+')*'+str(i+1)+' + '
        elif i== n_cortes-2 :
            ecuacion+='logical_and(A>='+str(cortes[i])+', A<='+str(round(float(cortes[i+1]),1))+')*'+str(i+1)
        
    return ecuacion
    
def cuantiles(path_r,quantil):
    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimesion = band1.shape
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band2= band1[band1 != nodata_r]
    band2 = band2.flatten()
    lista_val = [0,]
    
    for i in range(1,quantil+1):
        #print (i,i/quantil)
        valor= i/quantil
        cuantil_c = np.quantile(band2,valor)
        lista_val.append(cuantil_c)

    return lista_val
