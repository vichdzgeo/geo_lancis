
categorias = 5
campo_cat_referencia = 'cat_equi'
campo_cat_clasificacion = 'cat_fp20'

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
         if pol[campo_cat_referencia] == b+1 and pol[campo_cat_clasificacion]==c+1:  
            matrix[b+1][c]+=1
        

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