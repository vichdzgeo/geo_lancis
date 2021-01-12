import processing  as pr

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
        'GRASS_REGION_PARAMETER':region,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        pr.run("grass7:r.mapcalc.simple", dicc)
def raster_min_max(path_raster):
        '''

        Ejemplo de uso: 
        min, max = raster_min_max('/../raster.tif')
        '''
        rlayer = QgsRasterLayer(path_raster,"raster")

        extent = rlayer.extent()
        provider = rlayer.dataProvider()

        stats = provider.bandStatistics(1,
                                        QgsRasterBandStats.All,
                                        extent,
                                        0)

        min = stats.minimumValue
        max = stats.maximumValue
        return min,max
def remove_raster(path_r):
    '''
    Esta función elimina una capa del sistema

    :param path_r: ruta de la capa 
    :type path_r: str

    '''
    os.remove(path_r)

def extrae_crs(path_r):
    '''
    Extrae el código EPSG de la capa raster
    :param path_r: ruta de la capa
    :type parh_r: str
    '''
    r = QgsRasterLayer(path_r,"")
    return  r.crs().authid()
def rasterizar_vector (path_vector,n_campo,region,path_salida,tipo='int',ancho = 2992,alto = 2284):
    '''
    :param path_vector: ruta de la capa 
    :type path_vector: str

    :param n_campo: nombre del campo 
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
        v_tipo = 1 # valor para especificar entero a 16bits
    elif tipo == 'float':
        v_tipo =5 # valor para flotante 

    dicc={
        'INPUT':vector,
        'FIELD':n_campo,
        'BURN':0,
        'UNITS':0,
        'WIDTH':ancho,  ## DATOS PARA EL ESTADO DE YUCATAN 
        'HEIGHT':alto,
        'EXTENT':region,
        'NODATA':-9999.0,
        'OPTIONS':'',
        'DATA_TYPE':v_tipo,
        'INIT':None,
        'INVERT':False,
        'EXTRA':'',
        'OUTPUT':path_salida}
    pr.run("gdal:rasterize", dicc)
def alinear_raster(path_raster,region,resolucion,path_salida,crs_destino='',tipo='int'):
    '''
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
        v_tipo = 1 # valor para especificar entero a 16bits
    elif tipo == 'float':
        v_tipo =5 # valor para flotante 
    if crs_destino =='':
        crs_destino = extrae_crs(path_raster)

    dicc =  {'INPUT':path_raster,
        'SOURCE_CRS':extrae_crs(path_raster),
        'TARGET_CRS':crs_destino,
        'RESAMPLING':0,
        'NODATA':-9999,
        'TARGET_RESOLUTION':resolucion,
        'OPTIONS':'',
        'DATA_TYPE':v_tipo,
        'TARGET_EXTENT':region,
        'TARGET_EXTENT_CRS':None,
        'MULTITHREADING':False,
        'EXTRA':'--co="COMPRESS=LZW"',
        'OUTPUT':path_salida}
    pr.run("gdal:warpreproject",dicc)
def genera_buffer(capa,distancias,region,path_salida):
    '''
    Genera un buffer de un archivo raster, las distancias deben 
    ser kilometros

    :param capa: ruta de la capa de entrada
    :type capa: str

    :param distancias: distancias separadas por coma expresadas en kilometros 1,2,3...100 
    :type distancias: str

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str

    :param path_salida: ruta de la capa de salida
    :type path_salida: str

    '''
    dicc = {'input':capa,
                'distances':distancias,
                'units':1, 
                '-z':False,
                'output':path_salida,
                'GRASS_REGION_PARAMETER':region,
                'GRASS_REGION_CELLSIZE_PARAMETER':0,
                'GRASS_RASTER_FORMAT_OPT':'',
                'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.buffer",dicc )
def reclasifica_distancia(capa,intervalo,region,salida):
    '''
    Esta función reclasifica la capa de salida del buffer 

    :param capa: capa de entrada de distancias, salida de r.buffer
    :type capa: str

    :param intervalo: intervalo de distancias 
    :type intervalo:  int 

    :param region:coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str
    '''

    dicc = {'a':capa,
    'b':None,
    'c':None,
    'd':None,
    'e':None,
    'f':None,
    'expression':'A - %d'%intervalo,
    'output':salida,
    'GRASS_REGION_PARAMETER':region,
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple", dicc)
def reclasifica_capa(capa,region,reglas,salida):
    '''
    Esta función permite reclasificar una capa y agregar etiquetas a los valores

    :param capa: ruta de capa de entrada
    :type capa: str

    :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
    :type region: str

    :param reglas: ruta del archivo txt que contiene las reglas de clasificación 
    :type reglas: str

    :param salida: ruta de la capa de salida reclasificada
    :type salida: str
    '''

    dicc = {'input':capa,
                    'rules':reglas,
                    #'txtrules':'',
                    'output':salida,
                    'GRASS_REGION_PARAMETER':region,
                    'GRASS_REGION_CELLSIZE_PARAMETER':0,
                    'GRASS_RASTER_FORMAT_OPT':'',
                    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.reclass",dicc) 
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
def aplica_mascara(path_mascara, path_capa, path_salida, region):
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
    Esta función regresa en forma de cadena de texto 
    las coordenadas de la extensión de una capa raster xmin,xmax,ymin,ymax

    param path_layer: ruta de la capa raster
    type path_layer: str
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
    Esta función reclasifica una capa en enteros consecutivos en función de las categorias unicas de un 
    campo en especificico 

    :param path_v: ruta de capa vectorial
    :type path_v: str

    :param campo: nombre del campo que contiene las categorias
    :type campo: str

    :param nuevo_int_cats: nombre del campo el cúal contendrá las categorias en enteros
    :type nuevo_int_cats: str
    
    :param cont: contador para empezar la numeración en el número indicado, por defecto es 1
    :type cont: int
    '''
    vlayer = QgsVectorLayer(path_v,"","ogr")
    campos = [field.name() for field in vlayer.fields()]
    lista = list(set([i[campo] for i in vlayer.getFeatures()]))
    lista.sort()
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

def calcula_distancias_raster(path_r,path_mascara,path_salida,tipo_distancia = 0):
    region = get_region(path_mascara)
    path_r_distancia = path_r.split(".")[0]+"_tp_dis_mts.tif"
    dicc_distance =  {'input':path_r,
    'metric':tipo_distancia, # 0 = distancia euclidiana 3 = manhanthan
    '-m':False,
    '-':False,
    'distance':path_r_distancia,
    'value':'TEMPORARY_OUTPUT',
    'GRASS_REGION_PARAMETER':get_region(path_r),
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
            'GRASS_REGION_PARAMETER':region,
            'GRASS_REGION_CELLSIZE_PARAMETER':0,
            'GRASS_RASTER_FORMAT_OPT':'','GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple",dicc)
####- GENERAR UNA CADENA DE TEXTO PARA ESPECIFICAR LAS DISTANCIAS SOLICITADAS EN GENERA_BUFFER--####
#distancias = ",".join([str(x )for x in range(1,101)])

def distancia_caminos_lugar(path_lugar,campo_lugar,path_caminos,campo_caminos,path_mascara,path_salida,region,ancho=2292,alto=2284):
    region_pr = get_region(path_mascara)
    layer_raster_lugar = path_lugar.split(".")[0]+"tp_1.tif"
    rasterizar_vector(path_lugar,campo_lugar,region_pr,layer_raster_lugar,'int')
    layer_raster_caminos = path_caminos.split(".")[0]+"tp_1.tif"
    rasterizar_vector(path_caminos,campo_caminos,region,layer_raster_caminos,'int',ancho,alto)
    tp_distancia_camino = path_caminos.split(".")[0]+"tp_2.tif"
    calcula_distancias_raster(layer_raster_caminos,path_mascara,tp_distancia_camino,tipo_distancia = 3)
    path_presencia_invertida = path_lugar.split(".")[0]+"tp_2.tif"
    path_presencia_invertida_null1 = path_lugar.split(".")[0]+"tp_3.tif"
   

    dicc = {'a':layer_raster_lugar,
    'b':None,
    'c':None,
    'd':None,
    'e':None,
    'f':None,
    'expression':'A-1',
    'output':path_presencia_invertida,
    'GRASS_REGION_PARAMETER':region_pr,
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple", dicc)
    nulls(path_presencia_invertida,region,path_presencia_invertida_null1,valor_huecos=1)
    dicc2 = {'a':path_presencia_invertida_null1,
    'b':tp_distancia_camino,
    'c':None,
    'd':None,
    'e':None,
    'f':None,
    'expression':'A*B',
    'output':path_salida,
    'GRASS_REGION_PARAMETER':region_pr,
    'GRASS_REGION_CELLSIZE_PARAMETER':0,
    'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''}
    pr.run("grass7:r.mapcalc.simple", dicc2)
    remove_raster(layer_raster_lugar)
    remove_raster(layer_raster_caminos)
    remove_raster(tp_distancia_camino)
    remove_raster(path_presencia_invertida)
    remove_raster(path_presencia_invertida_null1)

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
        'GRASS_REGION_PARAMETER':region,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        pr.run("grass7:r.mapcalc.simple", dicc)


def redondea_raster(path_raster,no_decimales,salida):
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
                'NO_DATA':None,
                'RTYPE':5,
                'OPTIONS':'',
                'EXTRA':'--co=\"COMPRESS=LZW\"',
                'OUTPUT':salida}
    pr.run("gdal:rastercalculator",dicc)

