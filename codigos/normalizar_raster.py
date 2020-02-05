# -*- coding: utf-8 -*-

'''
Autores: Fidel Serrano,Victor Hernandez


Qgis 3.4 o superior

'''

import copy
import pprint
import string
import qgis 
import qgis.core
from osgeo import gdal
import gdal_calc
import os
def ecuacion_vulnerabilidad(n):
    '''
    Esta función expresa la ecuación para el cálculo de la vulnerabilidad

    .. math::
        vulnerabilidad = \exp^{( 1 - sus)^{(1 + ca)}}


        | exp = Exposición

        | sus = Susceptibilidad

        | ca = Capacidad adaptativa

    :returns: str ecuacion
    '''
    if n==1:
        ecuacion = 'pow(A,(1-B))'
    if n==2:
        ecuacion = 'pow(pow(A,(1-B)),(1+C))'
    return ecuacion
def raster_min_max(rlayer):
    '''

    Ejemplo de uso: 
    min, max = raster_min_max('/../raster.tif')
    '''
    #rlayer = QgsRasterLayer(path_raster,"raster")

    extent = rlayer.extent()
    provider = rlayer.dataProvider()

    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    min = stats.minimumValue
    max = stats.maximumValue
    return min,max



def crea_capa(ecuacion,rasters_input,salida): 

    '''
    Esta función crea una capa mediante la calculadora raster
    de GDAL, esta función esta limitada hasta 8 variables en la ecuación.

    :param ecuacion: ecuación expresada en formato gdal,\
                    es este caso es la salida de la funcion *ecuacion_clp*
    :type ecuacion: String
    :param rasters_input: lista de los paths de los archivos rasters, salida de la función *separa_ruta_pesos*
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
                        
def normalizar(rlayer):
    print ("normalizando capa")
    min,max = raster_min_max(rlayer)
    path_origen =rlayer.dataProvider().dataSourceUri()
    raster_inputs=[path_origen]
    
    path_salida = path_origen.split(".")[0]+"_n.tif"
    ecuacion = '(A - '+str(min)+') / ('+str(max)+'-'+str(min)+')'
    print (ecuacion)
    crea_capa(ecuacion,raster_inputs,path_salida)
    print ("finalizo el proceso")
layer =qgis.utils.iface.activeLayer()

print(layer.dataProvider().dataSourceUri())

lista_vulnerabilidad =['G:/papiit/finales/tp_exposicion_total_n.tif',
                    'G:/papiit/finales/tp_susceptibilidad_total_n.tif',
                    'G:/papiit/finales/tp_resiliencia_total_n.tif']
ec_vul = ecuacion_vulnerabilidad(2)
salida ='G:/papiit/finales/tp_vulnerabilidad_exp_sus_res_n.tif'
crea_capa(ec_vul,lista_vulnerabilidad,salida)
#min,max = raster_min_max(layer)
#normalizar(layer)