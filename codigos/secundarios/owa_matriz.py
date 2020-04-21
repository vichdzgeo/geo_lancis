import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import gdal_array



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
    

    ### Cálculo de OWA 
    df_o = df.sort_values(a,ascending=False).copy()
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

def owa_df(v,w,alpha=1):
    no_criterios =len(w)
    j = [x for x in range(1,no_criterios+1)]
    df = pd.DataFrame({'j':j,
                    'a':v,
                    'w':w},
                    columns=['j','a','w']) 
    
    valor = owa(df,'a','w',alpha)
    return valor



def juntar(left, right):
  return pd.merge(left, right, on='id', how='outer')



print (time.strftime("%H:%M:%S"))
path_r = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/biologica/v_acuatica_yuc/fv_v_acuatica_yuc.tif"
path_r2 ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/biologica/v_costera_yuc/fv_v_costera_distancia_yuc.tif"
path_r3 ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/fisica/ancho_playa_yuc/fv_distancia_playa_yuc.tif"
path_r4 ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/fisica/elev_yuc/fv_elevacion_yuc.tif"


rasterArray_r = gdal_array.LoadFile(path_r)
rasterArray_r2 = gdal_array.LoadFile(path_r2)
rasterArray_r3 = gdal_array.LoadFile(path_r3)
rasterArray_r4 = gdal_array.LoadFile(path_r4)



nodata_r =rasterArray_r.min()

nodata_r2 =rasterArray_r2.max()
nodata_r3 =rasterArray_r3.min()
nodata_r4 =rasterArray_r4.min()
#nodata = band.GetNoDataValue()

rasterArray_r = np.ma.masked_equal(rasterArray_r, nodata_r)


rasterArray_r2 = np.ma.masked_equal(rasterArray_r2, nodata_r2)
rasterArray_r3 = np.ma.masked_equal(rasterArray_r3, nodata_r3)
rasterArray_r4 = np.ma.masked_equal(rasterArray_r4, nodata_r4)


ind = ['r'+str(x) for x in range(3500)]
col = ['c'+str(x) for x in range(10474)]

df_r = pd.DataFrame(rasterArray_r,index=ind,columns=col)
df_r2 = pd.DataFrame(rasterArray_r2,index=ind,columns=col)
df_r3 = pd.DataFrame(rasterArray_r3,index=ind,columns=col)
df_r4 = pd.DataFrame(rasterArray_r4,index=ind,columns=col)

lista_id = [x for x in range(36659000)]

print ("renombre completo")
dr_r_long = df_r.unstack().reset_index()
dr_r_long['id']=[x for x in range(36659000)]
dr_r_long.rename(columns={0:'r1'}, inplace=True)
dr_r_long.rename(columns={'level_0':'col_r1'}, inplace=True)
dr_r_long.rename(columns={'level_1':'ren_r1'}, inplace=True)
dr_r_long=dr_r_long[dr_r_long['r1'] <= 1]


dr_r2_long = df_r2.unstack().reset_index()
dr_r2_long['id']=[x for x in range(36659000)]
dr_r2_long.rename(columns={0:'r2'}, inplace=True)
dr_r2_long.rename(columns={'level_0':'col_r2'}, inplace=True)
dr_r2_long.rename(columns={'level_1':'ren_r2'}, inplace=True)
dr_r2_long=dr_r2_long[dr_r2_long['r2'] <= 1]

dr_r3_long = df_r3.unstack().reset_index()
dr_r3_long['id']=[x for x in range(36659000)]
dr_r3_long.rename(columns={0:'r3'}, inplace=True)
dr_r3_long.rename(columns={'level_0':'col_r3'}, inplace=True)
dr_r3_long.rename(columns={'level_1':'ren_r3'}, inplace=True)
dr_r3_long=dr_r3_long[dr_r3_long['r3'] <= 1]

dr_r4_long = df_r4.unstack().reset_index()
dr_r4_long['id']=[x for x in range(36659000)]
dr_r4_long.rename(columns={0:'r4'}, inplace=True)
dr_r_long.rename(columns={'level_0':'col_r4'}, inplace=True)
dr_r_long.rename(columns={'level_1':'ren_r4'}, inplace=True)
dr_r4_long=dr_r4_long[dr_r4_long['r4'] <= 1]


mu = reduce(juntar,[dr_r_long,dr_r2_long,dr_r3_long,dr_r4_long]) #.set_index("id").sort_index()

print (time.strftime("%H:%M:%S"))
'''
#
mu1 = mu.filter(['id','col_r1','ren_r1','r1','r2','r3','r4'])


mu1['v']=mu1.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4']],axis = 1)
w=[0.08,0.42,0.065,0.435]
m2=mu1.filter(['id','v'])

m2['owa_05'] = m2.apply(lambda x: victor(x['v'],w,0.5),axis=1)
m2_owa05=m2.filter(['id','owa_05'])
raster_05=df_r.unstack().reset_index()
raster_05['id']=[x for x in range(36659000)]
raster_05=raster_05.filter(['id','level_0','level_1'])
owa05_long=pd.merge(raster_05,m2_owa05,on='id',how='outer')
owa05=owa05_long.pivot(index='level_1',columns='level_0')['owa_05']

print (time.strftime("%H:%M:%S"))
print(owa05)
'''