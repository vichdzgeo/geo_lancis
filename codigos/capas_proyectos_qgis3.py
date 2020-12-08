import os
from os import listdir,walk
from os.path import isfile, join,splitext
import processing as pr

def busca_prj(path_shape):
    '''
    Esta función busca dentro de la misma ruta del archivo shp, un archivo prj, este archivo
    contiene los datos de proyección cartográfica asociados.

    :param path_shape: ruta de la capa shapefile
    :type path_shape: str
    
    '''
    path_directorio = "/".join(path_shape.split("/")[:-1])+"/"
    directorio = (path_directorio.replace("\\","/")+"/").replace("//","/")
    fileNames=[]
    for root, dirs, files in walk(path_directorio):
        fileNames+=([f for f in listdir(root) if isfile(join(root, f))if f.split(".")[-1:][0]=='prj'])
    
    capa = (path_shape.split("/")[-1:][0].split(".")[0])+".prj"
    if capa  not in fileNames:
        valor = 0
    if capa in fileNames:
        valor =  10
        
    return valor
def extent_list(ext):
    xmin = ext.xMinimum()
    xmax = ext.xMaximum()
    ymin = ext.yMinimum()
    ymax = ext.yMaximum()

    region = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)
    return (region)

def lista_projects(path_carpeta):
    '''


    :param path_carpeta: ruta que contiene los archivos shape a procesar
    :type path_carpeta: String
    '''
    lista = []
    for root, dirs, files in os.walk(path_carpeta):
        
        for name in files:
            extension = os.path.splitext(name)
            if extension[-1] == '.qgs':
                lista.append(root+"/"+name)
    return lista
    
def total_geometrias(vlayer):
    if str(vlayer.type()) == 'QgsMapLayerType.RasterLayer':
        return "NA"
    total = int(vlayer.featureCount())
    return total
def tipo_geometria(vlayer):
    
    if str(vlayer.type()) == 'QgsMapLayerType.RasterLayer':
        return "raster"
    else:        
        if vlayer.geometryType()==0:
            tipo="punto"
        elif vlayer.geometryType()==1:
            tipo= "linea"
        elif vlayer.geometryType()==2:
            tipo = "poligono"
        return tipo

def nombre_proyeccion(vlayer):
    existe_prj = busca_prj(vlayer.source())
    proyeccion = ''
    if existe_prj ==10:
        
        proyeccion = vlayer.crs().authid()
        return proyeccion
    else:
        return "capa sin archivo prj"


path_projects = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/insumos/'

lista_proyectos = lista_projects(path_projects)
path_db_insumos = 'C:/analisis_insumos/insumos_fomix.csv'
db_insumos =open(path_db_insumos,"w")
proyectos = lista_proyectos
for proyecto in proyectos:
    categoria= proyecto.split("/")[-1].split(".")[0]
    #path_db_insumos = 'C:/analisis_insumos/'+proyecto.split("/")[-1].split(".")[0]+'.csv'
    #db_insumos =open(path_db_insumos,"w")
    project = QgsProject.instance()
    project.read(proyecto)
    names = [[categoria,
                        layer.name(),
                        layer.source(),
                        tipo_geometria(layer),
                        str(total_geometrias(layer)),
                        nombre_proyeccion(layer),
                        extent_list(layer.extent())] for layer in QgsProject.instance().mapLayers().values()]
                        
    for capa in names:
        renglon= ",".join(capa)
        db_insumos.write(renglon+"\n")
db_insumos.close()