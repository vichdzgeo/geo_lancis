import processing as pr 
def union_a_b (path_a,path_b,path_sig):
    path_salida = path_sig +"union_a_b.shp"
    dicc = {'INPUT':path_a,
    'OVERLAY':path_b,
    'OVERLAY_FIELDS_PREFIX':'',
    'OUTPUT':path_salida}
    pr.run("native:union", dicc)
    return calcula_area(path_salida)

def interseccion_a_b(path_a,path_b,path_sig):
    path_salida = path_sig +"interseccion_a_b.shp"
    dicc = {'INPUT':path_a,
    'OVERLAY':path_b,
  ' INPUT_FIELDS':[],
    'OVERLAY_FIELDS':[],
    'OVERLAY_FIELDS_PREFIX':'',
    'OUTPUT':path_salida}      
    pr.run("native:intersection",dicc)
    return calcula_area(path_salida)

def calcula_area(path_a, valor=10000):
    layer = QgsVectorLayer(path_a,"","ogr")
    area_ha = [x.geometry().area()/valor for x in layer.getFeatures()]
    ha = round(sum(area_ha),2)
    return ha
    
def compara_a_b(path_a,path_b,path_sig ):
    area_a = calcula_area(path_a)
    area_b = calcula_area(path_b)
    interseccion = interseccion_a_b(path_a,path_b,path_sig)
    union =  union_a_b(path_a,path_b,path_sig)
    diff_a = round(union - area_b,2)
    diff_b = round(union - area_a,2)
    #remove_raster(path_sig+"interseccion_a_b.shp")
    #remove_raster(path_sig+"union_a_b.shp")
    print ("area_a, area_b, intersección, diff_a, diff_b")
    print (area_a,area_b,interseccion,diff_a,diff_b)

area_a = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_anps/procesamiento/anps2_biocultural_del_puuc.shp"
area_b  = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_anps/procesamiento/anp_est_mun_priv_reserva_biocultural_helen_moyers_(kaxil_kiuik).shp"

path_sig = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_anps/procesamiento/"

compara_a_b(area_a,area_b,path_sig )

