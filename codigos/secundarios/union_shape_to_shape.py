def union_shape_to_shape(path_vector_base,path_vector_join,vector_id,bd_csv_id,path_salida):

    '''
    Funcion para unir una base de datos csv a un archivo shapefile, por medio de un campo en comun.
    El resultado es una nueva capa vectorial con la union tabular.
    Parametros
    path_csv: ruta del archivo csv, usar / en vez de '\'
    path_vector: ruta de la capa vectorial
    n_campo_comun: nombre del campo en comun
    path_salida:ruta de salida para la nueva capa vectorial que contiene la union
    '''
    vector_base = QgsVectorLayer(path_vector_base, "", "ogr")
    QgsProject.instance().addMapLayer(vector_base)
    #abre  el archivo csv

    if path_vector_join.endswith('.shp'):
        vector_join = QgsVectorLayer(path_vector_join, "", "ogr")
        
    elif path_vector_join.endswith('.csv'):

        bd_csv_uri = "file:///" \
                        + path_vector_join \
                        + "?delimiter=%s&encoding=%s" % (",", "utf-8")
        vector_join = QgsVectorLayer(bd_csv_uri, "", "delimitedtext")


    
    
    QgsProject.instance().addMapLayer(vector_join)

    #Nombre de los campos de ID para relacionar las tablas
    #union del archivo csv y vector.
    
    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinFieldName(bd_csv_id)
    joinObject.setTargetFieldName(vector_id)
    joinObject.setJoinLayerId(vector_join.id())
    joinObject.setPrefix('')
    joinObject.setUsingMemoryCache(True)
    joinObject.setJoinLayer(vector_join)
    vector_base.addJoin(joinObject)
    print ("fFFFF")
    QgsVectorFileWriter.writeAsVectorFormat(vector_base,path_salida,'utf-8',vector_base.crs(),"ESRI Shapefile")
    


path_vector_join ='C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/equidistante\action_budget_alto_asentamientos.shp'
path_vector_base='C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/insumos/consumo/agebs_consumo_deciles.shp'
vector_id = 'ageb_id'
bd_csv_id = 'ageb_id'
path_salida = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/insumos/consumo/agebs_cons_dec_action_budget_alto_asentamientos.shp'
union_shape_to_shape(path_vector_base,path_vector_join,vector_id,bd_csv_id,path_salida)
