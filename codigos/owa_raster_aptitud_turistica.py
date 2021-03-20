import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import osr


def csv_to_dicc_owa(path_csv):
    datos = pd.read_csv(path_datos).round(3)
    criterios,rutas,pesos = list(datos['nombre']),list(datos['ruta']),list(datos['w'])
    dicc ={}
    total_capas = len(criterios)
    n_capa =1
    for a,b,c in zip(criterios,rutas,pesos):
        dicc['capa_'+str(n_capa)]={'ruta':b,'w':c}
        c_capa+=1
    return dicc

def insumos_base(dicc): # 1 de 9
    '''
    Esta función recibe un diccionario y regresa una
    lista de data frames y una lista de pesos 

    :param dicc: Diccionario con la estructura solicitada
    :type dicc: dict

    :returns: un lista de dataframes (capas) y una lista de pesos (w)
    :rtype: list
    '''

    capas= []
    w = []
    no_capas =[]
    
    for k,v in dicc.items():
        no_capas.append(k)

    for i in range(1,len(no_capas)+1):
        for k,v in dicc.items():
            if k == 'capa_'+str(i):
                for k2,v2 in v.items():
                    if k2 == 'ruta':
                        capas.append(raster_to_df(v2,i))
                    if k2 == 'w':
                        w.append(v2)
    return capas,w
#--------------------------------------------------#
def matrix_base(path_r): # 2 de 9
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
#-----------------------------------------------------------------#
def raster_to_df(path_r,no_capa=1):# 3 de 9
    '''
    Esta función tranfoma una capa raster de formato tiff a
    un  pandas dataframe 
    
    :param path_r: ruta del archivo .tiff
    :type path_r: str 

    :param no_capa: numero de capa ascendiente en el diccionario
    :type no_capa: int

    :returns: pandas dataframe con un id asociado
    :rtype: pandas.core.frame.DataFrame
    '''

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
#-----------------------------------------------------------------------------#
def juntar(left, right): # 4 de 9 
    '''
    Función que junda dos dataframes a partir de la columna 'id'

    :param left: Dataframe A
    :type left: pandas dataframe

    :param right: Dataframe B
    :type right: pandas dataframe

    :returns: df unido
    :rtype: pandas dataframe
    '''

    return pd.merge(left, right, on='id', how='outer')
#-----------------------------------------------------------------------------#
def insumo_owa(capas,pesos): # 5 de 9 
    '''
    Esta función junta todas las capas en un solo dataframe
    ,la salida de esta función tiene asociado un id que conserva desde el origen
    y una columna v que contiene una lista de los valores de capa pixel. 

    :param capas: lista de dataframes
    :type capas: list

    :param pesos: lista de pesos
    :type pesos: list

    :returns: data frame que contiene los valores de los pixeles en una lista
    :rtype: pandas data frame
    '''


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
    elif no_capas==10:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10']],axis = 1)
    elif no_capas==11:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11']],axis = 1)
    elif no_capas==12:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11'],x['r12']],axis = 1)
    elif no_capas==13:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11'],x['r12'],x['r13']],axis = 1)
    elif no_capas==14:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11'],x['r12'],x['r13'],x['r14']],axis = 1)
    elif no_capas==15:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11'],x['r12'],x['r13'],x['r14'],x['r15']],axis = 1)
    elif no_capas==16:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11'],x['r12'],x['r13'],x['r14'],x['r15'],x['r16']],axis = 1)
    elif no_capas==17:
        matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2'],x['r3'],x['r4'],x['r5'],x['r6'],x['r7'],x['r8'],x['r9'],x['r10'],x['r11'],x['r12'],x['r13'],x['r14'],x['r15'],x['r16'],x['r17']],axis = 1)

    m2=matrix_v.filter(['id','v'])
    return m2
#----------------------------------------------------#
def calculo_owa(df,w,alpha=0.5): # 6 de 9
    '''
    Esta función aplica al dataframe de salida de la función 
    insumo_owa la función owa_df, dada una lista de valores,
    lista de pesos y un valor de alpha.

    :param df: dataframe de salida de la función insumo_owa
    :type df: pandas dataframe

    :param w: Lista de pesos
    :type w: list

    :param alpha: Valor de alpha
    :type alpha: float

    :returns: nombre del campo, dataframe que contiene el valor de owa para el alpha dado
    :rtype: str, pandas data frame
    '''
    campo_owa = 'owa_'+str(alpha).replace(".","")
    df[campo_owa] = df.v.apply(lambda x: owa_df(x,w,alpha))

    df_owa=df.filter(['id',campo_owa])
    
    return campo_owa,df_owa
#-----------------------------------------------------------------------#
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
    
    valor = owa(df,'a','w',alpha)
    return valor
#------------------------------------------------#
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


    pre_owa = [] #peso de orden * valor ordenado 
    vj=[] # peso de orden
    for i in range(len(u)):
        vj.append((uk[i]-uk1[i])) #peso de orden 
        pre_owa.append(round((uk[i]-uk1[i])*z[i],3))
    v_owa =round(sum(pre_owa),3)

    
    return v_owa
#----------------------------------------------------------#
def array_to_raster(array,path_salida,dimension,geotransform,EPSG): # 9 de 9:
    '''
    Esta función transforma una arreglo matricial en un archivo 
    tiff

    :param array: arreglo matricial 
    :type array: numpy array 

    :param path_salida: ruta con nombre salida del archivo tiff
    :type path_salida: str 

    :param dimension: lista con valores de numero de columnas y renglones
    :type dimension: list
    
    :param geotransform: datos de rotación, coordenadas y tamaño de pixel
    :type geotransform: gdal object

    :param EPSG: Identificador de Referencia Espacial
    :type EPSG: int
    '''
    dst_filename=path_salida
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)
    dst_ds = driver.Create(dst_filename, xsize=dimension[1], ysize=dimension[0],
                        bands=1, eType=gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(EPSG)
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(array)
    dst_ds = None


def extrae_epsg(path_r):
    ds=gdal.Open(path_r)
    prj=ds.GetProjection()
    srs=osr.SpatialReference(wkt=prj)
    if srs.IsProjected:
        epsg= int(srs.GetAttrValue('AUTHORITY',1))
    #epsg= srs.GetAttrValue('AUTHORITY',1)
    return epsg


def genera_owa(capas,w,owa_alpha,path_capa_maestra,ruta_salida): #funcion integradora
    '''
    Esta función calcula OWA, dada una lista de capas, pesos y lista de valores de
    alpha, para cada alpha dada generará una capa.

    :param capas: lista de dataframes, salida de la funcion insumos_base
    :type capas: pandas.core.frame.DataFrame

    :param w: lista de pesos, salida de la función insumos_base
    :type w: list

    :param owa_alpha: lista de valores de alpha
    :type owa_alpha: list

    :param path_capa_maestra: path de la capa en formato tiff 
    :type path_capa_maestra: str 

    :param ruta_salida: Directorio de salida de las capas 
    :type ruta_salida: str 

    
    '''
    
    ## datos de capa master 
    EPSG=extrae_epsg(path_capa_maestra)
    raster = gdal.Open(path_capa_maestra)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimension = band1.shape
    geotransform = raster.GetGeoTransform()
    m_base = matrix_base(path_capa_maestra)
    matrix = insumo_owa(capas,w)
    
    for alpha in owa_alpha:
        print ("procesando alpha ",alpha, time.strftime("%H:%M:%S"))
        campo, matrix_owa =calculo_owa(matrix,w,alpha)
        df_matrix_owa = pd.merge(m_base, matrix_owa, on='id', how='outer')
        df_matrix_array = df_matrix_owa.pivot(index='ren_r1',columns='col_r1',values=campo)

        arreglo = df_matrix_array.to_numpy()
        print(campo)
        array_to_raster(arreglo,ruta_salida + campo + ".tif",dimension,geotransform,EPSG)




path_insumos = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/aptitud_turistica__costera_yuc/"
print (time.strftime("%H:%M:%S"))

## insumos###
dicc_capas = {'capa_1':{'ruta':path_insumos +"procesamiento/carreteras/fv_carreteras.tif",'w':0.28},
            #'capa_2':{'ruta':path_insumos +"procesamiento/anp/fv_anp_yuc.tif",'w':0.04},
            'capa_2':{'ruta':path_insumos +"procesamiento/distancia_costa/fv_distancia_costa_yuc.tif",'w':0.58},
            'capa_3':{'ruta':path_insumos +"procesamiento/localidades_costeras/fv_localidades_costeras.tif",'w':0.14},
            }

### Ruta de capa maestra, puede ser cualquiera de los insumos ###
path_capa_maestra=path_insumos +"procesamiento/localidades_costeras/fv_localidades_costeras.tif"
## Ruta del directorio donde se almacenarán las salidas 
path_salida = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/pruebas/owa/"

capas, w = insumos_base(dicc_capas)
## lista de valores que toma alpha, para cada valor genera una salida
owa_alphas = [0.0001,0.1,0.5,1.0,2.0,5.0,10.0]

print ("procesando owa",time.strftime("%H:%M:%S"))  #imprime la hora que inicia el proceso

genera_owa(capas,w,owa_alphas,path_capa_maestra,path_salida)

print (time.strftime("%H:%M:%S"))  # imprime la hora una vez terminada la ejecución