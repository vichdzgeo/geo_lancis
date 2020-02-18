
from  qgis import *
from  qgis.core import *




def indice_lee_salee(vlayer_base,vlayer_model,campo_categoria,categoria,id='ageb_id'):
    '''

    Esta función regresa el índice Lee-Sallee

    .. math::
        lee\_sallee\_index =  \frac{A\cap B}{A\cup B}

    param vlayer_base: vector base
    type vlayer_base: QgsVectorLayer

    param vlayer_model: Vector modelo 
    type vlayer_model: QgsVectorLayer

    param campo_categoria: Nombre del campo que tiene las categorias
    type campo_categoria: String

    param categoria: Número de categoria
    type categoria: int 

    param id: nombre del campo identificador
    type id: String
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
    indice_lee = round(area_interseccion / area_union,4)
    return indice_lee
    


## Cálculo del índice Lee Sallee
path_sig = "C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/lee_sallee/"
vlayer_base = QgsVectorLayer(path_sig + 'insumos/action_budget_medio_base.shp',"","ogr")
vlayer_model = QgsVectorLayer(path_sig + 'insumos/action_budget_bajo_sin_extraccion.shp',"","ogr")



index_lee = indice_lee_salee(vlayer_base,vlayer_model,'cat_vul',5,id='ageb_id')
print (index_lee)
