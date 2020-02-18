import pandas as pd 


def owa(df,a,w,alpha=1):
    wj=[]
    for index, row in df.iterrows():
        wj.append(row[w])
    
    print(wj)
    rango_i =sorted(wj) #los pesos ordenados de menor a mayor 
    print(rango_i)
    rango_dicc ={} # diccionario de pesos 
    total = len(rango_i) #total de elementos en la lista de rango_i
    rango=[] #lista donde se almacena el orden segun su importancia  donde 1 es más importante y n el menos importante 
    for r in rango_i:
        rango_dicc[total]=r
        total-=1
    total = len(rango_i)
    for wr in wj:   
        for i in range(1,total+1):
            if rango_dicc[i]==wr:
                rango.append(i)
                #print (i)
    print(rango)
    ### Cálculo de OWA 
    df_o = df.sort_values(a,ascending=False).copy()
    #print(df_o)
    u= [] #lista de pesos ordenados
    z= [] #lista de valores ordenados 
    uk=[] #suma de wk^alpha    
    uk1=[] #suma de wk-1^alpha
    
    for index, row in df_o.iterrows():
        u.append(row[w])
        z.append(row[a])

    for i in range(len(u)):
        sumauk = 0
        sumauk1= 0 
        if i==0:
            sumauk=u[0]
            sumauk1=0
            uk.append(pow(sumauk,alpha))
            uk1.append(pow(sumauk1,alpha))
        if not i==0:    
            for j in range(1,i+2):
                sumauk +=u[j-1]
            uk.append(pow(sumauk,alpha))
            for k in range(i):
                sumauk1+=u[k]
            uk1.append(pow(sumauk1,alpha))
        #print (i,suma)

    pre_owa = [] #peso de orden * valor ordenado 
    vj=[] # peso de orden
    for i in range(len(u)):
        vj.append((uk[i]-uk1[i])) #peso de orden 
        pre_owa.append(round((uk[i]-uk1[i])*z[i],3))
    v_owa =sum(pre_owa)
    
    ## Calculo de Orness
    v_orness=[]
    print(rango)
    #vj=[1,0,0,0,0]
    vj=[0,0,1,0,0]
    for a,b in zip(rango,vj):
        print (a,b)
        o = ((len(rango)- a) / (len(rango)-1))*b
        v_orness.append(o)
    
    orness = sum(v_orness)
    
    ## Cálculo de tradeoff
    v_tradeoff=[]
   
    for a in vj:
        #print('lk:',a)
        t = pow((b - ( 1 / len(rango) )) , 2) / (len(rango)-1)
        #print (t)
        v_tradeoff.append(t)
    tradeoff = (1 - pow(len(rango) * sum(v_tradeoff),0.5))
    #print(sum(v_tradeoff))
    
    return v_owa,tradeoff,orness

#df = pd.DataFrame({'j':[1,2,3,4,5],
#                    'a':[0.1,0,0.6,0.8,0.3],
#                    'w':[0.07,0.27,0.33,0.13,0.20]},
#                    columns=['j','a','w'])                      
df = pd.DataFrame({'j':[1,2,3,4],
                    'a':[0.6,0.3,0.2,0.9],
                    'w':[0.1,0.5,0.3,0.1]},
                    columns=['j','a','w']) 
#
valor_owa = owa(df,'a','w',alpha=0.0001)
print (valor_owa)

## calcular el orden 
#wj=[]
#for index, row in df.iterrows():
#    wj.append(row['w'])
#    
#rango_i =sorted(wj) #los pesos ordenados de menor a mayor 
#rango_dicc ={} # diccionario de pesos 
#total = len(rango_i) #total de elementos en la lista de rango_i
#rango=[] #lista donde se almacena el orden segun su importancia  donde 1 es más importante y n el menos importante 
#for r in rango_i:
#    rango_dicc[total]=r
#    total-=1
#total = len(rango_i)
#for w in wj:
#    for i in range(1,total+1):
#        if rango_dicc[i]==w:
#            rango.append(i)
#            print (i)