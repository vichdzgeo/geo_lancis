import numpy as np 
import pandas as pd 
import time 
from functools import reduce
from osgeo import gdal
from osgeo import osr


'''
Proyecto: FOMIX YUCATÁN
Objetivo:   Generar matriz de transición a partir de dos capas raster de Uso de suelo y vegetación
Autor: LANCIS APC
Desarrollado en: Qgis 3.10, python 3
Contacto: victor.hernandez@iecologia.unam.mx
'''

def gdal_mix_max(path_raster):
    raster = gdal.Open(path_raster)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    dimension = band1.shape
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band1 = np.ma.masked_equal(band1, nodata_r)
    return band1.min(),band1.max()
    
def nombre_capa(path_capa):
    '''
    Esta función regresa el nombre de una capa sin extensión 

    :param path_capa: ruta de la capa
    :type path_capa: str 


    '''
    nombre_capa=(path_capa.split("/")[-1:])[0].split('.')[0]
    return nombre_capa


def raster_max(path_raster):
    '''

    Ejemplo de uso: 
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    provider = rlayer.dataProvider()
    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    max = stats.maximumValue

    
    return max


def genera_matrix(array,cat_min,cat_max):
    matrix = {}
    for i in range(cat_min,cat_max+1):
        matrix[i]=[0]*len(range(cat_min,cat_max+1))

    if cat_min==0:
        for b in range(cat_min,cat_max+1):
            for value in array['v']:
                for c in range(cat_min,cat_max+1):
                    if value[1] == b and value[0]==c:#if value[1] == b+1 and value[0]==c+1:  
                        matrix[b][c]+=1

    else:
        for b in range(cat_min,cat_max+1):
            for value in array['v']:
                for c in range(cat_min,cat_max+1):
                    if value[1] == b and value[0]==c:#if value[1] == b+1 and value[0]==c+1:  
                        matrix[b][c-1]+=1
    return matrix
def total_matrix(matrix):
    total=0.0
    for k,v in matrix.items():
        for valor in v:
            total+=float(valor)
    return total
def calcula_acuerdos(matrix,cat_min,cat_max):
    diagonal_principal =[]
    if cat_min==0:
        for i in range(cat_min,cat_max+1):
            diagonal_principal.append(matrix[i][i])
    else:
        for i in range(cat_min,cat_max+1):
            diagonal_principal.append(matrix[i][i-1])
    return sum(diagonal_principal) 
def calcula_kappa(matrix,cat_min,cat_max):
    columnas_renglones =0
    total=total_matrix(matrix)
    acuerdos = calcula_acuerdos(matrix,cat_min,cat_max)
    for j in range(cat_min,cat_max+1):
        suma_renglon=[]
        suma_columna=[]
        if cat_min==0:
            for i in range(cat_min,cat_max+1):
                suma_columna.append(matrix[i][j])
                suma_renglon.append(matrix[j][i])
        else:
            for i in range(cat_min,cat_max+1):
                suma_columna.append(matrix[i][j-1])
                suma_renglon.append(matrix[j][i-1])
        columnas_renglones+=((sum(suma_renglon)*sum(suma_columna))/total)

    kappa = round((acuerdos - columnas_renglones)/(total -columnas_renglones),3)
    return kappa
def matriz_transicion(dicc_capas,cat_min,cat_max,path_csv):

    capas= insumos_base(dicc_capas)
    array=insumo_kappa(capas)
    matrix = genera_matrix(array,cat_min,cat_max)
    k = calcula_kappa(matrix,cat_min,cat_max)
    
    print ("el valor de kappa es: ",k)
    matrix_csv = open(path_csv,"w")

    encabezado=["cat#"]
    for k1,v1, in matrix.items():
        encabezado.append((str(k1)))
    matrix_csv.write(",".join(encabezado)+"\n")

    for k1,v1, in matrix.items():
        renglon = []
        renglon.append(str(k1))
        for v2 in v1:
            renglon.append(str(v2))
        matrix_csv.write(",".join(renglon)+"\n")
    matrix_csv.write("\n\n el valor de kappa es:, %3f"%k)
    matrix_csv.close()
    
    return matrix 
    
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

    return dr_r_long.query("r"+str(no_capa)+">=0")

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
    matrix_v['v']=[[a,b]for a,b in zip(matrix_v['r1'],matrix_v['r2'])]
    m2=matrix_v.filter(['id','v'])
    return m2
#----------------------------------------------------#


path_sig = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/pruebas/'


# las categorias de las columnas corresponden a la capa_1, los renglones a la capa 2
dicc_capas = {'capa_1':{'ruta':'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/areas_conservacion/procesamiento/serie_6_inegi_100m.tif'},
             'capa_2':{'ruta':'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/areas_conservacion/procesamiento/mapacobertura_2016_yucatan_rev_sept_100m.tif'}
           }

# dicc_capas = {'capa_1':{'ruta':'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_aptitud/insumos/generales/cobertura_usv_svi_16cats.tif'},
#               'capa_2':{'ruta':'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_aptitud/insumos/generales/cobertura_conafor.tif'}
#             }

inicio = time.time()
path_csv = path_sig+'matrix_confusion_'+nombre_capa(dicc_capas['capa_1']['ruta'])+'_vs_'+nombre_capa(dicc_capas['capa_2']['ruta'])+'.csv'
cat_min,cat_max = gdal_mix_max(dicc_capas['capa_1']['ruta'])
#cat_min,cat_max = raster_min_max(dicc_capas['capa_1']['ruta'])
matriz = matriz_transicion(dicc_capas,int(cat_min),int(cat_max),path_csv)
fin = time.time()

print ("tiempo transcurrido en segundos",round(fin-inicio,0))