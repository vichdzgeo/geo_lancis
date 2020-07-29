
import pandas as pd 
import processing as pr 
capas  = pd.read_csv(r"C:\Dropbox (LANCIS)\SIG\desarrollo\sig_fomix\procesamiento\verificacion_capas.csv",names=['nombre','nulos','codificacion','proyeccion','url'])

capas_utm = capas[capas['proyeccion']=="EPSG:32616"]
lista = []
for index, row in capas_utm.iterrows():
    lista.append(row['url'])
    
capas_l =list(set(lista))

mascara ='C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/mascara_municipios_2018/area_municipios_2018_yuc.shp'


for l in  capas_l:
    print (l.split("/")[-1:])
    path_salida = l.split(".")[0]+"_clip.shp"
    dicc = { 'S_INPUT' : l,
        'S_OUTPUT' : path_salida,
        'CLIP' : mascara}

    pr.run("saga:polygonclipping",dicc)