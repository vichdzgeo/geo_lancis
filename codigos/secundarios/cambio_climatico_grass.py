#!/usr/bin/env python3

import grass.script as gscript
import pandas as pd 
import os 
from functools import reduce

## proyecto en grass yucatan_fomx##
def lista_tiff(path):
    lista_shp=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.tif':
                ruta = (root.replace("\\","/")+"/").replace("//","/")+name
                lista_shp.append(ruta)
    return lista_shp
def nombre_capa (path_capa):
    return path_capa.split("/")[-1].split(".")[0]
def importa_capa_raster(path_r,nombre):

    gscript.run_command('r.import',
                        input=path_r,
                        output=nombre,
                        overwrite=True,
                        quiet=True,
                        )

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

    return pd.merge(left, right, on='id_mun', how='outer')
def lista_filtros(lista, filtro1,filtro2,filtro3,filtro4):

    lista_filtrada = []

    for element in lista:

        if filtro1 in element and filtro2 in element and filtro3 in element and filtro4 in element:

            lista_filtrada.append(element)

    return lista_filtrada
def lista_csv(path,filtro1,filtro2,filtro3,filtro4):
    lista_shp=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.csv' and filtro1 in name and filtro2 in name and filtro3 in name and filtro4 in name:
                ruta = (root.replace("\\","/")+"/").replace("//","/")+name
                lista_shp.append(ruta)
    return lista_shp

def juntar_csv(lista_datos,path_salida):
    data = []
    for dato in lista_datos:
        data.append(pd.read_csv(dato))
    matrix_join = reduce(juntar,data)
    matrix_join.round(3).to_csv(path_salida,index=False)

def promedios_zonas(mapa_base,cobertura,path_salida):

    mapa_salida = "tp_mun_"+cobertura
    mes = cobertura.split("_")[-1]

    variable = cobertura.split("_")[0]
    archivo = open(path_salida+mapa_salida+".csv",'w')

    
    archivo.write('id_mun,d_'+variable+'_'+str(mes)+'\n')
    gscript.run_command('r.stats.zonal', 
                        base=mapa_base+'@PERMANENT',
                        cover=cobertura,
                        method='average',
                        overwrite=True,
                        quiet=True,
                        output=mapa_salida)

    p = gscript.pipe_command("r.stats", 
                             input=[mapa_base+'@PERMANENT',mapa_salida], 
                             flags="AnN",
                             separator='comma')
    for line in p.stdout:
        linea = str(line).replace("\\r\\n","").replace("b'","").replace("'","")
        archivo.write(linea+'\n')
    archivo.close()



def main():
    path_capas = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/cambio_climatico/'
    modelos = ['CNRMCM5','GFDL_CM3','HADGEM2_ES','MPI_ESM_LR']
    variables = ['prec','tmin','tmedia','tmax']
    horizontes = ['2015_2039','2045_2069','2075_2099']
    reforzamientos = ['rcp45','rcp85']
    meses = ['01','02','03','04','05','06','07','08','09','10','11','12']
    path_salida = 'C:/cambio_climatico/procesamiento/'
    path_salida_join = 'C:/cambio_climatico/salidas/'
    lista_capas = lista_tiff(path_capas)
    #[importa_capa_raster(ci,nombre_capa(ci))  for ci in lista_capas]

    capas = [nombre_capa(ci) for ci in lista_capas]
    print ("capas importadas")

    for modelo in modelos:

        for variable in variables:

            for reforzamiento in reforzamientos:

                for horizonte in horizontes:

                    capas_meses = lista_filtros(capas,modelo,variable,reforzamiento,horizonte)

                    for capa_m in capas_meses:

                        promedios_zonas('municipios_nombre_yuc',capa_m,path_salida)

                    juntar_csv(lista_csv(path_salida,modelo,variable,reforzamiento,horizonte),path_salida_join+"delta_"+"_".join([variable,modelo,reforzamiento,horizonte])+'.csv')
    ## PROCEDIMIENTO DE EJEMPLO##
    # for mes in meses:
    #     promedios_zonas('municipios_nombre_yuc','prec_CNRMCM5_rcp45_r1i1p1_2015_2039_Delta_'+str(mes),path_salida)
    # juntar_csv(path_salida,path_salida_join+'prec_CNRMCM5_rcp45_r1i1p1_2015_2039.csv')
if __name__ == '__main__':


    main()
