# -*- coding: utf-8 -*-
import numpy, gdal_calc
import os, sys, subprocess, processing
from qgis.core import QgsApplication
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.analysis import *
import string 
import qgis.utils
import processing 
import numpy as np 


def wf(fp=2, min=0, max=1, categories=5,sentido='directo'):
    '''
    Esta funcion regresa de cortes según el método de weber-fechner

    :param fp: factor de progresión 
    :type fp: float

    :param min: valor mínimo de la capa
    :type min: float

    :param max: valor máximo de la capa
    :type max: float

    :param categories: número de categorias
    :type categories: int 

    '''
    dicc_e = {}
    if sentido =='directo':
        list_val = [min,]
        pm = max - min 
        cats = np.power(fp, categories)
        e0 = pm/cats
        for i in range(1 , categories + 1):
            dicc_e['e'+str(i)]= min + (np.power(fp,i) * e0)
            
        for i in range(1, categories + 1):
            list_val.append(dicc_e['e'+str(i)])
            
    elif sentido =='inverso':
        list_val = [max,]
        pm = max - min 
        cats = np.power(fp, categories)
        e0 = pm/cats
        for i in range(1 , categories + 1):
            dicc_e['e'+str(i)]= max - (np.power(fp,i) * e0)
            
        for i in range(1, categories + 1):
            list_val.append(dicc_e['e'+str(i)])
    return list_val

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

def normalizar():
    
    min,max = raster_min_max(rlayer)
    path_origen =layer.dataProvider().dataSourceUri()
    path_salida = path_origen.split(".")[0]+"_n.tif"
    ecuacion = '('+str(max)+' - A) / ('+str(max)+'-'+str(min)+')'
    
        
def rampa_raster(lista_val,raster,ind=1):
    
    
    if ind==1:
        colDic = {'MB':'#267300','B':'#4ce600','M':'#ffff00','A':'#ff5500','E':'#730000'}
    elif ind==-1:
        colDic = {'MB':'#730000','B':'#ff5500','M':'#ffff00','A':'#4ce600','E':'#267300'}
      
    lst = [ QgsColorRampShader.ColorRampItem(lista_val[1],QColor(colDic['MB']),'MB:'+str(round(lista_val[0],3))+'-'+str(round(lista_val[1],3))),\
        QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['B']),'B:'+str(round(lista_val[1],3))+'-'+str(round(lista_val[2],3))), \
        QgsColorRampShader.ColorRampItem(lista_val[3], QColor(colDic['M']),'M:'+str(round(lista_val[2],3))+'-'+str(round(lista_val[3],3))), \
        QgsColorRampShader.ColorRampItem(lista_val[4], QColor(colDic['A']),'A:'+str(round(lista_val[3],3))+'-'+str(round(lista_val[4],3))), \
        QgsColorRampShader.ColorRampItem(lista_val[5], QColor(colDic['E']),'E:'+str(round(lista_val[4],3))+'-'+str(round(lista_val[5],3)))]
     
    myRasterShader = QgsRasterShader()
    myColorRamp = QgsColorRampShader()
     
    myColorRamp.setColorRampItemList(lst)
    myRasterShader.setRasterShaderFunction(myColorRamp)
    myColorRamp.setColorRampType("DISCRETE") 
    myPseudoRenderer = QgsSingleBandPseudoColorRenderer(\
        raster.dataProvider(), raster.type(),  myRasterShader)
     
    raster.setRenderer(myPseudoRenderer)
     
    raster.triggerRepaint()


layer =qgis.utils.iface.activeLayer()    
## para vulnerabilidad o capas integradas
fp=2
categorias=5
minimo,maximo=raster_min_max(layer)
#lista_val = progresiva(fp)
lista_val = wf(fp,minimo,maximo,categorias)
#print (lista_val)
for i in range(len(lista_val)):
    if i < 5:
        print ("categoria %d"%(i+1),round(lista_val[i],3)," - ",round(lista_val[i+1],3))

rampa_raster(lista_val,layer,1)

## para funciones de valor

#rampa_raster_fv(layer)