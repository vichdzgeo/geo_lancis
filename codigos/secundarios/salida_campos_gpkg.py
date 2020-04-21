def intervalos(min=0,max=1):
    dicc_e = {}
    lista_val = [min,]
    categorias = 5
    constante = (max-min)/categorias
    rango= min
    for i in range(1,categorias+1):
        rango += constante
        lista_val.append(rango)
    
    

    return lista_val


layer = iface.activeLayer()

campos = [field.name() for field in layer.fields()]
    
request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
i = 0
for field in layer.fields():
    lista=[]
    i+=1
    if not field.typeName()=="String" or field.typeName()=="Date":
        for feature in layer.getFeatures(request):

            if  not feature[field.name()] == NULL:
                lista.append(feature[field.name()])

        print("| "+"img"+str(i)+" | "+field.name()
                      + " | "
                      + str(round(min(lista),3))
                      +" | "+ str(round(max(lista),3))+" | |")
        print("+-")

    else:
        print ("| | ",field.name()," |")
        print("+-")
#        archivo.write(field.name()
#                      + " | "
#                      + field.typeName()
#                      + " | "
#                      + " | "
#                      + " |"
#                      + "\n")