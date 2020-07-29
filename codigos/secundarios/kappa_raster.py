import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import osr


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
    no_capas =2
    

    for i in range(1,no_capas+1):
        for k,v in dicc.items():
            if k == 'capa_'+str(i):
                for k2,v2 in v.items():
                    if k2 == 'ruta':
                        capas.append(raster_to_df(v2,i))
                     
    return capas
#--------------------------------------------------#

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
    dr_r_long=dr_r_long[dr_r_long['r'+str(no_capa)] > 0]

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
def insumo_kappa(capas): # 5 de 9 
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


    no_capas=2
    columnas_matrix =['id','col_r1','ren_r1']
    for no in range(1,no_capas+1):
        columnas_matrix.append('r'+str(no))
        
    matrix_join = reduce(juntar,capas)
    matrix_v = matrix_join.filter(columnas_matrix)
    
    if no_capas==2:
    matrix_v['v']=matrix_v.apply(lambda x: [x['r1'],x['r2']],axis = 1)
    else:
        print ("Solo se ingresan dos capas")
  
    m2=matrix_v.filter(['id','v'])
    return m2
#----------------------------------------------------#



print (time.strftime("%H:%M:%S"))

## insumos###
dicc_capas = {'capa_1':{'ruta':"C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/kappa/insumos/usv_s1_int_ze.tif"},
              'capa_2':{'ruta':"C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/kappa/insumos/usv_s6_int_ze.tif"}
            }

### Ruta de capa maestra, puede ser cualquiera de los insumos ###

## Ruta del directorio donde se almacenarán las salidas 






def indice_kappa(dicc_capas,categorias,path_csv):
    capas= insumos_base(dicc_capas)
    array=insumo_kappa(capas)
    matrix = {}
    
    for i in range(categorias):
        matrix[i+1]=[0]*categorias

    
    for b in range(categorias):
        for value in array['v']:
            for c in range(categorias):
                if value[1] == b+1 and value[0]==c+1:  
                    matrix[b+1][c]+=1

    diagonal_principal =[]
    for i in range(categorias):
        diagonal_principal.append(matrix[i+1][i])

    total=0.0

    for k,v in matrix.items():
        for valor in v:
            total+=float(valor)

    acuerdos = sum(diagonal_principal) 
    #print (matrix)
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
    #print ("acuerdos",diagonal_principal)
    matrix_csv = open(path_csv,"w")
    encabezado = ["clas/ref"]
    for k1,v1, in matrix.items():
        encabezado.append(("clase_"+str(k1)))
    matrix_csv.write(",".join(encabezado)+"\n")

    for k1,v1, in matrix.items():
        renglon = []
        renglon.append("clase_"+str(k1))
        for v2 in v1:
            renglon.append(str(v2))
        matrix_csv.write(",".join(renglon)+"\n")
        
    matrix_csv.close()
    print ("escribiendo matriz...")
    print ("el proceso ha finalizado")
    print ("ruta",path_csv)
