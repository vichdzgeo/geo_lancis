import pandas as pd 
def owa(df,a,w,alpha=1): #8  de 9
    '''
    Esta función calcula OWA dado un dataframe y un valor de alpha

    :param df: Data frame que contiene una columna de valores (a) y otra de pesos (w)
    :type df: Pandas data frame
    :param a: Nombre de la columna de los valores
    :type a: str
    :param w: Nombre de la columna de los pesos
    :type w: str
    :param alpha: Valor de alpha
    :type alpha: float

    :returns: valor de owa
    :rtype: float
    '''

    ### Cálculo de OWA 
    df_o = df.sort_values(a,ascending=False).copy() #ordena los elmentos por columna de valores
    print ("2) Matriz ordenada de mayor a menor por el orden de sus valores (Orden por valor)")
    print (df_o)
    u= [] #lista de pesos ordenados
    z= [] #lista de valores ordenados 
    uk=[] #suma de wk^alpha    
    uk1=[] #suma de wk-1^alpha
    
    for index, row in df_o.iterrows():    #del df ordenado se pasan los valores y pesos ordenados a listas
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
    #df_o['uk']=uk1


    pre_owa = [] #peso de orden * valor ordenado 
    vj=[] # peso de orden
    for i in range(len(u)):
        vj.append((uk[i]-uk1[i])) #peso de orden 
        pre_owa.append(round((uk[i]-uk1[i])*z[i],3))
    df_o['vj']=vj
    df_o['vj*a']=pre_owa
    v_owa =round(sum(pre_owa),3)
    print ("3) Matriz con todos los cálculos")
    print (df_o.round(3))
    print ('Valor de owa:', v_owa)
    
    return v_owa

def owa_df(v,w,alpha=1): #7 de 9
    '''
    Esta función recibe una lista de valores, pesos y valor de alfa, los agrega 
    a un dataframe que es ingresado a la función owa para calcular el valor
    :param v: lista de valores 
    :type v: list
    :param w: lista de pesos
    :type w: list 
    :param alpha: valor de alpha 
    :type alpha: float

    :return: valor de OWA
    :rtype: float
    '''
    no_criterios =len(w)
    j = [x for x in range(1,no_criterios+1)]
    df = pd.DataFrame({'j':j,
                    'a':v,
                    'w':w},
                    columns=['j','a','w']) 
    print("1) matriz de valores y pesos como se ingresan originalmente (Sin orden)")
    print (df)
    valor = owa(df,'a','w',alpha)
    return valor,df
#v = [0.8,0.3,0.1,1.0,0.5]
#w = [0.125,0.5,0.0625,0.0625,0.25]
v = [0.1,0.0,0.6,0.8,0.3]
w = [0.07,0.27,0.33,0.13,0.20]

valor,df = owa_df(v,w,alpha=0.85)
print (valor)