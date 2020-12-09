layer = iface.activeLayer()

def categorias_campo_csv(layer,campo):
    nombre_capa = layer.source().split("/")[-1].split(".")[0]
    path_categorias = "/".join(layer.source().split("/")[:-1])+"/categorias_"+campo+"_"+nombre_capa+".csv"
    archivo = open(path_categorias,'w')
    consulta = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
    lista = list(set([x[campo] for x in layer.getFeatures(consulta)]))
    lista.sort()
    print (lista)
    archivo.write("id,categoria\n")
    for i in range(len(lista)):
        archivo.write(str(i+1)+","+lista[i].replace(",",';')+"\n")
    archivo.close()
    print ('archivo csv de categorias creado...')
    print ('ruta: ',path_categorias)

def campos_csv(layer):
    lista_campos = [field.name() for field in layer.fields()]
    nombre_capa = layer.source().split("/")[-1].split(".")[0]
    path_categorias = "/".join(layer.source().split("/")[:-1])+"/campos_"+nombre_capa+".csv"
    archivo = open(path_categorias,'w')
    archivo.write("no,campo,descripcion\n")
    for i in range(len(lista_campos)):
        archivo.write(str(i+1)+","+lista_campos[i]+"\n")
    archivo.close()
    print ('archivo csv de campos creado...')
    print ('ruta: ',path_categorias)

categorias_campo_csv(layer,'DES_SAMOF')
campos_csv(layer)