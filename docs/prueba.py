import os
import sys
#sys.path.insert(0, os.path.abspath('../'))
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/share/gdal')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/bin/gdalplugins')
# sys.path.insert(0, 'C:/OSGEO4~1/share/epsg_csv')
# sys.path.insert(0, 'C:/OSGEO4~1')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis-ltr/bin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/pymod3/scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/Scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/bin')
# sys.path.insert(0, 'C:/Program Files/MiKTeX 2.9/miktex/bin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python27/Scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/bin;C:/WINDOWS/system32')
# sys.path.insert(0, 'C:/WINDOWS')
# sys.path.insert(0, 'C:/WINDOWS/system32/WBem')
# sys.path.insert(0, 'C:/Program Files/R/R-3.6.0/bin/x64')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/pywin32_system32')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/numpy/.libs')
# sys.path.insert(0, 'C:/OSGEO4~1/share/proj')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/pymod3/scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/pymod3/lib/site-packages')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/Scripts')
# sys.path.insert(0, 'C:/OSGEO4~1')


# sys.path.insert(0, 'C:/OSGEO4~1/share/gdal')
# sys.path.insert(0, 'C:/OSGEO4~1/bin')
# sys.path.insert(0, 'C:/OSGEO4~1/bin/gdalplugins')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis/bin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/DLLs')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/pymod3/Lib/site-packages/osgeo')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/win32')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/win32/lib')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/pythonwin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/numpy')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/Scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis/python/plugins')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis-dev/python')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis-dev/python/plugins')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/pymod3/scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/gdal2/pymod3/Lib/site-packages')
# sys.path.insert(0, 'C:/OSGeo4W64/apps/gdal2/pymod3/Lib/site-packages')
# sys.path.insert(0, 'C:/OSGeo4W64/apps/gdal2/pymod3/Lib/site-packages/osgeo')
# sys.path.insert(0, 'C:/OSGeo4W64/apps/gdal2/pymod3/scripts/')

import qgis 
import qgis.core
def saludo():
    '''esta funcion imprime hola
    '''
    print ("hola")

print ("prueba de qgis")

def vector(path_raster):
    '''
    esta función crea un objeto de una capa
    vetorial

    :param path_raster: Ruta del archivo shape
    :type path_raster: String

    '''
    layer = qgis.core.QgsVectorLayer(path_raster,"","ogr")
    return layer

vector = vector("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/agebs_coordendas_paralelas/agebs_cdmx.shp")

from osgeo import gdal
import gdal_calc
dataset = gdal.Open("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/merida_241019/tp_exposicion_total.tif", gdal.GA_ReadOnly)
if dataset:
    print ("aaaaa")
# for poligono in vector.getFeatures():
#     print (poligono['id'])

def crea_capa(ecuacion,rasters_input,salida): 

    '''
    Esta función crea una capa mediante la calculadora raster
    de GDAL, esta función esta limitada hasta 8 variables en la ecuación.

    :param ecuacion: ecuación expresada en formato gdal, es este caso es la salida de la funcion *ecuacion_clp*
    :type ecuacion: String
    :param rasters_input: lista de los paths de los archivos rasters, salida de la función `*separa_ruta_pesos*
    :type rasters_input: lista
    :param salida: ruta con extensión tiff de la salida
    :type salida: String
    '''
    path_A=''
    path_B=''
    path_C=''
    path_D=''
    path_E=''
    path_F=''
    path_G=''
    path_H=''
    total_raster = len(rasters_input)
    
    for a,b in zip(range(total_raster), rasters_input):
        if a == 0:
            path_A=b
        elif a == 1:
            path_B=b
        elif a == 2:
            path_C=b
        elif a == 3:
            path_D=b
        elif a == 4:
            path_E=b
        elif a == 5:
            path_F=b
        elif a == 6:
            path_G=b
        elif a == 7:
            path_H=b
    if total_raster == 1:
        gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            outfile=salida,
                            NoDataValue=-3.40282e+38,
                            quiet=True)
                            
    if total_raster == 2:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        outfile=salida,
                        NoDataValue=-3.40282e+38,
                        quiet=True)

    if total_raster == 3:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            outfile=salida,
                            NoDataValue=-3.40282e+38,
                            quiet=True)
                            
    if total_raster == 4:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        outfile=salida,
                        NoDataValue=-3.40282e+38,
                        quiet=True)

    if total_raster == 5:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            D=path_D,
                            E=path_E, 
                            outfile=salida,
                            NoDataValue=-3.40282e+38,
                            quiet=True)
                            
    if total_raster == 6:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        outfile=salida,
                        NoDataValue=-3.40282e+38,
                        quiet=True)

    if total_raster == 7:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            D=path_D,
                            E=path_E, 
                            F=path_F,
                            G=path_G, 
                            outfile=salida,
                            NoDataValue=-3.40282e+38,
                            quiet=True)
                            
    if total_raster == 8:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        outfile=salida,
                        NoDataValue=-3.40282e+38,
                        quiet=True)