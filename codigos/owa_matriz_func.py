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


def raster_to_df(path_r):

    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimesion = band1.shape
    nodata_r = band1.min()
    band1 = np.ma.masked_equal(band1, nodata_r)
    ind = ['r'+str(x) for x in range(dimesion[0])]
    col = ['c'+str(x) for x in range(dimesion[1])]

    df_r = pd.DataFrame(band1,index=ind,columns=col)
    print(df_r)




path_r = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/biologica/v_acuatica_yuc/fv_v_acuatica_yuc.tif"

#raster_to_matrix(path_r)
raster = gdal.Open(path_r)
proyeccion = raster.GetProjection()
geotransform = raster.GetGeoTransform()
origenxy=(geotransform[0], geotransform[3])
pixel = (geotransform[1], geotransform[5])

band1 =raster.GetRasterBand(1).ReadAsArray()
dimension = band1.shape
nodata_r = band1.min()
band1 = np.ma.masked_equal(band1, nodata_r)
ind = [x for x in range(dimesion[0])]
col = [x for x in range(dimesion[1])]



df_r = pd.DataFrame(band1,index=ind,columns=col)

# print(df_r)
dr_r_long = df_r.unstack().reset_index()
dim_long = len(dr_r_long)
dr_r_long['id']=[x for x in range(dim_long)]
dr_r_long.rename(columns={0:'r1'}, inplace=True)
dr_r_long.rename(columns={'level_0':'col_r1'}, inplace=True)
dr_r_long.rename(columns={'level_1':'ren_r1'}, inplace=True)

## Esto es para voltear la capa
dr_r_wide = dr_r_long.pivot(index='ren_r1',columns='col_r1',values='r1')

arra = dr_r_wide.to_numpy()
## Esto es para escribir la capa 

from osgeo import osr
dst_filename="C:/CursoDjango/export.tif"


fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra)
# Once we're done, close properly the dataset
dst_ds = None