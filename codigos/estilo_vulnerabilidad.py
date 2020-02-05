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



def wf(fp=2,min=0,max=1):
    
    if fp==1:
        lista_val = [0,0.2,0.4,0.6,0.8,1.0]
    else:
        dicc_e = {}
        lista_val = [0,]
        categorias = 5
        pm = max - min 
        cats = numpy.power(fp, categorias)
        e0 = pm/cats
        for i in range(1 , categorias + 1):
            dicc_e['e'+str(i)]= round((max - (numpy.power(fp,i) * e0)),3)
            

        dicc_cortes ={}
        for i in range(1 , categorias + 1):
            dicc_cortes['corte'+str(i)]= round(1 - dicc_e['e'+str(i)],3)
            lista_val.append(round(1 - dicc_e['e'+str(i)],3))

    return lista_val
def webber2(fp=2,minimo=0,maximo=1):


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
    print (myColorRamp.Type())

def rampa_raster_fv(layer):
    lista_val=[0,0.2,0.4,0.6,0.8,1.0]
    colDic_inv={'E':'#691e91', 'A':'#c9008c','M':'#f35864','B':'#faaf3c','MB':'#ffee7e'}
    colDic={'E':'#ffee7e', 'A':'#faaf3c','M':'#f35864','B':'#c9008c','MB':'#691e91'}
       
    lst = [ QgsColorRampShader.ColorRampItem(lista_val[1],QColor(colDic['MB']),'MB:'+str(round(lista_val[0],3))+'-'+str(round(lista_val[1],3))),\
        QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['B']),'B:'+str(round(lista_val[1],3))+'-'+str(round(lista_val[2],3))), \
        QgsColorRampShader.ColorRampItem(lista_val[3], QColor(colDic['M']),'M:'+str(round(lista_val[2],3))+'-'+str(round(lista_val[3],3))), \
        QgsColorRampShader.ColorRampItem(lista_val[4], QColor(colDic['A']),'A:'+str(round(lista_val[3],3))+'-'+str(round(lista_val[4],3))), \
        QgsColorRampShader.ColorRampItem(lista_val[5], QColor(colDic['E']),'E:'+str(round(lista_val[4],3))+'-'+str(round(lista_val[5],3)))]
    
    '''
    lst = [ QgsColorRampShader.ColorRampItem(lista_val[0], QColor(colDic['E'])), \
        QgsColorRampShader.ColorRampItem(lista_val[1], QColor(colDic['A'])), \
        QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['M'])), \
        QgsColorRampShader.ColorRampItem(lista_val[3], QColor(colDic['B'])), \
        QgsColorRampShader.ColorRampItem(lista_val[4], QColor(colDic['MB']))]
    '''
    
    myRasterShader = QgsRasterShader()
    myColorRamp = QgsColorRampShader()
    
    myColorRamp.setColorRampItemList(lst)
    #myColorRamp.setColorRampType(QgsColorRampShader.INTERPOLATED)
    myRasterShader.setRasterShaderFunction(myColorRamp)
    myColorRamp.setColorRampType("DISCRETE")
    myPseudoRenderer = QgsSingleBandPseudoColorRenderer(\
        layer.dataProvider(), layer.type(),  myRasterShader)
     
    layer.setRenderer(myPseudoRenderer)
     
    layer.triggerRepaint()


layer =qgis.utils.iface.activeLayer()    
## para vulnerabilidad o capas integradas
fp=1.8
categorias=5
minimo,maximo=raster_min_max(layer)
lista_val = wf(fp)
#lista_val = webber2(fp)
print (minimo,maximo)
rampa_raster(lista_val,layer)

## para funciones de valor

#rampa_raster_fv(layer)