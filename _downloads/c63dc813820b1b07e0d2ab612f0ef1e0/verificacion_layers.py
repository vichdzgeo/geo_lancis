# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayer, QgsProject
import os, errno
from os import listdir,walk
from os.path import isfile, join,splitext
import processing as pr
from time import sleep 

def mapa_base(): #carga en el mapa base de open street maps 
    
    urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
    rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
    if rlayer.isValid():
        QgsProject.instance().addMapLayer(rlayer)
        return rlayer
    else:
        print('invalid layer')
def cargar_capa_canvas(path):
    name = nombre_capa(path)
    layer = QgsVectorLayer(path,name,"ogr")
    if layer.isValid():
        QgsProject.instance().addMapLayer(layer)

        return layer
    else:
        print ("capa no valida")
def nombre_capa(path_shape):  #infomación general
    nombre_capa=(path_shape.split("/")[-1:])[0].split(".")[0]
    return nombre_capa
def remover_capa(layer):
    QgsProject.instance().removeMapLayer(layer)
def genera_preview(path): #Genera un archivo png de la capa
    base_map = mapa_base()
    lay = cargar_capa_canvas(path)
    codigo =int(lay.crs().authid()[5:])
    crs = QgsCoordinateReferenceSystem(codigo)
    path_salida = lay.dataProvider().dataSourceUri().split(".")[0]
    
    layers = QgsProject.instance().mapLayersByName(lay.name())
    layer = layers[0]
    
    project = QgsProject.instance()
    project.setCrs(crs)
    manager = project.layoutManager()
    layoutName = 'Layout1'
    layouts_list = manager.printLayouts()
    # remove any duplicate layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    manager.addLayout(layout)

    # create map item in the layout 
    map = QgsLayoutItemMap(layout)
    map.setRect(20,20,20,20)

    # set the map extent 

    ms = QgsMapSettings()
    #
    ms.setLayers([layer]) # set layers to be mapped 
    rect = layer.extent()
    rect.scale(1.0)
    ms.setExtent(rect)
    map.setExtent(rect)
    layout.addLayoutItem(map)
    #
    map.attemptMove(QgsLayoutPoint(5,20,QgsUnitTypes.LayoutMillimeters))
    map.attemptResize(QgsLayoutSize(85,100,QgsUnitTypes.LayoutMillimeters))

    # leyenda de la capa
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle("Legend")
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    #layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(80,15,QgsUnitTypes.LayoutMillimeters))

    # escala gráfica
    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(5)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitsPerSegment(0.5)
    scalebar.setLinkedMap(map)
    scalebar.setUnitLabel('km')
    scalebar.setFont(QFont('Arial',14))
    scalebar.update()
    #layout.addLayoutItem(scalebar)
    scalebar.attemptMove(QgsLayoutPoint(20,19,QgsUnitTypes.LayoutMillimeters))

    title = QgsLayoutItemLabel(layout)
    title.setText(lay.name())
    title.setFont(QFont('Arial',10))
    title.adjustSizeToText()
    #layout.addLayoutItem(title)
    title.attemptMove(QgsLayoutPoint(0, 0, QgsUnitTypes.LayoutMillimeters))


    layout.pageCollection().resizeToContents(QgsMargins(0,0,0,0),QgsUnitTypes.LayoutMillimeters)


    layout = manager.layoutByName(layoutName)
    exporter = QgsLayoutExporter(layout)
    
    fn = lay.dataProvider().dataSourceUri().split(".")[0]+'.png'
    exporter.exportToImage(fn,QgsLayoutExporter.ImageExportSettings())
    #exporter.exportToPdf(fn,QgsLayoutExporter.PdfExportSettings())

    remover_capa(lay)
    remover_capa(base_map)

##########################################################################


def nombre_capa(path_shape):  #infomación general
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
        valor =  10
        
    return valor    
def busca_xml(path_shape):
    path_directorio = "/".join(path_shape.split("/")[:-1])+"/"
    directorio = (path_directorio.replace("\\","/")+"/").replace("//","/")
    fileNames=[]
    for root, dirs, files in walk(path_directorio):
        fileNames+=([f for f in listdir(root) if isfile(join(root, f))if f.split(".")[-1:][0]=='xml'])
    
    capa = (path_shape.split("/")[-1:][0].split(".")[0])+".xml"
    if capa  not in fileNames:
        valor = 0
    if capa in fileNames:
        valor =  10
        
    return valor   
def topologia(vlayer,path_topologia):
    
    if not vlayer == "error":
               
        dir_topo = path_topologia+"/topologia"
        if "topologia" not in os.listdir(path_topologia):
            os.mkdir(dir_topo)
        nombre_capa = path_shape.split("/")[-1:][0].split(".")[0]
        p_val = dir_topo+"/"+nombre_capa+"_valido.shp"
        p_error = dir_topo+"/"+nombre_capa+"_error.shp"
        p_invalido = dir_topo+"/"+nombre_capa+"_invalido.shp"
        
        dicc={'INPUT_LAYER':vlayer,
                    'METHOD':2,
                    'VALID_OUTPUT':p_val,
                    'INVALID_OUTPUT':p_invalido,
                    'ERROR_OUTPUT':p_error,
                    'IGNORE_RING_SELF_INTERSECTION':True}
        
        pr.run("qgis:checkvalidity",dicc)
        error_layer=QgsVectorLayer(p_error,"","ogr")
        valid_layer=QgsVectorLayer(p_val,"","ogr")
        
        total_original = int(vlayer.featureCount())
        total_errores = int(error_layer.featureCount())
        total_validos = int(valid_layer.featureCount())
        
        #vlayer,valid_layer,error_layer="","",""
        
        identificador = 0
        if total_original == total_validos:
            identificador=10
        else:
            identificador = 10 -(total_errores*2)
        #print identificador 
        if identificador <0:
            identificador=0
    #    for archivo in os.listdir(dir_topo):
    #        os.remove(dir_topo+"/"+ archivo)
        return identificador
    return "error"
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
    if existe_prj ==10:
        
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
        return binario
    
    return "error"
def sin_geometria(vlayer):
    lena=0
    identificador=10
    for element in vlayer.getFeatures():
        if element.geometry() ==None:
            lena+=1
    if lena >0:
        identificador=0
    return identificador
def codificacion_contenido(vlayer):
    total = int(vlayer.featureCount())
    campos = [field.name() for field in vlayer.fields() if field.typeName()=="String"]
    dicc_campos={}
    for campo in campos:
        dicc_campos[campo]={'valido':0,'invalido':0,'como_txt':0,'vacio':0}
    
    for pol in vlayer.getFeatures():
        for campo in campos:
            if not pol[campo]:
                 if pol[campo]==NULL:
                     cadena=''
                     dicc_campos[campo]['vacio']+=1
            else:
                cadena=pol[campo]
            
            permisible=(((cadena.replace(" ","")).replace(".","")).replace("-","")).replace("/","")
              
            num=666
            alfanum=999
            if cadena.replace(".","").isdigit():
                num =1
            elif permisible.isalnum():
                alfanum =2

            status =''
            if num==1:
                status="numero codificado como texto"
                dicc_campos[campo]['como_txt']+=1
            elif alfanum==2:
                status="codificado correctamente"
                dicc_campos[campo]['valido']+=1
            else:
                status="error en la codificacion"
                dicc_campos[campo]['invalido']+=1
    valor=0
    campos_mal = []
    campos_texto =[]
    
    for key,value in dicc_campos.items():
        valor+=((value['valido']*100)/total)
        if value['invalido'] >0 :
            permisible=(((key.replace(" ","")).replace("_","")).replace("-","")).replace("/","")
            if permisible.isalnum():
                campos_mal.append(key)
            else:
                campos_mal.append("error detectado")
        if value['como_txt']>0:
            permisible=(((key.replace(" ","")).replace("_","")).replace("-","")).replace("/","")
            if permisible.isalnum():
                campos_texto.append(key)
            else:
                campos_texto.append("error detectado")

        
        
        #print (key,"el ",((value['correcto']*100)/total),"por ciento de los datos esta codificado correctamente")
    valor_final = valor
    indicador=0
    if valor_final ==len(campos)*100:
        indicador=10
    total = len(campos_mal)+len(campos_texto)
    c_mal = campos_mal +campos_texto
    
    return indicador
def diagnostico_capas(path_shape):
    path_topologia=carpeta_tmp(path_shape)
    suma=0
    diagnostico = {"nombre":"",
                    "total_campos":'-',
                    "código proyeccion":'-',
                    "metadatos":'-',
                    "proyeccion":'-',
                    "geometria_completa":'-',
                    "sobrelapados":'-',
                    #"sin_atributo":'-',
                    #"huecos":'-',
                    "nulos":'-',
                    #"significado":'-',
                    #"unidades":'-',
                    "codificados":'-',}
                    #"resolucion":'-',
                    #"fecha":'-',
                    #"linaje":'-',
                    #"fuente":'-',
                    
                    #"ruta":'-'}
    vlayer = cargar_capa(path_shape)
   
    if not vlayer == "error":
        diagnostico["nombre"]=nombre_capa(path_shape)  #informativa
        diagnostico["total_campos"]=total_campos(vlayer) #informativa
        diagnostico["código proyeccion"]=nombre_proyeccion(path_shape,vlayer) #informativa
        diagnostico["metadatos"]=busca_xml(path_shape) #variable
        diagnostico["proyeccion"]=busca_prj(path_shape) #variable 
        diagnostico["geometria_completa"]=sin_geometria(vlayer) #variable
        diagnostico["sobrelapados"]=topologia(vlayer,path_topologia) #variable 
        #diagnostico["sin_atributo"]="NA"#sin_geometria(vlayer) #falta cargarla
        #diagnostico["huecos"]="NA"
        diagnostico["nulos"]=campos_nulos(vlayer) #variable
        diagnostico["codificados"]=codificacion_contenido(vlayer) #Variable
        #diagnostico["significado"]="NA"
        #diagnostico["unidades"]="NA" 
        #diagnostico["resolucion"]="NA"
        #diagnostico["fecha"]="NA"
        #diagnostico["linaje"]="NA"
        #diagnostico["fuente"]="NA"
        
        #diagnostico["ruta"]=path_shape
        
        for key,value in diagnostico.items():
            if not key=='total_campos':
                if isinstance(value, int) and not isinstance(value, tuple):
                    
                    suma+=value
                if isinstance(value, tuple):
                    suma+=value[0]
        
        diagnostico['suma']=suma
        
        return diagnostico
    return diagnostico

def carpeta_tmp(path_shape):
    carpeta= "tmp"
    path_dir = "/".join(path_shape.split("/")[:-1])+"/"+carpeta

    try:
        os.mkdir(path_dir)
    except OSError as e:
        if e.errno !=errno.EEXIST:
            raise
    
    return path_dir+"/"

#path_shape = "C:/Users/Victor/Downloads/jalisco/procesamiento/resultados16IVCAT_single.shp"
path_dir = "C:/Dropbox (LANCIS)/SIG/insumos/agricultura/conabio/vector/produccion_miel/"
lista_shp=lista_shape(path_dir)
bitacora = open(path_dir+"verificacion.csv","w")
criterios_diagnosticos = ["nombre",
                            "no_campos",
                            "epsg",
                            "metadatos",
                            "proyeccion",
                            "geometria_completa",
                            "sobrelapados",
                            "codificados",
                            "nulos",
                            "calificacion"]
encabezado =''
for criterio in criterios_diagnosticos:
    encabezado+=(criterio+",")
encabezado +="\n"
bitacora.write(encabezado)

for path_shape in lista_shp:
    linea = ''
    diagnostico=diagnostico_capas(path_shape)
    linea =str(diagnostico["nombre"])+","+\
        str(diagnostico["total_campos"])+","+\
        str(diagnostico["código proyeccion"])+","+\
        str(diagnostico["metadatos"])+","+\
        str(diagnostico["proyeccion"])+","+\
        str(diagnostico["geometria_completa"])+","+\
        str(diagnostico["sobrelapados"])+","+\
        str(diagnostico["codificados"])+","+\
        str(diagnostico["nulos"])+","+\
        str(diagnostico["suma"])+"\n"


    bitacora.write(linea)

    if diagnostico['proyeccion']==10:
         genera_preview(path_shape)

bitacora.close()
