import pandas as pd 


def owa(df,a,w,alpha=1):
    ## calculo del rango 
    wj=[]
    for index, row in df.iterrows():
        wj.append(row[w])
    
    rango_i =sorted(wj) #los pesos ordenados de menor a mayor 
    #print(rango_i)
    rango_dicc ={} # diccionario de pesos 
    total = len(rango_i) #total de elementos en la lista de rango_i
    rango=[] #lista donde se almacena el orden segun su importancia  donde 1 es más importante y n el menos importante 
    for r in rango_i:
        rango_dicc[total]=r
        total-=1
  
    for c in wj:
        condicion =0
        for k,v in rango_dicc.items():
            
            if not condicion==1 and k not in rango:
                if c==v:
                    condicion+=1
                    #print (c,k)
                    rango.append(k)
    
#    print (rango)
    ### Cálculo de OWA 
    df_o = df.sort_values(a,ascending=False).copy()
    u= [] #lista de pesos ordenados
    z= [] #lista de valores ordenados 
    uk=[] #suma de wk^alpha    
    uk1=[] #suma de wk-1^alpha
    
    for index, row in df_o.iterrows():
        u.append(row[w])
        z.append(row[a])
#    print("pesos ordenados")
#    print (u)
#    print("valores ordenados")
#    print(z)
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


    pre_owa = [] #peso de orden * valor ordenado 
    vj=[] # peso de orden
    for i in range(len(u)):
        vj.append((uk[i]-uk1[i])) #peso de orden 
        pre_owa.append(round((uk[i]-uk1[i])*z[i],3))
    v_owa =round(sum(pre_owa),3)

    #### Temporal para seleccion de escenarios 
    
    minimo = min(rango)
    maximo = max(rango)
    
    if alpha < 0.0002:
        vj=[]
        for no in rango:
            if no==minimo:
                vj.append(1)
            else:
                vj.append(0)

    if alpha > 25:
        vj=[]
        for no in rango:
            if no==maximo:
                vj.append(1)
            else:
                vj.append(0)

    if alpha == 1:
        vj=[]
        for no in rango:
           vj.append(1/len(rango))
           
        
    
    
    
    ## Calculo de Orness
    
    
    
    v_orness=[]


    for a,b in zip(rango,vj):
        #print (a,b)
        o = ((len(rango)- a) / (len(rango)-1))*b
        v_orness.append(o)
    orness = round(sum(v_orness),3)
    
    ## Cálculo de tradeoff
    v_tradeoff=[]
   
    for a in vj:
        t = pow((a - ( 1 / len(rango) )) , 2) / (len(rango)-1)
        v_tradeoff.append(t)
        
    tradeoff = round((1 - pow(len(rango) * sum(v_tradeoff),0.5)),3)

    
    return v_owa#,orness, tradeoff

df = pd.DataFrame({'j':[1,2,3,4,5],
                    'a':[0.1,0.0,0.6,0.8,0.3],
                    'w':[0.07,0.27,0.33,0.13,0.20]},
                    columns=['j','a','w'])                      
#df = pd.DataFrame({'j':[1,2,3,4],
#                    'a':[0.6,0.3,0.2,0.9],
#                    'w':[0.1,0.5,0.3,0.1]},
#                    columns=['j','a','w']) 
#
#w=[0.08,0.42,0.065,0.435]
#a= [0.016439,0.989936,0.000396,1.0]
#df = pd.DataFrame({'j':[1,2,3,4],
#                    'a':a,
#                    'w':w},
#                    columns=['j','a','w'])    




valor_owa = owa(df,'a','w',alpha=1000)
print (valor_owa)
