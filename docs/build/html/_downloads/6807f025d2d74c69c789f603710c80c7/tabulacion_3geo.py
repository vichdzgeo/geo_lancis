import os, errno
from os import listdir,walk
from os.path import isfile, join,splitext
import processing as pr 
from PyQt5.QtWidgets import QInputDialog

def encuentra_noserie(ruta):
    nombre =nombre_capa(ruta)
    for i in range(1,7):
        if str(i) in nombre:
            return i
def lista_shape(path):
    lista_shp=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                ruta = (root.replace("\\","/")+"/").replace("//","/")+name
                lista_shp.append(ruta)
    return lista_shp
def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa
def campos_clases(vector,lista_clases,prefix_field=''):
    '''
    :param vector:
    :type vector:

    :param lista_clases:
    :type lista_clases:
    '''


    for clase in lista_clases:
        campos = [field.name() for field in vector.fields()]
        if not clase in campos:
            vector.dataProvider().addAttributes([QgsField(prefix_field+str(clase),QVariant.Double)])
            vector.updateFields()
def copia(vector,salida):
    '''
    Esta función crea una copia de la capa vectorial con la misma proyección
    :param vector: Objeto vectorial de qgis
    :type vector: Objeto Qgis

    :param salida: Ruta y nombre de la copia de la capa vectorial, en formato
    .shp
    :type salida: String
    '''

    crs=vector.crs()
    clonarv = QgsVectorFileWriter.writeAsVectorFormat(vector,salida,'UTF-8',crs,"ESRI Shapefile")

def vector_to_csv(vector,salida):
    '''
    :param vector: capa vectorial 
    :type vector: vector

    :param salida: ruta de salida del archivo csv
    :type salida: str

    '''
    crs=vector.crs()
    clonarv = QgsVectorFileWriter.writeAsVectorFormat(vector,salida,'utf-8',crs,"CSV")
    
def interseccion(vector_a,vector_b,vector_salida):
    '''
    :param vector_a: Ruta de la capa vectorial A
    :type vector_a: str

    :param vector_b: Ruta de la capa vectorial B
    :type vector_b: str

    :param vector_c: ruta de la capa vectorial resultado de la intersección
    :type vector_c: str

    '''
    dicc={'A':vector_a,
            'B':vector_b,
            'SPLIT':'True',
            'RESULT':vector_salida}
    pr.run("saga:intersect",dicc)

def carpeta_tmp(path_salida):
    carpeta= "tmp"
    path_dir = path_salida+"/"+carpeta

    try:
        os.mkdir(path_dir)
    except OSError as e:
        if e.errno !=errno.EEXIST:
            raise
    
    return path_dir+"/"

def campo_binario(layer):
    campos = [field.name() for field in layer.fields()]
    if not "id_bin" in campos:
        layer.dataProvider().addAttributes([QgsField("id_bin",QVariant.Int)])
        layer.updateFields()
def imprime_campos(layer):

    campos = [field.name() for field in layer.fields()]
    for campo in campos:
        print (campo)


def clasificador_binario(path_v,nombre_campo,path_salida):
    capa_original = QgsVectorLayer(path_v,"","ogr")
    path_v_copia = path_salida+"tp1_"+nombre_capa(path_v)
    copia(capa_original,path_v_copia)
    layer = QgsVectorLayer(path_v_copia,"","ogr")
    request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

    categorias = []
    for i in layer.getFeatures(request):
        categorias.append(i[nombre_campo])

    categorias = list(set(categorias))
    dicc_cat ={}
    for i in range(len(categorias)):
        dicc_cat[i+1]=categorias[i]
    print (dicc_cat)
    print ("Ingrese el número separado por comas de las clases a considerar o si desea considerar todas las categorias\n ingrese la palabra 'TODAS'")
    clave = QInputDialog.getText(None,"Ingrese categorias","ej 1,2,4 ó TODAS")

    campo_binario(layer)
    layer.startEditing()        

    if clave[0].upper() == "TODAS":
        for element in layer.getFeatures():
            element['id_bin']=1
            layer.updateFeature(element)
    else:
        lista = clave[0].split(",")
        lista_faltante = []
        for k,v in dicc_cat.items():
            lista_faltante.append(str(k))
        for l in lista:
            lista_faltante.remove(l)


        for num_cat in lista:
            for element in layer.getFeatures():
                if element[nombre_campo]==dicc_cat[int(num_cat)]:
                    element['id_bin']=1            
                    layer.updateFeature(element)
        for num_cat_f in lista_faltante:
            for element in layer.getFeatures():
                if element[nombre_campo]==dicc_cat[int(num_cat_f)]:
                    element['id_bin']=0           
                    layer.updateFeature(element)
                    
    layer.commitChanges()

    layer.startEditing() 
    elementos_borrar =[]
    for element in layer.getFeatures():
        if element['id_bin']==0:
            elementos_borrar.append(element.id())

    layer.dataProvider().deleteFeatures(elementos_borrar)
        
    layer.commitChanges()

    return path_v_copia

def area_nivel(path_geometria_a,path_geometria_b,path_dir_usv,campo_id_a,campo_clase_usv,clave_capas):

    path_salida_tmp = carpeta_tmp(path_salida)
    capa_a = QgsVectorLayer(path_geometria_a,"","ogr")
    capa_b = QgsVectorLayer(path_geometria_b,"","ogr")
    print("**************************************************************************************")
    print ("Ingrese el nombre del campo de las categorias a elegir en la geometría b")
    imprime_campos(capa_b)
    campo_clases_geometria_b= QInputDialog.getText(None,"Ingrese el nombre del","campo")
    path_geometria_b_clases=clasificador_binario(path_geometria_b,campo_clases_geometria_b[0],path_salida_tmp)
    path_a_b_tp = path_salida_tmp + 'tp_a_b.shp'
    lista_usv =lista_shape(path_dir_usv)
    interseccion(path_geometria_a,path_geometria_b_clases,path_a_b_tp)


    print("**************************************************************************************")
    print ("Ingrese 'area' o 'porcentaje' para expresar el área en las diferentes clases de usv en la geometria b")
    modo =  QInputDialog.getText(None,"Ingrese"," 'area' o 'porcentaje'")


    for path_usv in lista_usv:
        no_serie = encuentra_noserie(path_usv)
        area_b = 'area_'+clave_capas[1]
        print ("procesando serie %d"%no_serie)
        nombre_a_b_c = clave_capas[0]+"_"+clave_capas[1]+'_'+clave_capas[2]+'_s_'+str(no_serie)
        path_producto = path_salida_tmp + nombre_a_b_c + '.shp'
        path_producto_csv= path_salida + nombre_a_b_c +'.csv'
        
        
        usv = QgsVectorLayer(path_usv,"","ogr")
        
        copia(capa_a,path_producto)
        path_tp_inters_producto = path_salida_tmp + 'tp_inters_'+nombre_a_b_c+'.shp'
        

        lista_ids_a = []
        lista_clases = []
        request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

        for id_a in capa_a.getFeatures(request):
            lista_ids_a.append(id_a[campo_id_a])

        for pol in usv.getFeatures(request):
            lista_clases.append(pol[campo_clase_usv]) #id_clases es el nombre de la columna que tiene las clases
        lista_clases =list(set(lista_clases)) # esto es para ordenae
        interseccion(path_a_b_tp,path_usv,path_tp_inters_producto)

        #a la copia de capa_a se le agregan las columnas de categorias
        # para ello la función recibe la capa vectorial y la lista de clases
        producto = QgsVectorLayer(path_producto,"","ogr")
        lista_area_anp_ns=[area_b,'no_serie']
        campos_clases(producto,lista_area_anp_ns)

        # Esta función crea campos conforme el numero de clases
        campos_clases(producto,lista_clases,"clase_")

        consulta = QgsVectorLayer(path_tp_inters_producto,"","ogr")

        producto.startEditing()
        for elemento in lista_ids_a:
            area = 0
            request_mun_o = QgsFeatureRequest().setFilterExpression('"'+campo_id_a+'" ='+str(elemento))
            for anp in consulta.getFeatures(request_mun_o):
                area+= anp.geometry().area()
            for mun in producto.getFeatures(request_mun_o):
                mun[area_b]=round(area/10000.00,2)
                mun['no_serie']=no_serie
                producto.updateFeature(mun)
        producto.commitChanges()

        #calcula el área de usv dentro del area de la capa b contenida en cada geometria de la capa a
        producto.startEditing()
        for clase in lista_clases:
            area=0
            for id_a in lista_ids_a:
                area=0
                request_mun = QgsFeatureRequest().setFilterExpression('"'+campo_id_a+'" ='+str(id_a)+'and "'+campo_clase_usv+'" ='+str(clase))
                request_mun_o = QgsFeatureRequest().setFilterExpression('"'+campo_id_a+'" ='+str(id_a))
                for m in consulta.getFeatures(request_mun):
                    area+=m.geometry().area()
                for mun in producto.getFeatures(request_mun_o):
                    if modo[0].lower()=='area':
                        mun['clase_'+str(clase)]=round(area/10000.00,2) #area en hectareas
                        producto.updateFeature(mun)
                    elif modo[0].lower()=="porcentaje" and mun[area_b] > 0:
                        mun['clase_'+str(clase)]=round(round(area/10000.00,2) / mun[area_b],2) #area en hectareas
                        producto.updateFeature(mun)
                    elif modo[0].lower()=="porcentaje" and mun[area_b] == 0:
                        mun['clase_'+str(clase)]=round(0.000,2) #area en hectareas
                        producto.updateFeature(mun)

        producto.commitChanges()
        vector_to_csv(producto,path_producto_csv)


##-- RUTAS DE LOS INSUMOS --##
path_geometria_a = 'C:/geo_lancis/tabulacion3geo/insumos/muni_2018_utm16.shp'
path_geometria_b = "C:/geo_lancis/tabulacion3geo/insumos/degradacion_suelo_yuc.shp"
path_dir_usv = "C:/geo_lancis/tabulacion3geo/insumos/usv/"

##-- NOMBRE DEL CAMPO ID PERTENECIENTE A LA GEOMETRIA A --##
campo_id_geometria_a = 'cve_mun'
##-- NOMBRE DEL CAMPO ID  DE LA GEOMETRIA C --##
campo_clase_usv = 'id_clase2'

##-- LISTA DE IDENTIFICADORES DE TRES CARACTERES PARA LAS GEOMETRIAS --#
clave_capas=['mun','deg','usv']

## --RUTA DE SALIDA--##
path_salida = "C:/geo_lancis/tabulacion3geo/"

area_nivel(path_geometria_a,path_geometria_b,path_dir_usv,campo_id_geometria_a,campo_clase_usv,clave_capas)




