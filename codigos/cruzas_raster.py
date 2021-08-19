import copy
import pprint
import string
import qgis 
import qgis.core
import numpy as np
from osgeo import gdal
import gdal_calc
import os
import processing as pr 
import gdalnumeric
import pandas as pd 
import time 
from functools import reduce
from osgeo import osr

## FUNCIONES DE SEGUNDO PLANO ###
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

  
    return dr_r_long
    
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
def raster_nodata(path_raster):

    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    

    provider = rlayer.dataProvider()
    rows = rlayer.rasterUnitsPerPixelY()
    cols = rlayer.rasterUnitsPerPixelX()
    block = provider.block(1, extent,  rows, cols)

    no_data = block.noDataValue()

    
    return no_data
## fUNCIONES UTILES #####
def categorias_unicas_raster(path_raster):
    """
    Regresa una lista de valores unicos

    """
    
    v_nodata = raster_nodata(path_raster)
    raster_matrix = gdalnumeric.LoadFile(path_raster)


    valores_unicos = list(np.unique(raster_matrix))
    if -999 in valores_unicos:
        valores_unicos.remove(-999)
    else:
        valores_unicos.remove(v_nodata)
    return valores_unicos
def areas_por_categorias(path_raster,path_salida,dicc_cats={0:'Nula',1:'Muy baja',2:'Baja',3:'Moderada',4:'Alta',5:'Muy alta'}):
    """
    Calcula el porcentaje del área por categoria 
    como salida se tiene un archivo en excel 
    """
    valores = categorias_unicas_raster(path_raster)
    raster_matrix =  gdalnumeric.LoadFile(path_raster)
    dicc = {}
    area_total = 0
    for i in valores:
        total_pixeles_cat = (raster_matrix == i).sum() 
        area = total_pixeles_cat/100
        dicc[i]= area
        area_total +=area
        
    
    archivo = open(path_salida,'w')
    archivo.write("Categoría,km²,Porcentaje del estado\n")

    
    for i in valores:
        archivo.write(",".join([dicc_cats[i],str(round(dicc[i],1)),str(round((dicc[i]*100/area_total),1))])+"\n")
    archivo.close()
    arch_csv = pd.read_csv(path_salida)
    
    df_o = arch_csv.sort_index(ascending=False)
    if df_o['Porcentaje del estado'].sum()!=100:
        print ("Verificar la suma de porcentaje")
        sum_por = df_o['Porcentaje del estado'].sum()
        df_o['notas']="verificar porcentajes "+str(sum_por)
    print (df_o)
    df_o.to_excel( path_salida.split(".")[0]+".xlsx",index = False, header=True)

def cruza_2_capas(path_a,path_b,etiquetas,path_bd_cruza,dicc_cats_a={},dicc_cats_b={},por_cat_a='no'):
    capa_1=etiquetas[0]
    capa_2=etiquetas[1]
    valores_a = categorias_unicas_raster(path_a)
    valores_b = categorias_unicas_raster(path_b)
    if len(dicc_cats_a) ==0:
        for a in valores_a:
            dicc_cats_a[a]=str(a)

    if len(dicc_cats_b) ==0:
        
        for b in valores_b:
            dicc_cats_b[b]=str(b)

    datos = [raster_to_df(path_a,1),raster_to_df(path_b,2)]
    matrix_join = reduce(juntar,datos)
    matrix_join.rename(columns={'r1':capa_1}, inplace=True)
    matrix_join.rename(columns={'r2':capa_2}, inplace=True)
    archivo = open(path_bd_cruza, "w")
    if por_cat_a == 'no':
        archivo.write(",".join(["val_"+capa_1,"cat_"+capa_1,"val_"+capa_2,"cat_"+capa_2,"no_pixeles"])+"\n")
    elif por_cat_a == 'si':
        archivo.write(",".join(["val_"+capa_1,"cat_"+capa_1,"val_"+capa_2,"cat_"+capa_2,"no_pixeles",'porcentaje'])+"\n")
    for a in valores_a:
        for b in valores_b:
            if por_cat_a == 'no':
                no_pix = matrix_join.query(capa_1+' == ' +str(a) +' & '+capa_2 +'== '+str(b)).filter([capa_2]).count()[0]
                archivo.write(",".join([str(a),dicc_cats_a[a],str(b),dicc_cats_b[b],str(no_pix)])+"\n")
            elif por_cat_a == 'si':
                no_pix = matrix_join.query(capa_1+' == ' +str(a) +' & '+capa_2 +'== '+str(b)).filter([capa_2]).count()[0]
                pix_for_a = matrix_join.query(capa_1+' == ' +str(a)).filter([capa_1]).count()[0]
                porcentaje = round((no_pix/pix_for_a)*100,2)
                archivo.write(",".join([str(a),dicc_cats_a[a],str(b),dicc_cats_b[b],str(no_pix),str(porcentaje)])+"\n")
    archivo.close()
    df_areas = pd.read_csv(path_bd_cruza).query("no_pixeles > 0")
    df_areas.to_excel( path_bd_cruza.split(".")[0]+".xlsx",index = False ,header=True)

