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

def asignar_estilo(campo, l, cortes=[0, 0.062, 0.125, 0.25, 0.5, 1.0]):
    myRangeList = []
    opacidad = 1
    categorias_txt = ['MB','B','M','A','E']
    #colores_cat = ['#730000','#ff5500','#ffff00','#4ce600','#267300']
    colores_cat = ['#267300','#4ce600','#ffff00','#ff5500','#730000']
    
    renderer = l.renderer()
    
    for i in range(0,5):
        myMin = cortes[i]
        myMax = cortes[i+1]
        myLabel = categorias_txt[i]  #etiqueta primera categoria
        myColour = PyQt5.QtGui.QColor(colores_cat[i]) #color de la categoria
        mySymbol = QgsSymbol.defaultSymbol(l.geometryType()) #obtener el tipo de geometria
        mySymbol.setColor(myColour) #asignar color"
        mySymbol.setOpacity(opacidad) # opacidad del color 
        myRange = QgsRendererRange(myMin, myMax, mySymbol, myLabel) #
        myRangeList.append(myRange) # se guarda en una lista el rango
        
    myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
    myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    myRenderer.setClassAttribute(campo) # aqui va el campo 
    l.setRenderer(myRenderer)
    l.triggerRepaint()

def indice_lee_salee(vlayer_base,vlayer_model,campo_categoria,categoria,id='ageb_id'):   
    
    union = []
    interseccion = []
    for a,b in zip(vlayer_base.getFeatures(),vlayer_model.getFeatures()):
        if a[campo_categoria]==categoria:
            union.append(a[id])
        if b[campo_categoria]==categoria:
            union.append(a[id])
        if a[campo_categoria]==categoria and b[campo_categoria]==categoria:
            interseccion.append(b[id])

    union_conjunto = set(union)
    #print (len(agebs_base),len(agebs_alto),len(interseccion),len(union_conjunto))
    indice_lee_count = round((len(interseccion) / len(union_conjunto)),4)

    area_interseccion =0
    area_union =0

    for i in vlayer_base.getFeatures():
        for ageb_union in union_conjunto:
            if i[id]==ageb_union:
                area_union += i.geometry().area()
        for ageb_interseccion in interseccion:
            if i[id]==ageb_interseccion:
                area_interseccion += i.geometry().area()
    indice_lee = round(area_interseccion / area_union,4)
    return indice_lee