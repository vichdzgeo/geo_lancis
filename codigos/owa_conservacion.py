import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import osr
from owagis import *

## insumos###
path_datos = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/poety_aptitud/funciones_valor/conservacion.csv'
prefijo = 'conservacion'

## Ruta del directorio y prefijo que tendran los resultados 
path_salida = "C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/apc_temeraria/owa/procesamiento/"+prefijo

## lista de valores que toma alpha, para cada valor genera una salida
#owa_alphas = [0.0001,0.1,0.5,1.0,2.0,5.0,10.0,1000.0]
owa_alphas = [0.1,0.5,1.0,2.0,10.0]
print ("procesando owa",time.strftime("%H:%M:%S"))  #imprime la hora que inicia el proceso
genera_owa(path_datos,owa_alphas,path_salida)
print (time.strftime("%H:%M:%S"))  # imprime la hora una vez terminada la ejecución