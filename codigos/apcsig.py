# -*- coding: utf-8 -*-

'''
Autor: Víctor Hernández D.

Correo: victor.hernandez@iecologia.unam.mx

user_github: @vichdzgeo

Colaboladores: LANCIS - UNAM
'''

import copy
import pprint
import string
import qgis 
import qgis.core
import numpy 
from osgeo import gdal
import gdal_calc
import os
import processing as pr 


######## FUNCIONES GENERALES ###########
def nombre_capa(path_capa):
    nombre = path_capa.split("/")[-1].split(".")[0]
    return nombre

######## FUNCIONES A DATOS VECTORIALES ###########
def categorias_campo_csv(path_shape,campo):
    '''
    Esta función extrae las categorias únicas de un campo dado de una capa vectorial, el 
    archivo csv se guarda en la misma ruta de la capa vectorial y es nombrado como : **categorias_campo_nombre_capa.csv**

    .. note:: 

        En dado caso que el nombre de la categoria contenga el símbolo de ',' está función la remplaza por ';' para evitar errores en la escritura del archivo csv
    
    :param path_shape: ruta de la capa vectorial 
    :type path_shape: str

    :param campo: nombre del campo que contiene las categorias
    :type campo: str


    '''

    layer = QgsVectorLayer(path_shape,"","ogr")
    nombre_capa = layer.source().split("/")[-1].split(".")[0]
    path_categorias = "/".join(layer.source().split("/")[:-1])+"/categorias_"+campo+"_"+nombre_capa+".csv"
    archivo = open(path_categorias,'w')
    consulta = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
    lista = list(set([x[campo] for x in layer.getFeatures(consulta)]))
    lista.sort()
    print (lista)
    archivo.write("id,categoria\n")
    for i in range(len(lista)):
        archivo.write(str(i+1)+","+lista[i].replace(",",';')+"\n")
    archivo.close()
    print ('archivo csv de categorias creado...')
    print ('ruta: ',path_categorias)
def campos_minusculas(path_shape):
    '''
    Esta función renombra los campos en minúsculas

    :param path_shape: Ruta de la capa vectorial
    :type path_shape: str

    '''
    layer = QgsVectorLayer(path_shape,"","ogr")
    campos = [field.name() for field in layer.fields()]
    for campo in campos:
        for field in layer.pendingFields():
            if campo == field.name():
                with edit(layer):
                    idx = layer.fieldNameIndex(field.name())
                    layer.renameAttribute(idx,field.name().lower())
    print ("Proceso terminado")
def campos_mayusculas(path_shape):
    '''
    Esta función renombra los campos en mayusculas

    :param path_shape: Ruta de la capa vectorial
    :type path_shape: str

    '''
    layer = QgsVectorLayer(path_shape,"","ogr")
    campos = [field.name() for field in layer.fields()]
    for campo in campos:
        for field in layer.pendingFields():
            if campo == field.name():
                with edit(layer):
                    idx = layer.fieldNameIndex(field.name())
                    layer.renameAttribute(idx,field.name().upper())
    print ("Proceso terminado")
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
def llenar_campos_nulos(path_vector,valor=-9999):

    '''
    :param path_vector: Ruta de la capa vectorial
    :type path_vector: str

    :param valor: valor numérico para rellenar los campos vacios por default se establece -9999
    '''

    layer=QgsVectorLayer(path_vector,"","ogr")
    lista = [field.name()  for field in layer.fields() if  field.typeName() != 'String' and field.typeName() != 'Date']
    layer.startEditing()
    for poligono in layer.getFeatures():
        for campo in lista:
            if not poligono[campo]:
               poligono[campo] = valor
        layer.updateFeature(poligono)
    layer.commitChanges()
def capa_binaria(path_v,campo_cat='presencia'):
    '''
    Esta función crea un campo llamado presencia y asigna 
    a cada elemento el valor de 1 
    
    :param path_v: ruta de la capa vectorial
    :type path_v: str


    :param campo_cat: nombre del campo a crear, por default es presencia
    :type campo_cat: str
    '''
    vlayer = QgsVectorLayer(path_v,"","ogr")
    campos = [field.name() for field in vlayer.fields()]
    if campo_cat in campos:
        print ('el campo ya existe, se actualiza el contenido')
        vlayer.startEditing()

        for l in vlayer.getFeatures():
            l[campo_cat]=1
            vlayer.updateFeature(l)
        vlayer.commitChanges()
    else:
        vlayer.dataProvider().addAttributes([QgsField(campo_cat.lower(),QVariant.Int)])
        vlayer.updateFields()
        vlayer.startEditing()
        vlayer.commitChanges()
        vlayer.startEditing()

        for l in vlayer.getFeatures():
            l[campo_cat]=1
            vlayer.updateFeature(l)
        vlayer.commitChanges()
    print ('capa clasificada...')
def agregar_categorias(path_v,campo,nuevo_int_cats='categorias',cont=1):
    '''
    Esta función reclasifica una capa en enteros consecutivos en función de las categorias únicas de un 
    campo en especificico, como subproducto genera un archivo csv con las categorias.

    :param path_v: ruta de capa vectorial
    :type path_v: str

    :param campo: nombre del campo que contiene las categorias
    :type campo: str

    :param nuevo_int_cats: nombre del campo a crear, el cúal contendrá las categorias en enteros
    :type nuevo_int_cats: str
    
    :param cont: contador para empezar la numeración en el número indicado, por defecto es 1
    :type cont: int
    '''
    vlayer = QgsVectorLayer(path_v,"","ogr")
    campos = [field.name() for field in vlayer.fields()]
    lista = list(set([i[campo] for i in vlayer.getFeatures()]))
    lista.sort() # Ordena las categorias alfabeticamente 
    n_cats =len(lista)
    if nuevo_int_cats in campos:
        print ('el campo ya existe, se actualiza el contenido')
        vlayer.startEditing()
        for cat in lista:
            for l in vlayer.getFeatures():
                if cat == l[campo]:
                    l[nuevo_int_cats]=cont
                    vlayer.updateFeature(l)
            cont +=1
        vlayer.commitChanges()
    else:
        vlayer.dataProvider().addAttributes([QgsField(nuevo_int_cats.lower(),QVariant.Int)])
        vlayer.updateFields()
        vlayer.startEditing()
        vlayer.commitChanges()
        vlayer.startEditing()
        for cat in lista:
            for l in vlayer.getFeatures():
                if cat == l[campo]:
                    l[nuevo_int_cats]=cont
                    vlayer.updateFeature(l)
            cont +=1
        vlayer.commitChanges()
    print ('capa clasificada...')
    print ('generando archivo txt de categorias...')
    path_tp_reglas = "/".join(path_v.split("/")[:-1])+"/reglas_"+path_v.split("/")[-1].split(".")[0]+".txt"
    reglas = open(path_tp_reglas,"w")
    for i in range(1,cont):
        reglas.write(str(i)+" = "+str(i)+" "+lista[i-1]+'\n')
    reglas.close()
    return path_tp_reglas,n_cats

def genera_reglas_txt(p_layer,campo_cat,campo_id):
    layer = QgsVectorLayer(p_layer,"","ogr")
    consulta = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
    lista_cat =  list(set([(x[campo_id],x[campo_cat]) for x in layer.getFeatures(consulta)]))

    lista_cat.sort()
    n_cats = len(lista_cat)
    print ('generando archivo txt de categorias...')
    path_tp_reglas = "/".join(layer.source().split("/")[:-1])+"/reglas_"+layer.source().split("/")[-1].split(".")[0]+".txt"
    reglas = open(path_tp_reglas,"w")
    for cat in lista_cat:
        reglas.write(str(cat[0])+" = "+str(cat[0])+" "+cat[1]+'\n')
    print ('archivo txt de categorias generado')
    reglas.close()
    return path_tp_reglas,n_cats
def agrega_regla_txt(path_reglas,lista_cats):
    reglas = open(path_reglas,"a")
    for cat in lista_cats:
        reglas.write(str(cat[0])+" = "+str(cat[0])+" "+cat[1]+'\n')
    print ('catehorias agregadas')
    reglas.close()
def categorias_generales(p_capa,campo_cat,campo_id):
    
    layer = QgsVectorLayer(p_capa,"","ogr")
    consulta = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
    lista_cat =  list(set([(x[campo_id],x[campo_cat]) for x in layer.getFeatures(consulta)]))
    lista_cat.sort()
    dicc ={}
    for cat in lista_cat:
        print (cat[0],cat[1])
        dicc[cat[0]]=cat[1]
    return dicc
def selecciona_categorias(dicc,lista_ids,path_v,campo_cat,nuevo_int_cats='cats_s',cont=1):
    dicc2 = dicc.copy()
    for id in lista_ids:
        dicc2.pop(id)
    vlayer = QgsVectorLayer(path_v,"","ogr")
    campos = [field.name() for field in vlayer.fields()]
    consulta = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
    #lista = list(set([i[campo_cat] for i in vlayer.getFeatures(consulta)]))
    lista = []
    for k,v in dicc2.items():
        lista.append(v)
    
    lista.sort() # Ordena las categorias alfabeticamente 
    print(lista)
    n_cats =len(lista)

    if nuevo_int_cats in campos:
        print ('el campo ya existe, se actualiza el contenido')

        vlayer.startEditing()
        for cat in lista:
            for l in vlayer.getFeatures():
                l[nuevo_int_cats]=None
                vlayer.updateFeature(l)
        vlayer.commitChanges()

        vlayer.startEditing()
        for cat in lista:
            for l in vlayer.getFeatures():
                if cat == l[campo_cat]:
                    l[nuevo_int_cats]=cont
                    vlayer.updateFeature(l)
            cont +=1
        vlayer.commitChanges()
    else:
        vlayer.dataProvider().addAttributes([QgsField(nuevo_int_cats.lower(),QVariant.Int)])
        vlayer.updateFields()
        vlayer.startEditing()
        vlayer.commitChanges()
        vlayer.startEditing()
        for cat in lista:
            for l in vlayer.getFeatures():
                if cat == l[campo_cat]:
                    l[nuevo_int_cats]=cont
                    vlayer.updateFeature(l)
            cont +=1
        vlayer.commitChanges()
    print ('capa clasificada...')
    print ('generando archivo txt de categorias...')
    path_tp_reglas = "/".join(path_v.split("/")[:-1])+"/reglas_cat_selec_"+path_v.split("/")[-1].split(".")[0]+".txt"
    reglas = open(path_tp_reglas,"w")
    reglas.write(str(0)+" = "+str(0)+" "+"Ausencia"+'\n')
    for i in range(1,cont):
        reglas.write(str(i)+" = "+str(i)+" "+lista[i-1]+'\n')
    reglas.close()
    return path_tp_reglas,n_cats



######## FUNCIONES A DATOS RASTER ###########
def rasterizar_vector (path_vector,n_campo,region,path_salida,tipo='int',ancho = 0,alto = 0):
    '''
    Esta función rasteriza una capa vectorial a partir de un campo de tipo numérico y dada una región 
    y el numero de columnas (ancho) y el numero de renglones (alto)

    :param path_vector: ruta de la capa vectorial
    :type path_vector: str

    :param n_campo: nombre del campo que contiene los id de las categorias 
    :type  n_campo: srt

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str

    :param path_salida: ruta de la capa de salida con extension tif
    :type path_salida: str

    :param tipo: tipo de dato, use 'int' para entero o 'float' para flotante, por default es entero
    :type tipo: str

    
    '''
    vector = QgsVectorLayer(path_vector,"","ogr")
    if tipo == 'int':
        v_tipo = 4 # valor para especificar entero a 32 bits
    elif tipo == 'float':
        v_tipo =5 # valor para flotante 

    dicc={
        'INPUT':vector,
        'FIELD':n_campo,
        'BURN':0,
        'UNITS':0,
        'WIDTH':ancho, 
        'HEIGHT':alto,
        'EXTENT':region,
        'NODATA':-9999.0,
        'OPTIONS':'COMPRESS=LZW',
        'DATA_TYPE':v_tipo,
        'INIT':None,
        'INVERT':False,
        'OUTPUT':path_salida}
    pr.run("gdal:rasterize", dicc)
def alinear_raster(path_raster,region,resolucion,path_salida,crs_destino='',tipo='int'):
    '''
    Esta función alinea un raster dada una región y el tamaño de pixel 
    :param path_raster: ruta de la capa a alinear
    :type path_raster: str

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str 

    :param resolucion: tamaño de pixel
    :type resolucion: int 

    :param path_salida: ruta de la capa de salida con extension tif
    :type path_salida: str

    :param crs_destino: nombre del código EPSG,
    :type crs_destino:  str 

    :param tipo: tipo de dato, use 'int' para entero o 'float' para flotante, por default es entero
    :type tipo: str
    '''
    if tipo == 'int':
        v_tipo = 5 # valor para especificar entero a 32bits
    else:
        v_tipo =6 # valor para flotante 
    if crs_destino =='':
        crs_destino = QgsRasterLayer(path_raster,"").crs()

    dicc =  {'INPUT':path_raster,
        'SOURCE_CRS':QgsRasterLayer(path_raster,"").crs(),
        'TARGET_CRS':crs_destino,
        'RESAMPLING':0,
        'NODATA':-9999,
        'TARGET_RESOLUTION':resolucion,
        'OPTIONS':'COMPRESS=LZW',
        'DATA_TYPE':v_tipo,
        'TARGET_EXTENT':region,
        'TARGET_EXTENT_CRS':None,
        'MULTITHREADING':False,
        'OUTPUT':path_salida}
    pr.run("gdal:warpreproject",dicc)
def aplica_mascara(path_mascara, path_capa, path_salida, region):
    '''
    Esta función aplica la máscara de la zona de estudio a una capa raster, 
    es importante que la capa a la cual se aplicará la máscara este previamente alineada

    :param path_mascara: ruta de la mascara en formato tiff
    :type path_mascara: str


    :param path_capa: ruta de la capa a la cual se requiere aplicar la máscara
    :type path_capa: str

    :param path_salida: ruta de la capa resultado de aplicar la máscara
    :type path_salida: str

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str
    '''

    dicc = {'a':path_mascara,
    'b':path_capa,
    'c':None,
    'd':None,
    'e':None,
    'f':None,
    'expression':'A*B',
    'output':path_salida,
    'GRASS_REGION_PARAMETER':region,
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple", dicc)
def get_region(path_layer):
    '''
    Esta función extrae la región o extensión de una capa raster así como el número de columnas y renglones

    :param path_layer: ruta de la capa raster
    :type path_layer: str

    :returns: en forma de lista [1,2,3] [1] las coordenadas de la extensión de una capa raster xmin,xmax,ymin,ymax ; [2]. ancho de una capa raster (número de columnas) y [3]. alto de una capa raster (número de renglones)

    '''

    layer = QgsRasterLayer(path_layer,"")
    ext = layer.extent()
    xmin = ext.xMinimum()
    xmax = ext.xMaximum()
    ymin = ext.yMinimum()
    ymax = ext.yMaximum()

    region = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)
    ancho = layer.width()
    alto = layer.height()
    return [region,ancho,alto]
def ecuacion_clp(pesos):

    '''
    Esta función recibe una lista de pesos para regresar la ecuación
    en la estructura requerida por gdal para la combinación lineal ponderada. 
    
    **ejemplo:**

    .. math::

        ecuacion = A*0.40 + B*0.25 + C*0.15 +D*0.20

    :param pesos: lista de los pesos de las capas, salida de la función 
    :type pesos: lista

    :returns: ecuación en formato gdal para ser ingresada a la funcion crea_capa_raster
    :type returns: str

    '''
    n_variables=len(pesos)
    abc = list(string.ascii_uppercase)
    ecuacion = ''
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= (str(b)+str(' * ')+str(abc[a])+' + ' )
        else:
            ecuacion+= (str(b)+str(' * ')+str(abc[a]))
    return ecuacion
def normailiza(path_raster, path_raster_n,modo='ideales'):
    '''
    Esta función normaliza una capa raster, se puede elegir entre dos tipos de normalización.

    1) ideales: La capa ráster se divide entre el valor máximo como resultado se tiene una capa con un máximo de 1 pero el valor mínimo no necesariamente será 0

    .. math:: 

        ideales=\\frac{A}{A.max}
    
    2) lineal: la capa ráster resultante tendra como valor máximo 1 y como valor mínimo 0
    el 1 representará el maximo de la capa de entrada y el 0 representa el valor mínimo de la 
    capa de entrada

    .. math::

        lineal=\\frac{A -A.min}{A.max - A.min}
    '''

    min,max = raster_min_max(path_raster)
    
    no_data =raster_nodata(path_raster)
    if modo == 'ideales':
        ec_norm ='(A' + ') / (' + str(max) +')'  # llevar a ideal 
    elif modo == 'lineal':
        ec_norm ='(A - '+str(min) + ') / (' + str(max)+'-'+str(min) +')'  # normalizar 
    dicc ={        
        'INPUT_A':path_raster,
        'BAND_A':1,
        'FORMULA':ec_norm,
        'NO_DATA': no_data,
        'RTYPE':5,
        'EXTRA':'--co="COMPRESS=LZW"',
        'OUTPUT':path_raster_n}
    pr.run("gdal:rastercalculator",dicc)
def raster_min_max(path_raster):
    '''
    Esta funcion regresa los valores maximos y minimos de una capa raster

    :param path_raster: ruta de la capa raster
    :type path_raster: str 
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    provider = rlayer.dataProvider()
    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    v_min = stats.minimumValue
    v_max = stats.maximumValue
    return v_min, v_max
def redondea_raster(path_raster,salida,no_decimales=3):
    '''
    Esta función redondea una capa raster de tipo flotante en el número de decimales indicado

    :param path_raster: ruta de la capa raster
    :type path_raster: str

    :param no_decimales: número de decimales a los que se va a redondear la capa, por default es 3
    :type no_decimaes: int

    :param salida: ruta de la capa de salida
    :type salida: str

    '''
    dicc =  {'INPUT_A':path_raster,
                'BAND_A':1,
                'INPUT_B':None,
                'BAND_B':-1,
                'INPUT_C':None,
                'BAND_C':-1,
                'INPUT_D':None,
                'BAND_D':-1,
                'INPUT_E':None,
                'BAND_E':-1,
                'INPUT_F':None,
                'BAND_F':-1,
                'FORMULA':'A.round('+str(no_decimales)+')',
                'NO_DATA':-9999.0,
                'RTYPE':5,
                'OPTIONS':'',
                'EXTRA':'--co=\"COMPRESS=LZW\"',
                'OUTPUT':salida}
    pr.run("gdal:rastercalculator",dicc)
def crea_capa_raster(ecuacion,rasters_input,salida): 

    '''
    Esta función crea una capa mediante la calculadora raster
    de GDAL, esta función esta limitada hasta 14 variables en la ecuación.

    :param ecuacion: ecuación expresada en formato gdal,
    :type ecuacion: str
    :param rasters_input: lista de los paths de los archivos rasters
    :type rasters_input: list
    :param salida: ruta con extensión tiff de la salida
    :type salida: str

    :returns: Capa raster de tipo flotante, los valores de la capa son redondeados a 3 decimales
    
    '''
    path_A=''
    path_B=''
    path_C=''
    path_D=''
    path_E=''
    path_F=''
    path_G=''
    path_H=''  
    path_I=''
    path_J=''
    path_K=''
    path_L=''
    path_M=''
    path_N=''


    total_raster = len(rasters_input)
    
    for a,b in zip(range(total_raster), rasters_input):
        if a == 0:
            path_A=b
        elif a == 1:
            path_B=b
        elif a == 2:
            path_C=b
        elif a == 3:
            path_D=b
        elif a == 4:
            path_E=b
        elif a == 5:
            path_F=b
        elif a == 6:
            path_G=b
        elif a == 7:
            path_H=b
        elif a == 8:
            path_I=b
        elif a == 9:
            path_J=b
        elif a == 10:
            path_K=b
        elif a == 11:
            path_L=b
        elif a == 12:
            path_M=b
        elif a == 13:
            path_N=b

    tp_salida = salida.split(".")[0]+'_raw.tif'

   
     
    if total_raster == 1:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)
                        
    if total_raster == 2:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 3:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)
                        
    if total_raster == 4:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 5:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)
                        
    if total_raster == 6:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 7:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)
                            
    if total_raster == 8:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)
        
    if total_raster == 9:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        I=path_I,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 10:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        I=path_I,
                        J=path_J,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 11:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        I=path_I,
                        J=path_J,
                        K=path_K,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 12:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        I=path_I,
                        J=path_J,
                        K=path_K,
                        L=path_L,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 13:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        I=path_I,
                        J=path_J,
                        K=path_K,
                        L=path_L,
                        M=path_M,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    if total_raster == 14:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        I=path_I,
                        J=path_J,
                        K=path_K,
                        L=path_L,
                        M=path_M,
                        N=path_N,
                        outfile=tp_salida,
                        NoDataValue=-9999.0,
                        creation_options=["COMPRESS=LZW","PREDICTOR=3","TILED=YES"],
                        quiet=True)

    redondea_raster(tp_salida,3,salida)
    remove_raster(tp_salida)
def remove_raster(path_r):
    '''
    Esta función elimina una capa del sistema

    :param path_r: ruta de la capa 
    :type path_r: str

    '''
    lista = []
    for root, dirs, files in os.walk("/".join(path_r.split("/")[:-1])):
        nombre = nombre_capa(path_r)
        for name in files:
            extension = os.path.splitext(name)
            if  nombre in extension[0] and nombre[0:3]==extension[0][0:3] :
                arch="/".join([root,name])
                lista.append(arch)
    for arch in lista:
        os.remove(arch)
def nulls(map,region,output,valor_huecos=0):
    '''
    Esta función asigna un valor  a los no_data de la capa
    
    :param map: ruta de la capa raster
    :type map: str

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str

    :param output:ruta de la capa resultante
    :type output: str

    :param valor_huecos: número que tendrán los pixeles nulos
    :type valor_huecos: int 
    '''
    region=get_region(map)
    dicc={'map':map,
            'null':valor_huecos,
            'output':output,
            'GRASS_REGION_PARAMETER':region,
            'GRASS_REGION_CELLSIZE_PARAMETER':0}
    pr.run("grass7:r.null",dicc)
def raster_1capa(path_a,ecuacion,salida,tipo = 'int'):
    if tipo == 'int':
        r_type = 4
    elif tipo == 'float':
        r_type = 5
    dicc ={        
        'INPUT_A':path_a,
        'BAND_A':1,
        'FORMULA':ecuacion,
        'NO_DATA': -9999,
        'RTYPE':r_type,
        'EXTRA':'--co="COMPRESS=LZW"',
        'OUTPUT':salida}
    pr.run("gdal:rastercalculator",dicc)
def raster_2capas(path_a,path_b,ecuacion,salida,tipo = 'int'):
    if tipo == 'int':
        r_type = 4
    elif tipo == 'float':
        r_type = 5
    dicc ={        
        'INPUT_A':path_a,
        'BAND_A':1,
        'INPUT_A':path_b,
        'BAND_A':1,
        'FORMULA':ecuacion,
        'NO_DATA': -9999,
        'RTYPE':r_type,
        'EXTRA':'--co="COMPRESS=LZW"',
        'OUTPUT':salida}
    pr.run("gdal:rastercalculator",dicc)
def reclasifica_capa(capa,region,reglas,salida):
    '''
    Esta función permite reclasificar una capa raster y genera un archivo 
    xml el cúal contiene el nombre de las categorias.

    :param capa: ruta de capa de entrada
    :type capa: str

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str

    :param reglas: ruta del archivo txt que contiene las reglas de clasificación 
    :type reglas: str

    :param salida: ruta de la capa de salida reclasificada
    :type salida: str

    :retuns: Capa raster clasificada y archivo xml 
    '''

    dicc = {'input':capa,
                    'rules':reglas,
                    'output':salida,
                    'GRASS_REGION_PARAMETER':region,
                    'GRASS_REGION_CELLSIZE_PARAMETER':0,
                    'GRASS_RASTER_FORMAT_OPT':'',
                    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.reclass",dicc)
def calcula_distancias_raster(path_r,path_mascara,path_salida,tipo_distancia = 0):
    region = get_region(path_mascara)
    path_r_distancia = path_r.split(".")[0]+"_tp_dis_mts.tif"
    dicc_distance =  {'input':path_r,
    'metric':tipo_distancia, # 0 = distancia euclidiana 3 = manhanthan
    '-m':False,
    '-':False,
    'distance':path_r_distancia,
    'value':'TEMPORARY_OUTPUT',
    'GRASS_REGION_PARAMETER':get_region(path_r)[0],
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    
    pr.run("grass7:r.grow.distance",dicc_distance)
    region = get_region(path_mascara)
    dicc =  {'a':path_r_distancia,
            'b':path_mascara,
            'c':None,
            'd':None,
            'e':None,
            'f':None,
            'expression':'(round(A/100.0,1)/10.0)*B', #Expresión que convierte las distancias a kms con un decimal y aplica la mascara de la zona de estudio
            'output':path_salida,
            'GRASS_REGION_PARAMETER':region[0],
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'','GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple",dicc)

    remove_raster(path_r_distancia)
def distancia_caminos_lugar(layer_raster_lugar,path_caminos,campo_caminos,path_mascara,path_salida,region_ext,ancho_ext=2292,alto_ext=2284):
    '''
    Esta función genera una capa de distancia a caminos y agrega distancia cero a aquellos pixeles que se sobreponen con el área del lugar
    
    '''
    
    layer_raster_caminos = "/".join(path_salida.split("/")[:-1])+"/tp1_"+nombre_capa(path_caminos)+".tif"
    tp_distancia_camino = "/".join(path_salida.split("/")[:-1])+"/tp2_"+nombre_capa(path_caminos)+".tif"
    path_presencia_invertida = "/".join(path_salida.split("/")[:-1])+"/tp1_"+nombre_capa(layer_raster_lugar)+".tif" 
    path_presencia_invertida_null1 = "/".join(path_salida.split("/")[:-1])+"/tp2_"+nombre_capa(layer_raster_lugar)+".tif" 

    region_pr = get_region(path_mascara)
    rasterizar_vector(path_caminos,campo_caminos,region_ext,layer_raster_caminos,'int',ancho_ext,alto_ext) # 1 signigica carretera, 0 ausencia 
    calcula_distancias_raster(layer_raster_caminos,path_mascara,tp_distancia_camino,tipo_distancia = 3)
    
   

    dicc = {'a':layer_raster_lugar,
    'b':None,
    'c':None,
    'd':None,
    'e':None,
    'f':None,
    'expression':'A-1',
    'output':path_presencia_invertida,
    'GRASS_REGION_PARAMETER':region_pr[0],
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple", dicc)
    nulls(path_presencia_invertida,region_ext,path_presencia_invertida_null1,valor_huecos=1)
    dicc2 = {'a':path_presencia_invertida_null1,
    'b':tp_distancia_camino,
    'c':None,
    'd':None,
    'e':None,
    'f':None,
    'expression':'A*B',
    'output':path_salida,
    'GRASS_REGION_PARAMETER':region_pr[0],
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple", dicc2)
    remove_raster(layer_raster_caminos)
    remove_raster(tp_distancia_camino)
    remove_raster(path_presencia_invertida)
    remove_raster(path_presencia_invertida_null1)
def calculadora_grass(path_capa, ecuacion,path_salida):
        '''
        Esta función aplica la máscara de la zona de estudio

        :param path_mascara: ruta de la mascara en formato tiff
        :type path_mascara: str


        :param path_capa: ruta de la capa a la cual se requiere aplicar la máscara
        :type path_capa: str

        :param path_salida: ruta de la capa resultado de aplicar la máscara
        :type path_salida: str

        :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
        :type region: str
        '''
        region = get_region(path_capa)

        dicc = {'a':path_capa,
        'b':None,
        'c':None,
        'd':None,
        'e':None,
        'f':None,
        'expression':ecuacion,
        'output':path_salida,
        'GRASS_REGION_PARAMETER':region[0],
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        pr.run("grass7:r.mapcalc.simple", dicc)
def integra_localidades_caminos(path_lugar_n,w_lugar,path_d_camino_n,w_d_camino,d_max_lugar,salida):

        '''
        Esta función aplica la máscara de la zona de estudio

        :param path_mascara: ruta de la mascara en formato tiff
        :type path_mascara: str


        :param path_capa: ruta de la capa a la cual se requiere aplicar la máscara
        :type path_capa: str

        :param path_salida: ruta de la capa resultado de aplicar la máscara
        :type path_salida: str

        :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
        :type region: str
        '''
        region = get_region(path_lugar_n)
        ecuacion  = '(A*'+str(w_lugar)+' + B *'+str(w_d_camino)+') * ('+str(d_max_lugar)+')'
        dicc = {'a':path_lugar_n,
        'b':path_d_camino_n,
        'c':None,
        'd':None,
        'e':None,
        'f':None,
        'expression':ecuacion,
        'output':salida,
        'GRASS_REGION_PARAMETER':region[0],
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        pr.run("grass7:r.mapcalc.simple", dicc)
        print("proceso integra_localidades_caminos terminado")
