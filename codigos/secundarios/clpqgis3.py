# -*- coding: utf-8 -*-
import processing as pr 
import os
import string 

def remove_raster(path_r):
    '''
    Esta función elimina una capa del sistema

    :param path_r: ruta de la capa 
    :type path_r: str

    '''
    os.remove(path_r)
def get_region(path_layer):
    '''
    Esta función regresa en forma de cadena de texto 
    las coordenadas de la extensión de una capa raster

    :param path_layer: ruta de la capa raster
    :type path_layer: str
    '''

    layer = QgsRasterLayer(path_layer,"")
    ext = layer.extent()
    xmin = ext.xMinimum()
    xmax = ext.xMaximum()
    ymin = ext.yMinimum()
    ymax = ext.yMaximum()

    region = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)
    return region
def set_nulls(map,output):
    '''
    Esta función permite cambiar el valor de nodata de una capa
    por -9999.0 

    :param map: ruta de la capa tif
    :type map: str

    :param output: ruta de la capa con valor de nodata de -9999.0
    :type output: str 

    '''
    region=get_region(map)
    tp_output_1 = output.split(".")[0]+"_tp1.tif"
    tp_output_2 = output.split(".")[0]+"_tp2.tif"
    dicc={'map':map,
            'null':-9999,
            'output':tp_output_1,
            'GRASS_REGION_PARAMETER':region,
            'GRASS_REGION_CELLSIZE_PARAMETER':0}
    
    pr.run("grass7:r.null",dicc)

    dicc2={'map':tp_output_1,
            'setnull':-9999,
            'output':tp_output_2,
            'GRASS_REGION_PARAMETER':region,
            'GRASS_REGION_CELLSIZE_PARAMETER':0}
    

    pr.run("grass7:r.null",dicc2)

    crea_capa('A',[tp_output_2],output)
    remove_raster(tp_output_1)
    remove_raster(tp_output_2)
    return output
def ecuacion_clp(pesos):
    '''
    Esta función regresa la ecuación de la combinación líneal ponderada para la calculadora raster

    :param pesos: lista de pesos de los criterios para la clp
    :type pesos: list
    '''
    n_variables=len(pesos)
    abc = list(string.ascii_uppercase)
    lista = []
   
    for a,b in zip(range(n_variables),pesos):
        lista.append(str(b)+str('*')+str(abc[a]))
    ecuacion= " + ".join(lista)
    return ecuacion 
def ecuacion_comp(pesos):
    '''
    Esta función regresa la ecuación del modo de decisión compensatorio para la calculadora raster

    :param pesos: lista de pesos de los criterios para la clp
    :type pesos: list
    '''
    n_variables=len(pesos)
    abc = list(string.ascii_uppercase)
    lista = []
    for a,b in zip(range(n_variables),pesos):
       lista.append(str(b)+str(' * ')+"(1 - " +str(abc[a])+")")
    ecuacion = " + ".join(lista)
    return ecuacion
def ecuacion_p_comp(pesos):
    '''
    Esta función regresa la ecuación del modo de decisión  parcialmente compensatorio para la calculadora raster

    :param pesos: lista de pesos de los criterios para la clp
    :type pesos: list
    '''
    n_variables=len(pesos)
    abc = list(string.ascii_uppercase)
    ecuacion = 'numpy.power('
    lista = []
    for a,b in zip(range(n_variables),pesos):
        lista.append('numpy.power('+str(b)+",2)"+str(' * ')+"(1 - " +"numpy.power("+str(abc[a])+",2)"+")")
    ecuacion += " + ".join(lista)
    ecuacion+= ',0.5)'
    return ecuacion 
def ecuacion_no_comp(pesos):
    '''
    Esta función regresa la ecuación del modo de decisión  no compensatorio para la calculadora raster

    :param pesos: lista de pesos de los criterios para la clp
    :type pesos: list
    '''
    n_variables=len(pesos)
    abc = list(string.ascii_uppercase)
    ecuacion = 'numpy.power('
    lista = []
    for a,b in zip(range(n_variables),pesos):
        lista.append('numpy.power('+str(b)+",10)"+str(' * ')+"(1 - " +"numpy.power("+str(abc[a])+",10)"+")")
    ecuacion += " + ".join(lista)
    ecuacion+= ',0.1)'
    return ecuacion 
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
def crea_capa(ecuacion,rasters_input,salida):
    '''
    Esta función calcula el algebra de mapas dada una ecuación.

    :param ecuacion: ecuación para el álgebra de mapas de capas tipo raster
    :type ecuacion: str

    :param rasters_input: lita de las rutas de la o las capas en el álgebra de mapas
    :type rasters_input: list

    :param salida: ruta del resultado de la ecuación en formato tiff
    :type salida: str
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

    
    if total_raster == 1:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
        pr.run("gdal:rastercalculator",dicc)
                            
    if total_raster == 2:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
        pr.run("gdal:rastercalculator",dicc)

    if total_raster == 3:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
        pr.run("gdal:rastercalculator",dicc)
                            
    if total_raster == 4:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
        pr.run("gdal:rastercalculator",dicc)

    if total_raster == 5:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
        pr.run("gdal:rastercalculator",dicc)
                            
    if total_raster == 6:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
    if total_raster == 7:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}

    if total_raster == 8:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
    if total_raster == 9:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'INPUT_I':path_I,
                'BAND_I':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
    if total_raster == 10:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'INPUT_I':path_I,
                'BAND_I':1,
                'INPUT_J':path_J,
                'BAND_J':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}

    if total_raster == 11:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'INPUT_I':path_I,
                'BAND_I':1,
                'INPUT_J':path_J,
                'BAND_J':1,
                'INPUT_K':path_K,
                'BAND_K':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}

    if total_raster == 12:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'INPUT_I':path_I,
                'BAND_I':1,
                'INPUT_J':path_J,
                'BAND_J':1,
                'INPUT_K':path_K,
                'BAND_K':1,
                'INPUT_L':path_L,
                'BAND_L':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}
    if total_raster == 13:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'INPUT_I':path_I,
                'BAND_I':1,
                'INPUT_J':path_J,
                'BAND_J':1,
                'INPUT_K':path_K,
                'BAND_K':1,
                'INPUT_L':path_L,
                'BAND_L':1,
                'INPUT_M':path_M,
                'BAND_M':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}

    if total_raster == 14:
        dicc ={        
                'INPUT_A':path_A,
                'BAND_A':1,
                'INPUT_B':path_B,
                'BAND_B':1,
                'INPUT_C':path_C,
                'BAND_C':1,
                'INPUT_D':path_D,
                'BAND_D':1,
                'INPUT_E':path_E,
                'BAND_E':1,
                'INPUT_F':path_F,
                'BAND_F':1,
                'INPUT_G':path_G,
                'BAND_G':1,
                'INPUT_H':path_H,
                'BAND_H':1,
                'INPUT_I':path_I,
                'BAND_I':1,
                'INPUT_J':path_J,
                'BAND_J':1,
                'INPUT_K':path_K,
                'BAND_K':1,
                'INPUT_L':path_L,
                'BAND_L':1,
                'INPUT_M':path_M,
                'BAND_M':1,
                'INPUT_N':path_N,
                'BAND_N':1,
                'FORMULA':ecuacion,
                'NO_DATA': -9999.0,
                'RTYPE':5,
                'EXTRA':'--co="COMPRESS=LZW"',
                'OUTPUT':salida}

        pr.run("gdal:rastercalculator",dicc)
def nombre_capa(path_capa):
    '''
    Esta función regresa el nombre de una capa sin extensión 

    :param path_capa: ruta de la capa
    :type path_capa: str 


    '''
    nombre_capa=(path_capa.split("/")[-1:])[0].split(".")[0]
    return nombre_capa
def cargar_raster(path_raster):
    '''
    Esta función carga una capa raster a un proyecto 
    de qgis 

    :param path_raster: ruta de la capa raster
    :type path_raster: str

    '''  
    nombre = nombre_capa(path_raster).replace("_"," ")
    rlayer = QgsRasterLayer(path_raster, nombre)
    QgsProject.instance().addMapLayer(rlayer)
def raster_nodata(path_raster):
    '''
    Esta función regresa el valor NoData de una capa raster

    :param path_raster: ruta de la capa raster:
    :type path_raster: str
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    

    provider = rlayer.dataProvider()
    rows = rlayer.rasterUnitsPerPixelY()
    cols = rlayer.rasterUnitsPerPixelX()
    block = provider.block(1, extent,  rows, cols)

    no_data = block.noDataValue()

    
    return no_data
def norm_estandar(path_raster, path_raster_n):
    '''
    Esta función normaliza línealmente una capa tipo raster

    :param path_raster: ruta de la capa a normalizar:
    :type path_raster: str

    :param path_raster_n: ruta de la capa normalizada
    :type path_raster_n: str
    '''
    min,max = raster_min_max(path_raster)
    ec_norm ='(A - ' + str(min) + ') / (' + str(max) + ' - ' +str(min) +')' 
    crea_capa(ec_norm,[path_raster],path_raster_n)
def multicriteria_gis(modo, dict_capas,nombre_final,directorio_salida):
    '''
    Esta función permite realizar la integración de criterios (capas) según el modo 
    de decisión específicado para el análisis espacial multicriterio

    :param modo: modo de decisión a elegir escriba **clp** para combinación líneal ponderada, **pc** para parcialmente compensatorio o **nc** para no compensatorio
    :type modo: str

    :param dict_capas: diccionario que contiene el nombre de la capa la ruta y su peso
    :type dict_capas: dict

    :param nombre_final: nombre del resultado de la integración ej: exposicion
    :type nombre_final: str

    :param directorio_salida: ruta del directorio de salida
    :type directorio_salida: str
    '''

    lista_inputs = [] 
    pesos = []

    dir_tmp = directorio_salida+"tmp"
    if "tmp" not in os.listdir(directorio_salida):
        os.mkdir(dir_tmp)

    for k,v in dict_capas.items():
        lista_inputs.append(dict_capas[k]['ruta'])
        pesos.append(dict_capas[k]['peso'])

    capas_listas =[]
    for capa in lista_inputs:
        if raster_nodata(capa)==-9999.0:
            capas_listas.append(capa)
        else:
            print ("cambiando valores de null de la capa:",nombre_capa(capa))
            tp_capa_set_null = dir_tmp+"/"+nombre_capa(capa)+".tif"
            capa_ac = set_nulls(capa,tp_capa_set_null)
            capas_listas.append(capa_ac)

    if modo.lower()=='clp' or modo.lower().replace("_"," ")=='combinacion lineal ponderada':
        path_salida= directorio_salida+ nombre_final+".tif"
        ecuacion = ecuacion_clp(pesos)
        crea_capa(ecuacion,lista_inputs,path_salida)
        cargar_raster(path_salida)
        return  path_salida

    if modo.lower()=='pc' or modo.lower().replace("_"," ")=='parcialmente compensatorio':
        path_salida= directorio_salida+ nombre_final+".tif"
        ecuacion = ecuacion_p_comp(pesos)
        crea_capa(ecuacion,capas_listas,path_salida)

    if modo.lower()=='nc' or modo.lower().replace("_"," ")=='no compensatorio':
        path_salida= directorio_salida+ nombre_final+".tif"
        ecuacion = ecuacion_no_comp(pesos)
        crea_capa(ecuacion,capas_listas,path_salida)

