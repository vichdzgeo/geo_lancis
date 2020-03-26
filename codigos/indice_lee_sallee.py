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
    for a,b in zip(vlayer_base.getFeatures(),vlayer_model.getFeatures()):
        if a[campo_categoria]==categoria:
            union.append(a[id])
        if b[campo_categoria]==categoria:
            union.append(a[id])
        if a[campo_categoria]==categoria and b[campo_categoria]==categoria:
            interseccion.append(b[id])

    union_conjunto = set(union)
    if len(union_conjunto)==0:
        indice_lee_count=10
    else:
        indice_lee_count = round((len(interseccion) / len(union_conjunto)),4)

    area_interseccion =0
    area_union =0

    for i in vlayer_base.getFeatures():
        for ageb_union in union_conjunto:
            if i[id]==ageb_union:
                area_union += i.geometry().area()
        for ageb_interseccion in interseccion:
            if i[id]==ageb_interseccion:
                area_interseccion += i.geometry().area()
    if area_union ==0:
        indice_lee=10
    else:
        indice_lee = round(area_interseccion / area_union,3)
    return indice_lee
    


# ## Cálculo del índice Lee Sallee
# path_sig = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/equidistante/"
# #vlayer_base = QgsVectorLayer(path_sig + 'action_budget_bajo_asentamientos.shp',"","ogr")
# #vlayer_model = QgsVectorLayer(path_sig + 'system_budget_bajo_asentamientos.shp',"","ogr")
# #
# #path = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/equidistante/"
# lista_nombres = lista_shp(path_sig)
# list2=lista_nombres[:1]
# path_csv = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/comparacion_equidistante_cat5.csv'

# matrix=open(path_csv,"w")
# matrix.write('esc,'+','.join(lista_nombres)+"\n")
# print (time.strftime("%H:%M:%S"))
# for nombre_1 in lista_nombres:
#     #print("comparando: ",nombre_1)
#     vlayer_base = QgsVectorLayer(path_sig + nombre_1+'.shp',"","ogr")
#     renglon=nombre_1+","
#     for nombre_2 in lista_nombres:
#         vlayer_model = QgsVectorLayer(path_sig + nombre_2+'.shp',"","ogr")

#         #print(nombre_1,"con_este",nombre_2)
#         index_lee = indice_lee_salee(vlayer_base,vlayer_model,'cat_vul',5,id='ageb_id')
#         renglon+=(str(index_lee)+",")
#     renglon+='\n'
#     matrix.write(renglon)
# print('fin')
# matrix.close()
# print (time.strftime("%H:%M:%S"))