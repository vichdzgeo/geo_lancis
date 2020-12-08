# -*- coding: utf-8 -*-

'''
Autores: Fidel Serrano,Victor Hernandez


Qgis 3.4 o superior

'''

import copy
import pprint
import string
import qgis 
import qgis.core
from osgeo import gdal
import gdal_calc
import os
def ecuacion_vulnerabilidad(n):
    '''
    Esta función expresa la ecuación para el cálculo de la vulnerabilidad

    .. math::
        vulnerabilidad = \exp^{( 1 - sus)^{(1 + ca)}}


        | exp = Exposición
        | sus = Susceptibilidad
        | ca = Capacidad adaptativa

    :returns: str ecuacion
    '''
    if n==1:
        ecuacion = 'pow(A,(1-B))'
    if n==2:
        ecuacion = 'pow(pow(A,(1-B)),(1+C))'
    return ecuacion
def media_raster(path_raster):
    '''
    Esta función regresa el promedio de todos los pixeles válidos
    de un archivo raster

    :param path_raster: Ruta del archivo raster
    :type path_raster: String
    '''
    rlayer = qgis.core.QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    provider = rlayer.dataProvider()
    stats = provider.bandStatistics(1,
                                    qgis.core.QgsRasterBandStats.All,
                                    extent,
                                    0)
    promedio = stats.mean
    return round(promedio,3)
    
def lista_criterios(dicc):
    '''
    Esta función regresa una lista de los criterios de un diccionario

    :param dicc: Diccionario que contiene nombres, rutas y pesos para el
    análisis de vulnerabilidad / sensibilidad
    :type dicc: diccionario python
    '''
    criterios = []
    for k1,v1 in dicc.items():
        for k2,v2, in v1['criterios'].items():
            for k3,v3, in v2['criterios'].items():
                criterios.append(k3)
    return criterios
def crea_capa(ecuacion,rasters_input,salida): 

    '''
    Esta función crea una capa mediante la calculadora raster
    de GDAL, esta función esta limitada hasta 14 variables en la ecuación.

    :param ecuacion: ecuación expresada en formato gdal,\
                    es este caso es la salida de la funcion *ecuacion_clp*
    :type ecuacion: String
    :param rasters_input: lista de los paths de los archivos rasters, salida de la función *separa_ruta_pesos*
    :type rasters_input: lista
    :param salida: ruta con extensión tiff de la salida
    :type salida: String
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


    # raster = gdal.Open(path_A)
    # band1 =raster.GetRasterBand(1).ReadAsArray()
    # dimesion = band1.shape
    # no_data=raster.GetRasterBand(1).GetNoDataValue()
            
    if total_raster == 1:
        gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            outfile=salida,
                            #NoDataValue= 3.40282e+38,
                            quiet=True)
                            
    if total_raster == 2:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
                        quiet=True)

    if total_raster == 3:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            outfile=salida,
                            #NoDataValue= 3.40282e+38,
                            quiet=True)
                            
    if total_raster == 4:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
                        quiet=True)

    if total_raster == 5:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            D=path_D,
                            E=path_E, 
                            outfile=salida,
                            #NoDataValue= 3.40282e+38,
                            quiet=True)
                            
    if total_raster == 6:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        outfile=salida,
                       #NoDataValue= 3.40282e+38,
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
                            outfile=salida,
                            #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
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
                        outfile=salida,
                        #NoDataValue= 3.40282e+38,
                        quiet=True)


def ecuacion_clp(pesos):

    '''
    Esta función recibe una lista de pesos para regresar la ecuación
    en la estructura requerida por gdal para la combinación lineal ponderada.

    :param pesos: lista de los pesos de las capas, salida de la función *separa_ruta_pesos*
    :type pesos: lista
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
def lista_pesos_ruta(dicc):
    '''
    Funcion para sacar listas por subcriterio
    '''
    exp_fis=[]
    exp_bio=[]
    sus_fis=[]
    sus_bio=[]
    pesos_1n = []
    for k1, v1 in dicc.items():

        for k2, v2 in v1['criterios'].items():
            pesos_1n.append(k1+"|"+str(v1['w'])+"|"+k2+"|"+str(v2['w']))
            for k3, v3 in v2['criterios'].items():
                if k1=='exposicion' and k2=='fisico':
                    exp_fis.append(v3['ruta'] + "|" + str(v3['w']))
                    #print (k1,v1['w'],k2,v2['w'],k3,v3['w'],v3['ruta'])
                elif k1=='exposicion' and k2=='biologico':
                    exp_bio.append(v3['ruta'] + "|" + str(v3['w']))
                    #print (k1,v1['w'],k2,v2['w'],k3,v3['w'],v3['ruta'])
                elif k1=='susceptibilidad' and k2=='fisico':
                    sus_fis.append(v3['ruta'] + "|" + str(v3['w']))
                    #print (k1,v1['w'],k2,v2['w'],k3,v3['w'],v3['ruta']
                elif k1=='susceptibilidad' and k2=='biologico':
                    sus_bio.append(v3['ruta'] + "|" + str(v3['w']))
                    #print (k1,v1['w'],k2,v2['w'],k3,v3['w'],v3['ruta']
    return exp_fis, exp_bio, sus_fis, sus_bio,pesos_1n

def separa_ruta_pesos(lista):
    rutas =[]
    pesos= []
    for capa in lista:
        rutas.append(capa.split("|")[0])
        pesos.append(capa.split("|")[1])
    return rutas,pesos
    
def rutas_pesos_globales(dicc):
    '''
    Esta funcion recibe un diccionario de la siguiente estructura ...
    
    regresa listas individuales de los criterios principales (Exposicion,
    susceptibilidad y capacidad adatativa.
    Estas listas llevan la ruta y el peso separadados por el carácter "|"
    '''
    exposicion=[]
    susceptibilidad=[]
    resiliencia=[]
    for k1, v1 in dicc.items():
        for k2, v2 in v1['criterios'].items():
            for k3, v3 in v2['criterios'].items():
                if k1=='exposicion':
                    exposicion.append(v3['ruta'] + "|" + str(v2['w']*v3['w']))
                    #print (k1,k2,v2['w'],k3,v3['w'],v3['ruta'])
                elif k1=='susceptibilidad':
                    susceptibilidad.append(v3['ruta'] + "|" + str(v2['w']*v3['w']))
                    #print (k1,k2,v2['w'],k3,v3['w'],v3['ruta'])
                elif k1=='resiliencia':
                    resiliencia.append(v3['ruta'] + "|" + str(v2['w']*v3['w']))
                    #print (k1,k2,v2['w'],k3,v3['w'],v3['ruta'])
    return exposicion,susceptibilidad,resiliencia
def quita(dicc,key):
    '''
    Esta función retira un elemento del diccionario y regresa un nuevo diccionario 
    sin dicho elemento <<dicc_q>>.

    :param dicc: Diccionario con la estructura requerida
    :type dicc: diccionario
    :param key: nombre de la variable a quitar
    :type key: String

    '''
    
    dicc_q = copy.deepcopy(dicc)
    k_1 =[]
    k_2 =[]
    k_3 =[]
    for k1, v1 in dicc_q.items():
        for k2, v2 in v1['criterios'].items():
             for k3, v3 in v2['criterios'].items():   
                  if k3 == key:
                      #print (v3['w'])
                      k_1.append(k1)
                      k_2.append(k2)
                      k_3.append(k3)
    for i in range(len(k_1)):
        kk_1 = k_1[i]
        kk_2 = k_2[i]
        kk_3 = k_3[i]
        dicc_q[kk_1]['criterios'][kk_2]['criterios'].pop(kk_3)
        if len(dicc_q[kk_1]['criterios'][kk_2]['criterios']) == 0:
            dicc_q[kk_1]['criterios'].pop(kk_2)
            if len(dicc_q) == 0:
                dicc_q.pop(kk_1)
    
    return dicc_q
    
def reescala(dicc_q):
    '''
    Esta función rescala un diccionario que se le a quitado un criterio
    y regresa el diccionario con los pesos rescalados

    :param dicc_q: salida de la función *quita* 
    
    '''

    dicc_r = copy.deepcopy(dicc_q)
    suma = 0
    for k1, v1 in dicc_r.items():
        suma += v1['w']
    for k1, v1 in dicc_r.items():
        v1['w'] = v1['w']/suma
        
    for k1, v1 in dicc_r.items():
        suma = 0
        for k2, v2 in v1['criterios'].items():
            suma += v2['w']
        for k2, v2 in v1['criterios'].items():
            v2['w'] = v2['w'] / suma
            
            
    for k1, v1 in dicc_r.items():
        for k2, v2 in v1['criterios'].items():      
            suma = 0
            for k3, v3 in v2['criterios'].items():   
                suma += v3['w']
            for k3, v3 in v2['criterios'].items():
                v3['w'] = v3['w'] / suma
    
    return dicc_r
    
def quita_reescala(dicc,key):
    '''
    Función que integra las funciones quita y reescala y regresa
    un diccionario sin la variable y con los pesos reescalados.
    
    :param dicc: Diccionario con la estructura requerida
    :type dicc: diccionario
    :param key: nombre de la variable a quitar
    :type key: String
    '''
    dicc_q = quita(dicc,key)
    dicc_r = reescala(dicc_q)
    return dicc_r
def pesos_superiores(dicc):
    pesos=[]
    for k1,v1 in dicc.items():
        #print (k1,v1['w'])
        pesos.append([k1,str(v1['w'])])
    return pesos 



def analisis_sensibilidad(dicc,p_procesamiento):
    # ----- GENERACIÓN DE LAS CAPAS CONSIDERANDO TODOS LOS ELEMENTOS ----- #
    '''
    :param dicc: diccionario con nombre de los criterios, rutas y ponderaciones ordenados por componente y subcomponente
    :type dicc: dict

    :param p_procesamiento: Directorio de salida para el procesamiento de los productos necesarios para el cálculo del analisis de sensibilidad
    :type p_procesamiento: str 


    '''
    exposicion_total,susceptibilidad_total,resiliencia_total = rutas_pesos_globales(dicc)
    path_exp_t,w_exp_t = separa_ruta_pesos(exposicion_total)
    path_sus_t,w_sus_t = separa_ruta_pesos(susceptibilidad_total)
    path_res_t,w_res_t = separa_ruta_pesos(resiliencia_total)

    ecuacion_exp_t = ecuacion_clp(w_exp_t)
    ecuacion_sus_t = ecuacion_clp(w_sus_t)
    ecuacion_res_t = ecuacion_clp(w_res_t)

    salida_exposicion_t = p_procesamiento+"exposicion.tif"
    salida_susceptibilidad_t = p_procesamiento+"susceptibilidad.tif"
    salida_resiliencia_t = p_procesamiento+"resiliencia.tif"


    crea_capa(ecuacion_exp_t,path_exp_t,salida_exposicion_t)
    crea_capa(ecuacion_sus_t,path_sus_t,salida_susceptibilidad_t)
    crea_capa(ecuacion_res_t,path_res_t,salida_resiliencia_t)

    ## --- Creación de la capa de vulnerabilidad ---##

    #salida_vulnerabilidad_exp_sus= p_procesamiento+"tp_vulnerabilidad_exp_sus.tif"
    salida_vulnerabilidad_exp_sus_res= p_procesamiento+"vulnerabilidad.tif"

    #lista_exp_sus = [salida_exposicion_t,salida_susceptibilidad_t]
    lista_exp_sus_res = [salida_exposicion_t,salida_susceptibilidad_t,salida_resiliencia_t]
    #ecuacion_exp_sus =ecuacion_vulnerabilidad(1)
    ecuacion_exp_sus_res =ecuacion_vulnerabilidad(2)

    #rea_capa(ecuacion_exp_sus,lista_exp_sus,salida_vulnerabilidad_exp_sus)
    crea_capa(ecuacion_exp_sus_res,lista_exp_sus_res,salida_vulnerabilidad_exp_sus_res)

    vulnerabilidad_total_media = media_raster(salida_vulnerabilidad_exp_sus_res)
    exp_media_total = media_raster(salida_exposicion_t)
    sus_media_total = media_raster(salida_susceptibilidad_t)
    res_media_total = media_raster(salida_resiliencia_t)



    #---- TERMINA ---#

    #--- ANALISIS DE SENSIBILIDAD ----#


    archivo = open(p_procesamiento+"analisis_sensibilidad.csv","w")
    archivo.write("criterio,vulnerabilidad,valor_sensibilidad\n")
    archivo.write("all elements,"+str(round(exp_media_total,3))+",,"+str(round(sus_media_total,3))+",,"+str(round(res_media_total,3))+",,"+str(round(vulnerabilidad_total_media,3))+"\n")
        
    criterios = lista_criterios(dicc) #obtiene criterios del diccionario principal
    cont=0
    for criterio in criterios:
        cont +=1
        print ("procensado criterio: ",criterio,"  ",cont,"de",len(criterios))
        dicc2  = quita_reescala(dicc,criterio)
        

        exposicion,susceptibilidad,resiliencia = rutas_pesos_globales(dicc2) #separa los subcriterios por criterios

        path_exp,w_exp = separa_ruta_pesos(exposicion)
        path_sus,w_sus = separa_ruta_pesos(susceptibilidad)
        path_res,w_res = separa_ruta_pesos(resiliencia)

        ecuacion_exp = ecuacion_clp(w_exp)
        ecuacion_sus = ecuacion_clp(w_sus)
        ecuacion_res = ecuacion_clp(w_res)

        salida_exposicion = p_procesamiento+"tp_exposicion_sin_"+criterio+".tif"
        salida_susceptibilidad = p_procesamiento+"tp_suscep_sin_"+criterio+".tif"
        salida_resiliencia = p_procesamiento+"tp_resilencia_sin_"+criterio+".tif"

        salida_vulnerabilidad = p_procesamiento+"tp_vulnerabilidad_sin_"+criterio+".tif"
        print(salida_exposicion.split("/")[-1:],"|",salida_susceptibilidad.split("/")[-1:])
        crea_capa(ecuacion_exp,path_exp,salida_exposicion)
        crea_capa(ecuacion_sus,path_sus,salida_susceptibilidad)
        crea_capa(ecuacion_res,path_res,salida_resiliencia)
            
        ## --- Creación de la capa de vulnerabilidad --- ##

        lista_c = [salida_exposicion,salida_susceptibilidad,salida_resiliencia]
        ecuacion_vul_01 =ecuacion_vulnerabilidad(2)
        crea_capa(ecuacion_vul_01,lista_c,salida_vulnerabilidad)

        ## --- Promedios de los productos ---- ## 
        vulnerabilidad_media = media_raster(salida_vulnerabilidad)
        exp_media = media_raster(salida_exposicion)
        sus_media = media_raster(salida_susceptibilidad)
        res_media = media_raster(salida_resiliencia)
        
        ##---  Cálculo de la sensibilidad ---##
        sensibilidad_exp_calculada = round((abs((exp_media_total-exp_media))/exp_media_total),3)
        sensibilidad_sus_calculada = round((abs((sus_media_total-sus_media))/sus_media_total),3)
        sensibilidad_res_calculada = round((abs((res_media_total-res_media))/res_media_total),3)
        sensibilidad_calculada = round((abs((vulnerabilidad_total_media-vulnerabilidad_media))/vulnerabilidad_total_media),3)
        archivo.write(criterio+","+\
                        str(round(vulnerabilidad_media,3))+","+\
                        str(sensibilidad_calculada)+"\n")
        
    archivo.close()




### rutas de entrada y salida


dicc = {
    'exposicion': {'w':0.33,
                        'criterios':{'biologico':{'w':0.50,
                                                        'criterios':{'v_acuatica':{'w':0.16,'ruta':'C:/analisis_sensibilidad/insumos/exposicion/biologica/v_acuatica_yuc/fv_v_acuatica_yuc.tif'},
                                                                        'v_costera':{ 'w':0.84,'ruta':'C:/analisis_sensibilidad/insumos/exposicion/biologica/v_costera_yuc/fv_v_costera_distancia_yuc.tif'}}},
                                        'fisico':{'w':0.50,
                                                    'criterios':{'elevacion':{ 'w':0.87,'ruta':'C:/analisis_sensibilidad/insumos/exposicion/fisica/elev_yuc/fv_elevacion_yuc.tif'},
                                                                    'ancho_playa':{'w':0.13,'ruta':'C:/analisis_sensibilidad/insumos/exposicion/fisica/ancho_playa_yuc/fv_distancia_playa_yuc.tif'}
    }}}},
    'susceptibilidad': {'w':0.33,
                            'criterios':{'biologico':{'w':0.50 ,
                                                            'criterios':{'v_costera':{ 'w':1.0,'ruta':'C:/analisis_sensibilidad/insumos/sensibilidad/biologica/v_costera_yuc/fv_v_costera_presencia_yuc.tif'}}},
                                            'fisico':{'w':0.50,
                                                        'criterios':{'elevacion':{ 'w':0.26,'ruta':'C:/analisis_sensibilidad/insumos/sensibilidad/fisica/elev_yuc/fv_elevacion_yuc.tif' },
                                                                        'duna_costera':{'w':0.10,'ruta':'C:/analisis_sensibilidad/insumos/sensibilidad/fisica/duna_yuc/fv_duna_yuc.tif'},
                                                                        'tipo_litoral':{'w':0.64,'ruta':'C:/analisis_sensibilidad/insumos/sensibilidad/fisica/t_litoral_yuc/fv_tipo_litoral_yuc.tif'}
    }}}},
    'resiliencia': {'w':0.33,
                            'criterios':{'biologico':{'w':0.50 ,
                                                            'criterios':{'biodiversidad':{'w':0.50,'ruta':'C:/analisis_sensibilidad/insumos/resiliencia/biologica/biodiversidad/fv_biodiversidad_yuc.tif'},
                                                                            'servicios_ambientales':{'w':0.50,'ruta':'C:/analisis_sensibilidad/insumos/resiliencia/biologica/serv_ambientales/fv_servicios_ambientales_yuc.tif'}}},
                                        'fisico':{'w':0.50,
                                                        'criterios':{'ancho_playa':{'w':0.62,'ruta':'C:/analisis_sensibilidad/insumos/resiliencia/fisica/ancho_playa_yuc/fv_ancho_playa_yuc.tif'},
                                                                    'duna_costera':{'w':0.27,'ruta':'C:/analisis_sensibilidad/insumos/resiliencia/fisica/duna_yuc/fv_duna_yuc.tif'},
                                                                    'elevacion':{'w':0.06,'ruta':'C:/analisis_sensibilidad/insumos/resiliencia/fisica/elev_yuc/fv_elev_yuc.tif'},
                                                                    'tipo_litoral':{'w':0.05,'ruta':'C:/analisis_sensibilidad/insumos/resiliencia/fisica/t_litoral_yuc/fv_tipo_litoral_yuc.tif'}
    }}}}

    }

p_procesamiento = 'C:/analisis_sensibilidad/salida/'

analisis_sensibilidad(dicc,p_procesamiento)
