import os ,time,csv
# Get the project instance

def lista_projects(path_carpeta):
    '''


    :param path_carpeta: ruta que contiene los archivos shape a procesar
    :type path_carpeta: String
    '''
    for root, dirs, files in os.walk(path_carpeta):
        lista = []
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.qgs':
                lista.append(root+name)
    return lista
def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa


def cargar_capa(nombre,path,estilo):
    tipo = path.split(".")[1]
    if tipo.lower() == 'shp' or tipo.lower()== 'kml' or tipo.lower() =='kmz':
        cargar_vector(nombre,path,estilo)
    elif tipo.lower() == 'tif' or tipo.lower()== 'bil' or tipo.lower() =='tiff':
        cargar_raster(nombre,path,estilo)
        
def cargar_vector(nombre,path_shape,estilo):
    
    #nombre = nombre_capa(path_shape).split(".")[0]
    layer = QgsVectorLayer(path_shape, nombre, "ogr")
    QgsProject.instance().addMapLayer(layer)
    layer.loadNamedStyle(estilo)

def cargar_raster(nombre,path_raster,estilo):
    
    #nombre = nombre_capa(path_raster).split(".")[0]
    rlayer = QgsRasterLayer(path_raster, nombre)
    QgsProject.instance().addMapLayer(rlayer)
    rlayer.loadNamedStyle(estilo)
    rlayer.triggerRepaint()

path_projects = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/mapas/sub_productivo/'
pathToQMLFile = "C:/estilos/productivo/" 
'''
lista_proyectos = lista_projects(path_projects)
for proyecto in lista_proyectos:
    project = QgsProject.instance()
    project.read(proyecto)

    for layer in iface.mapCanvas().layers():
            url = layer.dataProvider().dataSourceUri().split("|")[0]
            nombre = layer.name()
            estilo = pathToQMLFile + nombre + ".qml"
            #layersNames.append(str(i.name()))
            layer.saveNamedStyle( estilo )
            if  nombre not in dicc:
                dicc[nombre]={'url':url,'estilo':estilo}

archivo =open(pathToQMLFile+"capas_socioeconomico.csv","a")
for k,v in dicc.items():
    renglon = [k,dicc[k]['url'],dicc[k]['estilo']]
    archivo.write(",".join(renglon)+"\n")
archivo.close()
'''
### ------ CARGAR CAPAS   -----#####

capas = pathToQMLFile+"capas_productivo.csv"
with open(capas, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
#        print (row[2])
        nombre=row[0]
        url=row[1]
        estilo=row[2]
        cargar_capa(nombre,url,estilo)
