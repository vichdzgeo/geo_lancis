from qgis.core import QgsVectorLayer, QgsProject
import os
def lista_shape(path):
    lista_shp=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                ruta = (root.replace("\\","/")+"/").replace("//","/")+name
                lista_shp.append(ruta)
    return lista_shp
    
def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa
def ordena_lista_shp(lista_shp):
    lista_preordenada =[]
    for capa in lista_shp:    
        lista_preordenada.append(capa.split("/")[-1].split(".")[0])
    lista_ordenada=sorted(lista_preordenada,reverse = True)
    paths_ordenados=[]
    for ordenada in lista_ordenada:
        for capa in lista_shp:
            if ordenada == capa.split("/")[-1].split(".")[0]:
                paths_ordenados.append(capa)
    return paths_ordenados

def cargar_capa(path_shape):
    nombre = nombre_capa(path_shape).split(".")[0]
    layer = QgsVectorLayer(path_shape, nombre, "ogr")
    QgsProject.instance().addMapLayer(layer)
    
path = 'G:/fomix/datos/recortes_utm16/'
lista_shp=lista_shape(path)
paths_ordenados=ordena_lista_shp(lista_shp)
for capa in paths_ordenados:
    cargar_capa(capa)