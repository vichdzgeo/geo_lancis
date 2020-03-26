def grado_coincidencia(path_layer_a,path_layer_b,campo):
    categorias = 5
    matrix = {}

    for i in range(categorias):
        matrix[i+1]=[0]*categorias

    layer_a = QgsVectorLayer(path_layer_a,"","ogr")
    layer_b = QgsVectorLayer(path_layer_b,"","ogr")

    request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)

    for r1 in range(categorias):
        for a,b in zip(layer_a.getFeatures(request),layer_b.getFeatures(request)):
            for r2 in range(categorias):
            if a[campo] == r1+1 and b[campo]==r2+1:
                matrix[r1+1][r2]+=1
            
    diagonal_principal =[]
    for i in range(categorias):
        diagonal_principal.append(matrix[i+1][i])

    total=0.0

    for k,v in matrix.items():
        for valor in v:
            total+=float(valor)

    aciertos = sum(diagonal_principal)


    grado = round((aciertos)/(total -aciertos),3)
    return grado
