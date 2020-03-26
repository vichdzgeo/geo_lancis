# -*- coding: utf-8 -*-

import os
from  qgis import *
from  qgis.core import *
import time 
def lista_shp(path_carpeta):
    '''


    :param path_carpeta: ruta que contiene los archivos shape a procesar
    :type path_carpeta: String
    '''
    for root, dirs, files in os.walk(path_carpeta):
        lista = []
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                lista.append(extension[0])
    return lista





def indice_lee_salee(vlayer_base,vlayer_model,campo_categoria,categoria,id='ageb_id'):
    '''

    Esta función regresa el índice Lee-Sallee

    .. math::
        lee\_sallee\_index =  \frac{A\cap B}{A\cup B}

    :param vlayer_base: vector base
    :type vlayer_base: QgsVectorLayer

    :param vlayer_model: Vector modelo 
    :type vlayer_model: QgsVectorLayer

    :param campo_categoria: Nombre del campo que tiene las categorias
    :type campo_categoria: String

    :param categoria: Número de categoria
    :type categoria: int 

    :param id: nombre del campo identificador
    :type id: String
    '''
    union = []
    interseccion = []
    request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

    for a,b in zip(vlayer_base.getFeatures(request),vlayer_model.getFeatures(request)):
        if a[campo_categoria]==categoria:
            union.append(a[id])
        if b[campo_categoria]==categoria:
            union.append(a[id])
        if a[campo_categoria]==categoria and b[campo_categoria]==categoria:
            interseccion.append(b[id])

    union_conjunto = set(union)
    if len(union_conjunto)==0:
        indice_lee_count='*'
    else:
        indice_lee_count = round((len(interseccion) / float(len(union_conjunto))),4)

#    area_interseccion =0
#    area_union =0
#
#    for i in vlayer_base.getFeatures():
#        for ageb_union in union_conjunto:
#            if i[id]==ageb_union:
#                area_union += i.geometry().area()
#        for ageb_interseccion in interseccion:
#            if i[id]==ageb_interseccion:
#                area_interseccion += i.geometry().area()
#    if area_union ==0:
#        indice_lee=10
#    else:
#        indice_lee = round(area_interseccion / area_union,3)
    return indice_lee_count
    


## Cálculo del índice Lee Sallee
path_sig = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/fp15/"
path_sig_2 = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/fp20/"
#vlayer_base = QgsVectorLayer(path_sig + 'action_budget_bajo_asentamientos.shp',"","ogr")
#vlayer_model = QgsVectorLayer(path_sig + 'system_budget_bajo_asentamientos.shp',"","ogr")
#
#path = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/equidistante/"
path_csv = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/comparacion_fp15_escenarios.csv'

escenarios = ['asentamientos','base','increm_cutza','mejora_efi','reduc_agua','reduc_cutza']
arch=open(path_csv,"w")
arch.write('budget_split,'+','.join(escenarios)+"\n")
budget = ['bajo','medio','alto']
for c in range(1,6):
    for bud in budget:
        lista =bud+","
        for escenario in escenarios:
            
            vlayer_base = QgsVectorLayer(path_sig + 'action_budget_'+bud+"_"+escenario+'.shp',"","ogr") 
            vlayer_model = QgsVectorLayer(path_sig + 'system_budget_'+bud+"_"+escenario+'.shp',"","ogr")
            index_lee = indice_lee_salee(vlayer_base,vlayer_model,'cat_vul',c,id='ageb_id')
            lista+=(str(index_lee)+",")
        lista+="\n"
        arch.write(lista)
    arch.write('\n\n')
arch.close()
#    matrix=open(path_csv,"w")
#    matrix.write('esc,'+','.join(lista_nombres)+"\n")
print (time.strftime("%H:%M:%S"))
#    for nombre_1 in lista_nombres:
#        #print("comparando: ",nombre_1)
#        vlayer_base = QgsVectorLayer(path_sig + nombre_1+'.shp',"","ogr")
#        renglon=nombre_1+","
#        for nombre_2 in lista_nombres:
#            vlayer_model = QgsVectorLayer(path_sig_2 + nombre_2+'.shp',"","ogr")
#
#            #print(nombre_1,"con_este",nombre_2)
#            index_lee = indice_lee_salee(vlayer_base,vlayer_model,'cat_vul',c,id='ageb_id')
#            renglon+=(str(index_lee)+",")
#        renglon+='\n'
#        matrix.write(renglon)
#    print('fin')
#    matrix.close()
#    print (time.strftime("%H:%M:%S"))