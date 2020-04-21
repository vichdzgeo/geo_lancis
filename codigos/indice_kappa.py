import csv 

def indice_kappa(path_db,categorias,campo_cat_referencia,campo_cat_clasificacion):
    '''
    :param path_vector: Ruta del archivo puede ser un shapefile o un csv
    :type path_vector: srt

    :param categorias: Número de categorias 
    :type categorias: int

    :param campo_cat_referencia: Nombre del campo de categorias de referencia (estas serán las columnas en la matriz de error)
    :type campo_cat_referencia: str

    :param campo_cat_clasificacion: Nombre del campo de categorias del mapa clasificado (estos seran los renglones en la matriz de error)
    :type campo_cat_clasificacion:int 

    '''

    matrix = {}
    validacion =''
    for i in range(categorias):
        matrix[i+1]=[0]*categorias

    if path_db.split(".")[1]=="shp":
        layer = QgsVectorLayer(path_db,"","ogr")
        request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
    
        for b in range(categorias):
            for pol in layer.getFeatures(request):
                for c in range(categorias):
                    if pol[campo_cat_clasificacion] == b+1 and pol[campo_cat_referencia]==c+1:  
                        matrix[b+1][c]+=1
    elif path_db.split(".")[1]=="csv":
        uri = "file:///"+path_db+'?d?delimiter=","'
        layer = QgsVectorLayer(uri,"","delimitedtext")
        for b in range(categorias):
            for pol in layer.getFeatures():
                for c in range(categorias):
                    if pol[campo_cat_clasificacion] == b+1 and pol[campo_cat_referencia]==c+1:  
                        matrix[b+1][c]+=1
    else:
        validacion = "formato no valido"
        print ("formato no valido")
            
    if not validacion == "formato no valido":

        #Suma de la diagonal principal 
        diagonal_principal =[]
        for i in range(categorias):
            diagonal_principal.append(matrix[i+1][i])

        total=0.0

        for k,v in matrix.items():
            for valor in v:
                total+=float(valor)

        acuerdos = sum(diagonal_principal) 
        columnas_renglones =0
        for j in range(categorias):
            suma_renglon=[]
            suma_columna=[]
            for i in range(categorias):
                suma_columna.append(matrix[i+1][j])
                suma_renglon.append(matrix[j+1][i])
            columnas_renglones+=((sum(suma_renglon)*sum(suma_columna))/total)

        k = round((acuerdos - columnas_renglones)/(total -columnas_renglones),3)
        print ("el valor de kappa es: ",k)
        

        ### genera la salida de la matriz de error en un archivo csv con el mismo nombre que la capa 
        path_csv = path_db.split(".")[0]+"_matrix_error_"+campo_cat_referencia+"_vs_"+campo_cat_clasificacion+".csv"
        matrix_csv = open(path_csv,"w")
        encabezado = ["clas/ref"]
        for k1,v1, in matrix.items():
            encabezado.append(("clase_"+str(k1)))
        matrix_csv.write(",".join(encabezado)+"\n")
       
        for k1,v1, in matrix.items():
            renglon = []
            renglon.append("clase_"+str(k1))
            for v2 in v1:
                renglon.append(str(v2))
            matrix_csv.write(",".join(renglon)+"\n")
            
        matrix_csv.close()
        print ("escribiendo matriz...")
        print ("el proceso ha finalizado")
        print ("ruta",path_csv)
        return k

path_db  = "C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/kappa/insumos/datos_prueba.csv" 
indice_kappa(path_db,5,'cat_vul','ex_cat_vul')