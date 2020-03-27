import processing as pr 

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
    
    
def interseccion(vector_a,vector_b,vector_salida):
    dicc={'A':vector_a,
            'B':vector_b,
            'SPLIT':1,
            'RESULT':vector_salida}
    pr.run("saga:intersect",dicc)
    

path_mun = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/insumos/limites/inegi/div_pol_mpio_2018/muni_2018_utm16.shp'
municipios = QgsVectorLayer(path_mun,"","ogr")
path_usv = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/usv_partes_sencillas/usv_serie6_v2.shp"
usv = QgsVectorLayer(path_usv,"","ogr")


lista_mun = []
lista_clases = []
request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
for municipio in municipios.getFeatures(request):
    lista_mun.append(municipio['cve_mun'])

for pol in usv.getFeatures(request):
    lista_clases.append(pol['id_clases'])
lista_clases =list(set(lista_clases))
path_interseccion = 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/nivel_municipios/tp_inters_mun_usv.shp'
#interseccion(path_mun,path_usv,path_interseccion)

path_mun_usv= 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/nivel_municipios/mun_usv.shp'
copia(municipios,path_mun_usv)
mun_usv = QgsVectorLayer(path_mun_usv,"","ogr")

lista_mun=['060']
id_clases=[1]
for clase in lista_clases:
    mun_usv.dataProvider().addAttributes([QgsField("clase_"+str(clase), QVariant.Double)])


consulta_interect = QgsVectorLayer(path_interseccion,"","ogr")

for municipio in lista_mun:
    request_mun_o = QgsFeatureRequest().setFilterExpression('"cve_mun" ='+str(municipio)).setFlags(QgsFeatureRequest.NoGeometry)
    for mun in mun_usv.getFeatures(request_mun_o):
        for clase in lista_clases:
            area= 0
            request_mun = QgsFeatureRequest().setFilterExpression('"cve_mun" ='+str(municipio)+'and "id_clases" ='+str(clase))
            for m in consulta_interect.getFeatures(request_mun):
                area+=m.geometry().area()
            print (area)
            mun['clase_'+str(clase)]=(round(area,3))
            
            mun_usv.updateFeature(mun)

    mun_usv.commitChanges()

