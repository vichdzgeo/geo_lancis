import random, numpy 
import os, sys, subprocess, processing
from qgis.core import QgsApplication
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import *
from qgis.analysis import *
import qgis.utils
from qgis.PyQt import QtGui
import qgis 

def equidistante():
    lista_val =[0.0,0.20,0.4,0.6,0.8,1.0]
    return lista_val
def weber_fechner(fp=2,min=0,max=1):
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
def clasificar_campo(layer,cortes,campo,campo_cat="categoria"):
    categorias_txt = ['MB','B','M','A','E']
    campos = [field.name() for field in layer.fields()]
    if not campo_cat in campos:
        layer.dataProvider().addAttributes([QgsField(campo_cat,QVariant.String)])
        layer.updateFields()
    
    for i in range(len(cortes)-1):
        myMin = cortes[i]
        myMax = cortes[i+1]
            
        print (myMin,myMax)
        layer.startEditing()        
        for element in layer.getFeatures():
            if element[campo] >= myMin and element[campo] <= myMax:
                element[campo_cat]=categorias_txt[i]
                layer.updateFeature(element)
        layer.commitChanges()

def areas_categorias(layer,campo,tipo_area="ha"):
    categorias_txt = ['MB','B','M','A','E']
    areas = {}
    for categoria in categorias_txt:
        area=0
        for element in layer.getFeatures():
            if element[campo]==categoria:
                area +=element.geometry().area()
        if tipo_area=="ha":
            print (categoria,"area en ha :",round(area/10000,2))
            areas[categoria]=round(area/10000,2)
        elif tipo_area=="km2":
            print (categoria,"area en km2 :",round(area/1000000,2))
            areas[categoria]=round(area/1000000,2)
    return areas

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
        myColour = QtGui.QColor(colores_cat[i]) #color de la categoria
        mySymbol = QgsSymbol.defaultSymbol(l.geometryType()) #obtener el tipo de geometria
        mySymbol.setColor(myColour) #asignar color"
        mySymbol.setOpacity(opacidad) # opacidad del color 
        myRange = QgsRendererRange(myMin, myMax, mySymbol, myLabel) #
        myRangeList.append(myRange) # se guarda en una lista el rango
        
    myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
    myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    myRenderer.setClassAttribute(campo) # aqui va el campo 
    l.setRenderer(myRenderer)
    #QgsProject.instance().addMapLayer(layer)
    l.triggerRepaint()
def valores(areas):
    valores = []
    for k,v in areas.items():
        
        valores.append(str(v))
    print (",".join(valores))
    return ",".join(valores)

layer = iface.activeLayer()

campos = [field.name() for field in layer.fields()][2:13]
campos = ['FP10', 'FP11', 'FP12', 'FP13', 'FP14', 'FP15', 'FP16', 'FP17', 'FP18', 'FP19', 'FP20']
lista_fp = [1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]
n=0
archivo=open("C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/clasificacion_significancia/salida/areas_ha_neutral_v3.csv","w")
categorias_txt = ['MB','B','M','A','E']
archivo.write("campo,"+",".join(categorias_txt)+"\n")
for campo in campos:
    print ("procesando campo:  ",campo)
#print (campo,lista_fp[n])
    n_campo = "cat_"+ campo
    rango_wf = webber2(lista_fp[n])
    
    clasificar_campo(layer,rango_wf,campo,n_campo)
    areas = areas_categorias(layer,n_campo)
    value =valores(areas)
    archivo.write(campo+","+value+"\n")
    print (rango_wf,lista_fp[n])
    n+=1
    
archivo.close()

# para asignar el estilo de color 
#rango_wf = webber2(1)
#asignar_estilo('fp20',layer,rango_wf)
#
#


