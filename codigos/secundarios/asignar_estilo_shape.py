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


def asignar_estilo(campo, l, cortes=[0, 0.062, 0.125, 0.25, 0.5, 1.0]):
    myRangeList = []
    opacidad = 1
    categorias_txt = ['MB','B','M','A','E']
    #categorias_txt = [1,2,3,4,5]
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

layer = iface.activeLayer()

cortes_equi =equidistante()
asignar_estilo('consumo_no',layer,cortes)

#cortes_fp15 =weber_fechner(1.5)
#asignar_estilo('consumo_no',layer,cortes_fp15)

#cortes_fp20 =weber_fechner(2.0)
#asignar_estilo('consumo_no',layer,cortes_fp20)