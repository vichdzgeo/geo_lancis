# -*- coding: utf-8 -*-
'''
Qgis 3 o superior
'''


import os
import processing as pr
import numpy as np 
from osgeo import gdal
from osgeo import osr


def raster_min_max(path_raster):
    '''
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    provider = rlayer.dataProvider()
    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    min = stats.minimumValue
    max = stats.maximumValue
    return min,max

def raster_nodata(path_raster):
    '''

    '''
    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    provider = rlayer.dataProvider()
    rows = rlayer.rasterUnitsPerPixelY()
    cols = rlayer.rasterUnitsPerPixelX()
    block = provider.block(1, extent,  rows, cols)
    no_data = block.noDataValue()

    return no_data

def wf(fp=2,min=0,max=1,categorias=5):
    
    dicc_e = {}
    lista_val = [min,]
    categorias = 5
    pm = max - min 
    cats = np.power(fp, categorias)
    e0 = pm/cats
    for i in range(1 , categorias + 1):
        dicc_e['e'+str(i)]= min + (np.power(fp,i) * e0)
        
    print (dicc_e)
    dicc_cortes ={}
    for i in range(1 , categorias + 1):
        lista_val.append( dicc_e['e'+str(i)])
    print (lista_val)
    return lista_val


def progresiva(fp=2,minimo=0,maximo=1):


    ConjDifusos = ['MB', 'B', 'M', 'A', 'E']

    # # Cortes de categorias siguiendo Ley de Weber

    # print '\n\t\t////Cortes de categorias siguiendo Ley de Weber-Feshner////\n'

    numcats = len(ConjDifusos)
    numeroDeCortes = numcats - 1
    laSuma = 0

    for i in range(numcats) :
        laSuma += ((fp) ** i)

    cachito = 1 / laSuma

    FuzzyCut = []

    for i in range(numeroDeCortes) :
        anterior = 0
        if i > 0:
            anterior = FuzzyCut[i - 1]

        corte = anterior + fp ** i * cachito
        FuzzyCut.append(corte)

    FuzzyCut.insert(0,0)
    FuzzyCut.append(1)
    
    return FuzzyCut

def tipo_clasificador(clasificador,path_r,fp=2,categorias = 5,min=0,max=1):

    if clasificador.lower() == "progresiva":
        nombre =clasificador.lower()+"_"+str(fp).replace('.','_')
        return progresiva(fp,min,max),nombre
        
    elif clasificador.lower() == "wf" or clasificador.lower() == "weber-fechner":
        nombre =clasificador.lower()+"_"+str(fp).replace('.','_')
        return wf(fp,categorias,min,max),nombre
    elif clasificador.lower()=='cuartiles':
        nombre = clasificador
        return cuantiles(path_r,4,min,max),nombre
    elif clasificador.lower()=='quintiles':
        nombre = clasificador
        return cuantiles(path_r,5,min,max),nombre
    elif clasificador.lower()== 'deciles':
        nombre = clasificador
        return cuantiles(path_r,10,min,max),nombre
    elif clasificador.lower()== 'equidistante':
        nombre = clasificador
        return equidistantes(categorias,min,max),nombre
    else:
        print ("error en el nombre de clasificacion")
        
def cuantiles(path_r,quantil,min,max):
    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimesion = band1.shape
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band2= band1[band1 != nodata_r]
    band2 = band2.flatten()
    print (nodata_r)
    lista_val = [min,]
    
    for i in range(1,quantil+1):
        #print (i,i/quantil)
        valor= i/quantil
        cuantil_c = np.quantile(band2,valor)
        lista_val.append(cuantil_c)
    print (lista_val)
    return lista_val
    
def equidistantes (categorias=5,min=0,max=1):
    lista_val = [min,]
    incremento = (max - min) / categorias
    for i in range(1,categorias+1):
        valor = min + (incremento * i)
        lista_val.append(valor)
    print (lista_val)
    return lista_val

def clasifica_raster(path_capa,clasificador,fp=2,categorias=5,min=0,max=1):

    cortes,nombre = tipo_clasificador(clasificador,path_capa,fp,categorias,min,max)
    no_d = raster_nodata(path_capa)
    ecuacion = ecuacion_class(cortes)
    path_salida = path_capa.split(".")[0]+"_"+nombre+".tif"
    dicc ={        
        'INPUT_A':path_capa,
        'BAND_A':1,
        'FORMULA':ecuacion,
        'NO_DATA': -9999,
        'RTYPE':1,
        'OUTPUT':path_salida}
    pr.run("gdal:rastercalculator",dicc)
    print ("capa clasificada... ruta ->",path_salida)
    cargar_raster(path_salida)

    
def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa

def ecuacion_class(cortes):
    n_cortes = len(cortes)
    ecuacion =''
    for i in range(n_cortes):
        if i < n_cortes-2: 
            ecuacion+='logical_and(A>='+str(cortes[i])+',A<'+str(cortes[i+1])+')*'+str(i+1)+' + '
        elif i== n_cortes-2 :
            ecuacion+='logical_and(A>='+str(cortes[i])+', A<='+str(cortes[i+1])+')*'+str(i+1)
    print (ecuacion)
    return ecuacion

def cargar_raster(path_raster):
    
    nombre = nombre_capa(path_raster).split(".")[0]
    rlayer = QgsRasterLayer(path_raster, nombre)
    QgsProject.instance().addMapLayer(rlayer)
    if 'cuartiles' in nombre:
        estilo = "C:/Users/Victor/Downloads/sigclassifier/rampa_cuartiles.qml"
    elif 'quintiles' in nombre:
        estilo = "C:/Users/Victor/Downloads/sigclassifier/rampa_quinitles.qml"
    elif 'deciles' in nombre:
        estilo = "C:/Users/Victor/Downloads/sigclassifier/rampa_deciles.qml"
    else:
        estilo = "C:/Users/Victor/Downloads/sigclassifier/rampa_5cats.qml"
    rlayer.loadNamedStyle(estilo)
    rlayer.triggerRepaint()


#path_capa ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/indice_fragilidad_del_territorio/procesamiento/serie3_indice_fragilidad.tif"
#path_capa ="C:/Dropbox (LANCIS)/SOFTWARE/plenumsoft/datos_prueba/sigindex/bcs_240420/clp_qgis_bcs_norm.tif"
#clasifica_raster(path_capa,"wf",1.3) # indice de calidad 
#clasifica_raster(path_capa,"wf",1.7) # indice de riesgo
#path_capa = 'C:/Dropbox (LANCIS)/SOFTWARE/plenumsoft/datos_prueba/sigclassifier/yucatan/tp_vulnerabilidad_exp_sus_res_n.tif'

path_capa = 'C:/Dropbox (LANCIS)/SOFTWARE/plenumsoft/datos_prueba/sigindex/yuc_230420/clp_qgis_norm.tif'
min,max=raster_min_max(path_capa)
clasifica_raster(path_capa,"equidistante",categorias=10,min=min,max=max) # indice de fragilidad
#clasifica_raster(path_capa,"wf",1.2) # indice de vulnerabilidad costera

#clasifica_raster(path_capa,"deciles")




