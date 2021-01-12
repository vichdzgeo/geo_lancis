import numpy as np 
def wf(fp=2,min=0,max=1,categorias=5):
    
    dicc_e = {}
    lista_val = [min,]
    pm = max - min 
    cats = np.power(fp, categorias)
    e0 = pm/cats
    for i in range(1 , categorias + 1):
        dicc_e['e'+str(i)]= min + (np.power(fp,i) * e0)
        

    dicc_cortes ={}
    for i in range(1 , categorias + 1):
        lista_val.append( dicc_e['e'+str(i)])
    print ('cat, corte_inf,corte_sup')
    for i in range(1,len(lista_val)):
        print (i,",",lista_val[i-1],",",lista_val[i])
        
    return lista_val

min = 0
max = 1
categorias= 3
fp = 2
wf(fp,min,max,categorias)