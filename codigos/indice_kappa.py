
categorias = 5

matrix = {}

for i in range(categorias):
    matrix[i+1]=[0]*categorias


layer = iface.activeLayer()
request =  QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
#for a in range(categorias):
#    for pol in layer.getFeatures(request):
#        ## diagonal principal 
#        if pol['cat_y_40'] == a+1 and pol['cat_mean']==a+1:
#            matrix[a+1][a]+=1

for b in range(categorias):
    for pol in layer.getFeatures(request):
        for c in range(categorias):
         if pol['cat_equi'] == b+1 and pol['cat_fp20']==c+1:
            matrix[b+1][c]+=1
        
print ("fin")



        
diagonal_principal =[]
for i in range(categorias):
    diagonal_principal.append(matrix[i+1][i])

total=0.0

for k,v in matrix.items():
    for valor in v:
        total+=float(valor)

aciertos = sum(diagonal_principal)
omision =0
for j in range(categorias):
    suma_renglon=[]
    suma_columna=[]
    for i in range(categorias):
        suma_columna.append(matrix[i+1][j])
        suma_renglon.append(matrix[j+1][i])
    omision+=((sum(suma_renglon)*sum(suma_columna))/total)

k = round((aciertos - omision)/(total -omision),3)
print (k)