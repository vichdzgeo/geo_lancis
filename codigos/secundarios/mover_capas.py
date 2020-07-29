

def cargar_capa(path_shape):
    
    nombre = nombre_capa(path_shape).split(".")[0]
    
    layer = QgsVectorLayer(path_shape, nombre, "ogr")
    QgsProject.instance().addMapLayer(layer)
    
def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa
    
def vcopia(path_vector, path_salida):
    """
    Crea una copia de la capa a partir de la ruta de la capa,
    la capa es creada con el mismo sistema de referencia que el origen.

    :param path_vector: ruta de la capa original
    :type path_vector: String

    :param path_salida: ruta de donde sera almacenada la capa
    :type path_salida: String
    """
    vlayer = QgsVectorLayer(path_vector, "", "ogr")
    clonarv = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                      path_salida,
                                                      'utf-8',
                                                      vlayer.crs(),
                                                      "ESRI Shapefile")


def mover_capa(layer,path_destino):
    url = layer.dataProvider().dataSourceUri().split("|")[0]
    
    if "sig_becarios" in url:
        nombre = url.split("/")[-1]
        print ("copiando capa ",nombre)
        ruta_destino = path_destino+nombre
        print (ruta_destino)
        vcopia(url,ruta_destino)
        cargar_capa(ruta_destino)


layer = iface.activeLayer()
path_destino = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/sig_becarios/"
mover_capa(layer,path_destino)