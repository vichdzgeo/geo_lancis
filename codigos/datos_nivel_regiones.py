import processing as pr 

def campos_clases(vector,lista_clases):
    '''
    :param vector:
    :type vector:

    :param lista_clases:
    :type lista_clases:
    '''


    for clase in lista_clases:

        vector.dataProvider().addAttributes([QgsField("clase_"+str(clase),QVariant.Double)])
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
#    if formato == "gpkg":
#        clonarv = QgsVectorFileWriter.writeAsVectorFormat(vector,salida,'utf-8',crs,"GPKG")
#    else:
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
path_mun = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/regiones/regiones_yuc2.shp'
for clasificacion in range(2,5):
    id_clase = "id_clase"+str(clasificacion)
    for i in range(1,7):
        print ("procesando serie %d"%i)
        path_usv = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/usv_v2/usv_serie"+str(i)+"_yuc.shp"
        serie = 'reg_usv_s'+str(i)+"_c"+str(clasificacion)
        #Ruta de la capa vectorial que tendrá la información a nivel municipal
        path_mun_usv= 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/nivel_regiones/clasificacion_'+str(clasificacion)+"/"+serie+'.shp'
        path_mun_usv_csv= 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/nivel_regiones/clasificacion_'+str(clasificacion)+"/"+serie+'.csv'
        #Se declaran las variables como capas vectoriales 
        municipios = QgsVectorLayer(path_mun,"","ogr")
        usv = QgsVectorLayer(path_usv,"","ogr")

        # Se crea una copia 
        copia(municipios,path_mun_usv) #crea una copia de la capa oficial de municipios


        # Tambien se declara la ruta y nombre de la capa resultante
        path_interseccion = 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/nivel_regiones/tp_inters_'+serie+'.shp'





        #Se generan unas listas de valores unicos para municipios y para las clases
        lista_mun = []
        lista_clases = []

        request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        for municipio in municipios.getFeatures(request):
            lista_mun.append(municipio['id_region'])

        for pol in usv.getFeatures(request):
            lista_clases.append(pol[id_clase]) #id_clases es el nombre de la columna que tiene las clases
        lista_clases =list(set(lista_clases)) # esto es para ordenar de menor a mayor la clase


        #Se realiza la intersección entre la copia de municipios y la capa de USV
        interseccion(path_mun_usv,path_usv,path_interseccion) 

        #a la copia de municipios se le agregan las columnas de categorias
        # para ello la función recibe la capa vectorial y la lista de clases
        mun_usv = QgsVectorLayer(path_mun_usv,"","ogr")
        # Esta función crea campos conforme el numero de clases
        campos_clases(mun_usv,lista_clases)

        #Se declara como capa vectorial la ruta de salida resultante de la interseccion
        consulta_interect = QgsVectorLayer(path_interseccion,"","ogr")


        mun_usv.startEditing()
        for clase in lista_clases:
            area=0
            for municipio in lista_mun:
                area=0
                request_mun = QgsFeatureRequest().setFilterExpression('"id_region" ='+str(municipio)+'and "'+id_clase+'" ='+str(clase))
                request_mun_o = QgsFeatureRequest().setFilterExpression('"id_region" ='+str(municipio))
                for m in consulta_interect.getFeatures(request_mun):
                    area+=m.geometry().area()
                for mun in mun_usv.getFeatures(request_mun_o):
                    mun['clase_'+str(clase)]=round(area/10000.00,2) #area en hectareas
                    mun_usv.updateFeature(mun)
                #print(municipio,clase,(round(area,3)))

        mun_usv.commitChanges()


        vector_to_csv(mun_usv,path_mun_usv_csv)






