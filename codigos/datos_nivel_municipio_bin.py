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
    anp = QgsVectorLayer(path_v,"","ogr")
    path_v_copia = path_salida+"tp1_"+nombre_capa(path_v)
    copia(anp,path_v_copia)
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

    clave = QInputDialog.getText(None,"Ingrese el número separado por comas de las clases a considerar o si desea considerar todas las categorias","ej 1,2,4 ó TODAS")

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

def area_nivel(path_geometria_a,path_geometria_b,path_dir_usv,campo_mun,campo_clase_usv,clave_capas):

    path_salida_tmp = carpeta_tmp(path_salida)
    municipios = QgsVectorLayer(path_geometria_a,"","ogr")
    anp = QgsVectorLayer(path_geometria_b,"","ogr")
    print("**************************************************************************************")
    print ("Ingrese el nombre del campo de las categorias a elegir en la geometría b")
    imprime_campos(anp)
    campo_clases_geometria_b= QInputDialog.getText(None,"Ingrese el nombre del","campo")
    path_anp=clasificador_binario(path_geometria_b,campo_clases_geometria_b[0],path_salida_tmp)
    path_mun_anp_tp = path_salida_tmp + 'tp_a_b.shp'
    lista_usv =lista_shape(path_dir_usv)
    interseccion(path_geometria_a,path_geometria_b,path_mun_anp_tp)


    print("**************************************************************************************")
    print ("Ingrese 'area' o 'porcentaje' para expresar el área en las diferentes clases de usv en la geometria b")
    modo =  QInputDialog.getText(None,"Ingrese"," 'area' o 'porcentaje'")


    for path_usv in lista_usv:
        no_serie = encuentra_noserie(path_usv)
        area_b = 'area_'+clave_capas[1]
        print ("procesando serie %d"%no_serie)
        serie_anp_usv = clave_capas[0]+"_"+clave_capas[1]+'_'+clave_capas[2]+'_s_'+str(no_serie)
        path_mun_anp_usv = path_salida + serie_anp_usv + '.shp'
        path_mun_anp_usv_csv= path_salida + serie_anp_usv+'.csv'
        
        
        usv = QgsVectorLayer(path_usv,"","ogr")
        
        copia(municipios,path_mun_anp_usv)
        path_interseccion_anp_usv = path_salida_tmp + 'tp_inters_'+serie_anp_usv+'.shp'
        

        lista_mun = []
        lista_clases = []
        lista_mun_anp  = []
        request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

        for municipio in municipios.getFeatures(request):
            lista_mun.append(municipio[campo_mun])

        for pol in usv.getFeatures(request):
            lista_clases.append(pol[campo_clase_usv]) #id_clases es el nombre de la columna que tiene las clases
        lista_clases =list(set(lista_clases)) # esto es para ordenae
        interseccion(path_mun_anp_tp,path_usv,path_interseccion_anp_usv)

        #a la copia de municipios se le agregan las columnas de categorias
        # para ello la función recibe la capa vectorial y la lista de clases
        mun_anp_usv = QgsVectorLayer(path_mun_anp_usv,"","ogr")
        lista_area_anp_ns=[area_b,'no_serie']
        campos_clases(mun_anp_usv,lista_area_anp_ns)

        # Esta función crea campos conforme el numero de clases
        campos_clases(mun_anp_usv,lista_clases,"clase_")

        consulta_mun_anp = QgsVectorLayer(path_interseccion_anp_usv,"","ogr")

        mun_anp_usv.startEditing()
        for elemento in lista_mun:
            area = 0
            request_mun_o = QgsFeatureRequest().setFilterExpression('"'+campo_mun+'" ='+str(elemento))
            for anp in consulta_mun_anp.getFeatures(request_mun_o):
                area+= anp.geometry().area()
            for mun in mun_anp_usv.getFeatures(request_mun_o):
                mun[area_b]=round(area/10000.00,2)
                mun['no_serie']=no_serie
                mun_anp_usv.updateFeature(mun)
        mun_anp_usv.commitChanges()

        #calcula el área de usv dentro del area de anp contenida en el municipio
        mun_anp_usv.startEditing()
        for clase in lista_clases:
            area=0
            for municipio in lista_mun:
                area=0
                request_mun = QgsFeatureRequest().setFilterExpression('"'+campo_mun+'" ='+str(municipio)+'and "'+campo_clase_usv+'" ='+str(clase))
                request_mun_o = QgsFeatureRequest().setFilterExpression('"'+campo_mun+'" ='+str(municipio))
                for m in consulta_mun_anp.getFeatures(request_mun):
                    area+=m.geometry().area()
                for mun in mun_anp_usv.getFeatures(request_mun_o):
                    if modo[0].lower()=='area':
                        mun['clase_'+str(clase)]=round(area/10000.00,2) #area en hectareas
                        mun_anp_usv.updateFeature(mun)
                    elif modo[0].lower()=="porcentaje" and mun[area_b] > 0:
                        mun['clase_'+str(clase)]=round(round(area/10000.00,2) / mun[area_b],2) #area en hectareas
                        mun_anp_usv.updateFeature(mun)
                    elif modo[0].lower()=="porcentaje" and mun[area_b] == 0:
                        mun['clase_'+str(clase)]=round(0.000,2) #area en hectareas
                        mun_anp_usv.updateFeature(mun)

        mun_anp_usv.commitChanges()
        vector_to_csv(mun_anp_usv,path_mun_anp_usv_csv)

path_geometria_a = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/mun_region/muni_2018_utm16.shp'
path_geometria_b = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/insumos/ambiente/sds/anps_sds/anps.shp"
path_dir_usv = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/usv_v2/"

campo_id_geomatria_a = 'cve_mun'

clave_capas=['mun','anp','usv']

for clasificacion in range(2,5):
    path_salida = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/nivel_municipios_anp_usv/clasificacion_%d/"%clasificacion
    campo_clase_usv = 'id_clase%d'%clasificacion
    area_nivel(path_geometria_a,path_geometria_b,path_dir_usv,campo_id_geomatria_a,campo_clase_usv,clave_capas)




