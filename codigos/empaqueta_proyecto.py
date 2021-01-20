import os 
import shutil


proyecto = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/insumos/agricultura.qgs'
carpeta = 'C:/analisis_insumos/empaqueta/'

proyecto_nuevo = carpeta + proyecto.split("/")[-1]
project = QgsProject.instance()
project.read(proyecto)
f = open(proyecto_nuevo, "w")
f.close()
capas = [layer.source() for layer in QgsProject.instance().mapLayers().values()]

lista = []
lista_layers_importar = []
for capa in capas:
    ruta = capa.split("|")[0]
    ruta_dir = "/".join(ruta.split("/")[:-1])+"/"
    nombre = ruta.split("/")[-1].split(".")[0]  
    lista_layers_importar.append(carpeta+'insumos/'+ruta.split("/")[-1])
    
    for root, dirs, files in os.walk(ruta_dir):
        for name in files:
            extension = os.path.splitext(name)
            if  extension[0] in nombre and ruta_dir == root:
                arch=root+name
                lista.append(arch)
              
for arch in lista:
    shutil.copyfile(arch,carpeta+"insumos/"+arch.split("/")[-1])

project = QgsProject.instance()
project.read(proyecto_nuevo)
[QgsProject.instance().removeMapLayers([layer.id()])for layer in QgsProject.instance().mapLayers().values()]
#for p_layer in lista_layers_importar:
#    layer = QgsVectorLayer(p_layer, "","ogr")
#    project.addMapLayer(layer)