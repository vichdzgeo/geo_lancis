import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import gdal_array

def matrix_base(path_r):
    no_capa=1
    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimesion = band1.shape
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band1 = np.ma.masked_equal(band1, nodata_r)
    ind = [x for x in range(dimesion[0])]
    col = [x for x in range(dimesion[1])]

    df_r = pd.DataFrame(band1,index=ind,columns=col)
    dr_r_long = df_r.unstack().reset_index()
    dim_long = len(dr_r_long)
    dr_r_long['id']=[x for x in range(dim_long)]
    dr_r_long.rename(columns={0:'r'+str(no_capa)}, inplace=True)
    dr_r_long.rename(columns={'level_0':'col_r'+str(no_capa)}, inplace=True)
    dr_r_long.rename(columns={'level_1':'ren_r'+str(no_capa)}, inplace=True)
    base=dr_r_long.filter(['id','ren_r'+str(no_capa),'col_r'+str(no_capa)])
    return base

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


def raster_to_df(path_r,no_capa=1):

    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimesion = band1.shape
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band1 = np.ma.masked_equal(band1, nodata_r)
    ind = [x for x in range(dimesion[0])]
    col = [x for x in range(dimesion[1])]

    df_r = pd.DataFrame(band1,index=ind,columns=col)
    dr_r_long = df_r.unstack().reset_index()
    dim_long = len(dr_r_long)
    dr_r_long['id']=[x for x in range(dim_long)]
    dr_r_long.rename(columns={0:'r'+str(no_capa)}, inplace=True)
    dr_r_long.rename(columns={'level_0':'col_r'+str(no_capa)}, inplace=True)
    dr_r_long.rename(columns={'level_1':'ren_r'+str(no_capa)}, inplace=True)
    dr_r_long=dr_r_long[dr_r_long['r'+str(no_capa)] <= 1]
    return dr_r_long

def insumo_owa(capas,pesos):
    
    no_capas=len(pesos)
    columnas_matrix =['id','col_r1','ren_r1']
    for no in range(1,no_capas+1):
        columnas_matrix.append('r'+str(no))
        
    matrix_join = reduce(juntar,capas)
    matrix_v = matrix_join.filter(columnas_matrix)
    
    if no_capas==2:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2']],axis = 1)
    elif no_capas==3:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3']],axis = 1)
    elif no_capas==4:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4']],axis = 1)
    elif no_capas==5:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5']],axis = 1)
    elif no_capas==6:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6']],axis = 1)
    elif no_capas==7:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7']],axis = 1)
    elif no_capas==8:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8']],axis = 1)
    elif no_capas==9:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9']],axis = 1)
    
    
    m2=matrix_v.filter(['id','v'])
    return m2


def calculo_owa(df,pesos,owa=0.5):
    campo_owa = 'owa_'+str(owa).replace(".","")
    df[campo_owa] = df.apply(lambda x: owa_df(x['v'],w,owa),axis=1)

    df_owa=df.filter(['id',campo_owa])
    
    return campo_owa,df_owa
    
    


path_r = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/biologica/v_acuatica_yuc/fv_v_acuatica_yuc.tif"
path_r2 ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/biologica/v_costera_yuc/fv_v_costera_distancia_yuc.tif"
path_r3 ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/fisica/ancho_playa_yuc/fv_distancia_playa_yuc.tif"
path_r4 ="C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/fisica/elev_yuc/fv_elevacion_yuc.tif"
print (time.strftime("%H:%M:%S"))

### datos para formar al último la capa
raster = gdal.Open(path_r)
band1 =raster.GetRasterBand(1).ReadAsArray()
dimension = band1.shape
#proyeccion = raster.GetProjection()
geotransform = raster.GetGeoTransform()


capa_1,capa_2,capa_3,capa_4 = raster_to_df(path_r,1),raster_to_df(path_r2,2),raster_to_df(path_r3,3),raster_to_df(path_r4,4)
capas=[capa_1,capa_2,capa_3,capa_4]
w=[0.08,0.42,0.065,0.435]


def genera_owa(capas,pesos,path_r,ruta_salida):
    ## datos de capa master 
    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimension = band1.shape
    geotransform = raster.GetGeoTransform()


    m_base = matrix_base(path_r)
    matrix = insumo_owa(capas,w)
    owa_values = [0.0001,0.1,0.5,1.0,2.0,10.0,1000.0]

    for owa_val in owa_values:
        campo, matrix_owa =calculo_owa(matrix,w,owa_val)
        df_matrix_owa = pd.merge(m_base, matrix_owa, on='id', how='outer')
        arreglo = dr_r_wide.to_numpy()



#### - OWA PARA 0.0001 --- ###

campo_0001,owa_0001 =calculo_owa(matrix,w,0.0001)
df_owa0001 = pd.merge(m_base, owa_0001, on='id', how='outer')
dr_r_owa0001 = df_owa0001.pivot(index='ren_r1',columns='col_r1',values=campo_0001)
arra0001 = dr_r_wide.to_numpy()  

##### - PROCESO PARA GUARDAR LA CAPA -######

def array_to_raster(array,path_salida,dimension,zona_utm):
    dst_filename=path_salida
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)
    dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                        bands=1, eType=gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.SetUTM(zona_utm, 1)
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None

print (time.strftime("%H:%M:%S"))

'''
from osgeo import osr
dst_filename="C:/CursoDjango/owa0001.tif"
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra0001)
# Once we're done, close properly the dataset
dst_ds = None
### - TERMINA PROCESO - #######


### OWA PARA 0.1 ##

campo_01,owa_01 =calculo_owa(matrix,w,0.1)
df_owa01 = pd.merge(m_base, owa_01, on='id', how='outer')
dr_r_owa01 = df_owa01.pivot(index='ren_r1',columns='col_r1',values=campo_01)
arra01 = dr_r_owa01.to_numpy()  

##### - PROCESO PARA GUARDAR LA CAPA -######


from osgeo import osr
dst_filename="C:/CursoDjango/owa01.tif"
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra01)
# Once we're done, close properly the dataset
dst_ds = None
### - TERMINA PROCESO - #######


### OWA PARA 1 ##

campo_1,owa_1 =calculo_owa(matrix,w,1.0)
df_owa1 = pd.merge(m_base, owa_1, on='id', how='outer')
dr_r_owa1 = df_owa1.pivot(index='ren_r1',columns='col_r1',values=campo_1)
arra1 = dr_r_owa1.to_numpy()  

##### - PROCESO PARA GUARDAR LA CAPA -######


from osgeo import osr
dst_filename="C:/CursoDjango/owa1.tif"
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra1)
# Once we're done, close properly the dataset
dst_ds = None
### - TERMINA PROCESO - #######




### OWA PARA 2 ##

campo_2,owa_2 =calculo_owa(matrix,w,2.0)
df_owa2 = pd.merge(m_base, owa_2, on='id', how='outer')
dr_r_owa2 = df_owa2.pivot(index='ren_r1',columns='col_r1',values=campo_2)
arra2 = dr_r_owa2.to_numpy()  

##### - PROCESO PARA GUARDAR LA CAPA -######


from osgeo import osr
dst_filename="C:/CursoDjango/owa2.tif"
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra2)
# Once we're done, close properly the dataset
dst_ds = None
### - TERMINA PROCESO - #######



### OWA PARA 10 ##

campo_10,owa_10 =calculo_owa(matrix,w,10.0)
df_owa10 = pd.merge(m_base, owa_10, on='id', how='outer')
dr_r_owa10 = df_owa10.pivot(index='ren_r1',columns='col_r1',values=campo_10)
arra10 = dr_r_owa10.to_numpy()  

##### - PROCESO PARA GUARDAR LA CAPA -######


from osgeo import osr
dst_filename="C:/CursoDjango/owa10.tif"
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra10)
# Once we're done, close properly the dataset
dst_ds = None
### - TERMINA PROCESO - #######


### OWA PARA 1000 ##

campo_1000,owa_1000 =calculo_owa(matrix,w,1000.0)
df_owa1000 = pd.merge(m_base, owa_1000, on='id', how='outer')
dr_r_owa1000 = df_owa1000.pivot(index='ren_r1',columns='col_r1',values=campo_1000)
arra1000 = dr_r_owa1000.to_numpy()  

##### - PROCESO PARA GUARDAR LA CAPA -######


from osgeo import osr
dst_filename="C:/CursoDjango/owa1000.tif"
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                    bands=1, eType=gdal.GDT_Float32)
                    
dst_ds.SetGeoTransform(geotransform)
srs = osr.SpatialReference()
srs.SetUTM(16, 1)
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection(srs.ExportToWkt())

dst_ds.GetRasterBand(1).WriteArray(arra1000)
# Once we're done, close properly the dataset
dst_ds = None
### - TERMINA PROCESO - #######






'''
