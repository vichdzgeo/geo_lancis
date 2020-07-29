import processing as pr 

def campos_clases(vector,lista_clases,prefix_field=''):
    '''
    :param vector:
    :type vector:

    :param lista_clases:
    :type lista_clases:
    '''


    for clase in lista_clases:

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
    clonarv = QgsVectorFileWriter.writeAsVectorFormat(vector,salida,'utf-8',crs,"ESRI Shapefile")

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


# Ruta de los insumos
path_mun = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/mun_region/muni_2018_utm16.shp'
path_dir_usv = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/usv_v2/"
path_salida = 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/nivel_municipios/anp_usv_mun/'
path_anp = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/insumos/ambiente/sds/anps_sds/anps_federal_estatal.shp"
path_mun_anp_tp = path_salida + 'tp_mun_anp.shp'
interseccion(path_mun,path_anp,path_mun_anp_tp)

for i in range(1,7):
    print ("procesando serie %d"%i)
    path_usv = path_dir_usv + "usv_serie"+str(i)+"_yuc.shp"
    serie_anp_usv = 'mun_anp_usv_s_'+str(i)
    #Ruta de la capa vectorial que tendrá la información a nivel municipal
    path_mun_anp_usv = path_salida + serie_anp_usv + '.shp'
    path_mun_anp_usv_csv= path_salida + serie_anp_usv+'.csv'
    #Se declaran las variables como capas vectoriales 
    municipios = QgsVectorLayer(path_mun,"","ogr")
    usv = QgsVectorLayer(path_usv,"","ogr")
    anp = QgsVectorLayer(path_anp,"","ogr")
    # Se crea una copia 
    copia(municipios,path_mun_anp_usv) #crea una copia de la capa oficial de municipios
    # Tambien se declara la ruta y nombre de la capa resultante
    
    path_interseccion_anp_usv = path_salida + 'tp_inters_'+serie_anp_usv+'.shp'
    
    #Se generan unas listas de valores unicos para municipios y para las clases
    lista_mun = []
    lista_clases = []
    lista_mun_anp  = []
    request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

    for municipio in municipios.getFeatures(request):
        lista_mun.append(municipio['cve_mun'])

    for pol in usv.getFeatures(request):
        lista_clases.append(pol['id_clase']) #id_clases es el nombre de la columna que tiene las clases
    lista_clases =list(set(lista_clases)) # esto es para ordenar de menor a mayor la clase

    for an in anp.getFeatures(request):
        lista_mun_anp.append(an['id']) #id_clases es el nombre de la columna que tiene las clases

    lista_mun_anp =list(set(lista_mun_anp)) # esto es para ordenar de menor a mayor la clase




    #Se realiza la intersección entre la copia resultante de la cruza de anp y municipios  y la capa de USV
    interseccion(path_mun_anp_tp,path_usv,path_interseccion_anp_usv)
 

    #a la copia de municipios se le agregan las columnas de categorias
    # para ello la función recibe la capa vectorial y la lista de clases
    mun_anp_usv = QgsVectorLayer(path_mun_anp_usv,"","ogr")

    lista_area_anp=['area_anp']
    campos_clases(mun_anp_usv,lista_area_anp)

    lista_area_anp=['no_serie']
    campos_clases(mun_anp_usv,lista_area_anp)
    # Esta función crea campos conforme el numero de clases
    campos_clases(mun_anp_usv,lista_clases,"clase_")

    
    consulta_mun_anp = QgsVectorLayer(path_interseccion_anp_usv,"","ogr")


 
    # calcula el area total de ANP contenida en un municipio, sin considerar si es federal o estatal
    mun_anp_usv.startEditing()
    for elemento in lista_mun:
        area = 0
        request_mun_o = QgsFeatureRequest().setFilterExpression('"cve_mun" ='+str(elemento))
        for anp in consulta_mun_anp.getFeatures(request_mun_o):
            area+= anp.geometry().area()
        for mun in mun_anp_usv.getFeatures(request_mun_o):
            mun['area_anp']=round(area/10000.00,2)
            mun['no_serie']=i
            mun_anp_usv.updateFeature(mun)
    mun_anp_usv.commitChanges()

    #calcula el área de usv dentro del area de anp contenida en el municipio

    mun_anp_usv.startEditing()
    for clase in lista_clases:
        area=0
        for municipio in lista_mun:
            area=0
            request_mun = QgsFeatureRequest().setFilterExpression('"cve_mun" ='+str(municipio)+'and "id_clase" ='+str(clase))
            request_mun_o = QgsFeatureRequest().setFilterExpression('"cve_mun" ='+str(municipio))
            for m in consulta_mun_anp.getFeatures(request_mun):
                area+=m.geometry().area()
            for mun in mun_anp_usv.getFeatures(request_mun_o):
                mun['clase_'+str(clase)]=round(area/10000.00,2) #area en hectareas
                mun_anp_usv.updateFeature(mun)
            #print(municipio,clase,(round(area,3)))

    mun_anp_usv.commitChanges()





    vector_to_csv(mun_anp_usv,path_mun_anp_usv_csv)







