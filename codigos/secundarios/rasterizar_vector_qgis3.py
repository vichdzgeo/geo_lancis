# -*- coding: utf-8 -*-
'''
Este script funciona para convertir un vector en raster, el vector debe
estar en la proyeccion UTM Z16N "EPSG:32616". El raster resultante
hereda los parametros del extent 3
'''

from osgeo import gdal, osr
import numpy as np
import processing
from qgis.core import QgsRasterLayer
from PyQt5.QtCore import QFileInfo
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.analysis import *


layer = iface.activeLayer()
path = layer.dataProvider().dataSourceUri()

path_vector =layer.dataProvider().dataSourceUri()
path_salida = layer.dataProvider().dataSourceUri().split(".")[0]+".tif"

nombre_campo = 'fv'#nombre del campo del vector que contiene la clase o categorias
valor_nodata = -9999.0## El valor no data
tipo_raster = 'Float32'## El tipo de dato de salida del raster
# Diccionario de tipos de datos perteneciente a qgis


## tipo  de dato que ocupa gdal en su funcion rasterize
RTYPE = { 'Byte': 0, 'Int16': 1, 'UInt16': 2, 'UInt32':3,\
                'Int32':4, 'Float32':5, 'Float64':6 }
## Extent_2 o region de la zona de estudio NO MODIFICAR ESTOS VALORES
xmin = 463960
xmax =  505660
ymin = 2114567
ymax = 2166467
vector = QgsVectorLayer(path_vector,"","ogr")
## llamada a la funcion de gadal rasterize para convertir el vector a una capa raster.
dicc={
    'INPUT':vector,
    'FIELD':nombre_campo,
    'BURN':0,
    'UNITS':0,
    'WIDTH':417,
    'HEIGHT':519,
    'EXTENT':"%f,%f,%f,%f" % (xmin, xmax, ymin, ymax),
    'NODATA':valor_nodata,
    'OPTIONS':'',
    'DATA_TYPE':5,
    'INIT':None,
    'INVERT':False,
    'EXTRA':'',
    'OUTPUT':path_salida}

processing.run("gdal:rasterize", dicc)

