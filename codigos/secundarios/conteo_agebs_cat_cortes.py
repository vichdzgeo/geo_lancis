import os

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
                lista.append(extension)
    return lista
    
path = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/equidistante/"
archivo = open(path+"agebs_no_cambian.csv","w")
archivo.write("escenario,cat_1,cat_2,cat_3,cat_4,cat_5\n")

archivocount = open(path+"agebs_no_cambian_count.csv","w")
archivocount.write("escenario,cat_1,cat_2,cat_3,cat_4,cat_5\n")

lista_nombres = lista_shp(path)

                

for nombre in lista_nombres:
#    print (nombre[0])
    path_equi = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/equidistante/" + nombre[0]+".shp"
    path_fp15 = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/fp15/" + nombre[0]+".shp"
    path_fp20 = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/indice_leesallee/shapes/fp20/" + nombre[0]+".shp"
    
    equidistante = QgsVectorLayer(path_equi,"","ogr")
    fp15 = path_fp15 = QgsVectorLayer(path_fp15,"","ogr")
    fp20 =path_fp20 = QgsVectorLayer(path_fp20,"","ogr")

    lista_1 = []
    lista_2 = []
    lista_3 = []
    lista_4 = []
    lista_5 = []

    for a,b,c in zip(equidistante.getFeatures(),fp15.getFeatures(),fp20.getFeatures()):
    

        if a['cat_vul']==b['cat_vul'] and  a['cat_vul']==c['cat_vul']:
           if a['cat_vul'] ==1:
               lista_1.append(a['ageb_id'])
           if a['cat_vul'] ==2:
               lista_2.append(a['ageb_id'])
           if a['cat_vul'] ==3:
               lista_3.append(a['ageb_id'])
           if a['cat_vul'] ==4:
               lista_4.append(a['ageb_id'])
           if a['cat_vul'] ==5:
               lista_5.append(a['ageb_id'])

    
    archivo.write(nombre[0]+","+"|".join(lista_1)+","+
                                "|".join(lista_2)+","+
                                "|".join(lista_3)+","+
                                "|".join(lista_4)+","+
                                "|".join(lista_5)+","+"\n")
                                
    archivocount.write(nombre[0]+","+str(len(lista_1))+","+
                            str(len(lista_2))+","+
                            str(len(lista_3))+","+
                            str(len(lista_4))+","+
                            str(len(lista_5))+","+"\n")
                                
archivo.close()
archivocount.close()
print ("fin")
    