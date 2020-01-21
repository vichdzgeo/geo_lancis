from qgis.core import QgsVectorLayer, QgsProject
import os
from os import listdir,walk
from os.path import isfile, join,splitext

def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa

def lista_shape(path):
    lista_shp=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                ruta = (root.replace("\\","/")+"/").replace("//","/")+name
                lista_shp.append(ruta)
    return lista_shp

def busca_prj(path_shape):
    path_directorio = "/".join(path_shape.split("/")[:-1])+"/"
    directorio = (path_directorio.replace("\\","/")+"/").replace("//","/")
    fileNames=[]
    for root, dirs, files in walk(path_directorio):
        fileNames+=([f for f in listdir(root) if isfile(join(root, f))if f.split(".")[-1:][0]=='prj'])
    
    capa = (path_shape.split("/")[-1:][0].split(".")[0])+".prj"
    if capa  not in fileNames:
        valor = 0
    if capa in fileNames:
        valor =  1
        
    return valor


def cargar_capa(path_shape):
    nombre = nombre_capa(path_shape).split(".")[0]
    layer = QgsVectorLayer(path_shape, nombre, "ogr")
    validacion = validar_capa(layer)
    if validacion==1:
        return layer
    elif validacion==0:
        return "error"

def validar_capa(vlayer):
    if vlayer.isValid():
        return 1
    else:
        return 0
        
def tipo_geometria(vlayer):
    if not vlayer == "error":
        if vlayer.geometryType()==0:
            tipo="punto"
        elif vlayer.geometryType()==1:
            tipo= "linea"
        elif vlayer.geometryType()==2:
            tipo = "poligono"
            return tipo
    return "error"

def total_campos(vlayer):
    
    if not vlayer == "error":
        campos = [field.name() for field in vlayer.fields()]
        total = len(campos)
        return total
    return "error"
def total_geometrias(vlayer):
    if not vlayer == "error":
        total = int(vlayer.featureCount())
        return total
    return "error"
def nombre_proyeccion(path_shape,vlayer):
    existe_prj = busca_prj(path_shape)
    proyeccion = ''
    if existe_prj ==1:
        if not vlayer == "error":
            proyeccion = vlayer.crs().authid()
            return proyeccion
    else:
        return "capa sin archivo prj"


def campos_nulos(vlayer):
    
    if not vlayer == "error":
        campos = [field.name() for field in vlayer.fields()]
        dicc={}
        for campo in campos:
            dicc[campo]=0
        for poligono in vlayer.getFeatures():
 
            for campo in campos:
                lista_vacio=0
                if not poligono[campo]:
                    if poligono[campo]==NULL:
                        lista_vacio+=1
                if lista_vacio > 0:
                    dicc[campo]+=1

        lista_campos_nulos=[]
 
        for key,value in dicc.items():
            if value>0:
                lista_campos_nulos.append(key)
                
        binario=10
        total = len(lista_campos_nulos)
        if total >0:
            binario=0
        return (str(total)+"campos nulos")
    
    return "error"



path = "C:/Dropbox (LANCIS)/ADMIN/admin_propuestas/semarnat/oe_pacifico_cs/sig/areas_prioritarias_proteccion/oempcs_zonaecolterrestre.shp"

layer2 = cargar_capa(path)
tipo=tipo_geometria(layer2)
campos = total_campos(layer2)
proyeccion = nombre_proyeccion(path,layer2)
t_features=total_geometrias(layer2)
nulos = campos_nulos(layer2)
print (tipo,campos,proyeccion,t_features,nulos)


