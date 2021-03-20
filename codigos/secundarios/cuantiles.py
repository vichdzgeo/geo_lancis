import os
import numpy as np 
from osgeo import gdal
from osgeo import osr
import matplotlib.pyplot as plt
import matplotlib as mpl
def gdal_mix_max(path_raster):
    r = gdal.Open(path_raster)
    banda1=r.GetRasterBand(1)
    stats = banda1.GetStatistics(True, True)
    min,max = stats[0],stats[1]
    print (min,max)
    return min,max

def equidistantes (path_r,categorias=5):
    min,max = gdal_mix_max(path_r)
    lista_val = [min,]
    incremento = (max - min) / categorias
    for i in range(1,categorias+1):
        valor = min + (incremento * i)
        lista_val.append(valor)
    print (lista_val)
    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band2= band1[band1 >=min]
    band2 = band2.flatten()
    lista_pix = []
    for j in range(1,len(lista_val)):
        pixeles = np.sum((np.logical_and(band2>=lista_val[j-1], band2<=lista_val[j])))
        print(pixeles)
        lista_pix.append(pixeles)
    return lista_val,lista_pix

def cuantiles(path_r,quantil):
    min,max = gdal_mix_max(path_r)
    raster = gdal.Open(path_r)
    band1 =raster.GetRasterBand(1).ReadAsArray()
    nodata_r=raster.GetRasterBand(1).GetNoDataValue()
    band2= band1[band1 >=min]
    band2 = band2.flatten()
    print (band2)
    lista_val = [min,]
    lista_pix = []
    
    for i in range(1,quantil+1):
        print (i,i/quantil)
        valor= i/quantil
        cuantil_c = np.quantile(band2,valor)
        lista_val.append(cuantil_c)
    lista_cuantiles =['Q'+str(x)+'\n'+str(round(lista_val[x-1],3))+' - '+str(round(lista_val[x],3)) for x in range(1,quantil+1)]
    for j in range(1,len(lista_val)):
        pixeles = np.sum((np.logical_and(band2>=lista_val[j-1], band2<=lista_val[j])))
        print(pixeles)
        lista_pix.append(pixeles)
   

    return lista_val,lista_cuantiles,lista_pix
def grafica_cats(lista_val,lista_pix,categorias):
    ## PARA ESTILO DE LAS GRAFICAS
    # palette={"primary":"#FEF702",
    #          "background": "#252525",
    #          "primary_chart":"#F1F1F1",
    #          "text_color": "#7F7F7F"}

    # mpl.rcParams["figure.facecolor"] = palette["background"]
    # mpl.rcParams["axes.facecolor"] = palette["background"]
    # mpl.rcParams["savefig.facecolor"] = palette["background"]
    # mpl.rcParams['axes.labelcolor']= palette["text_color"]
    fig = plt.figure(u'Expansión turística Máxima') # Figure
    ax = fig.add_subplot(111) # Axes
    lista_cats =['Cat_'+str(x)+'\n'+str(round(lista_val[x-1],3))+' - '+str(round(lista_val[x],3)) for x in range(1,categorias+1)]
    nombres = lista_cats
    datos = lista_pix
    xx = range(len(datos))


    plt.title("Expansión turística Máxima",
                horizontalalignment = 'left',
                x=0.05,
                y=0.99,
                color='#691e91',
                pad=25)

    ax.bar(xx, datos, width=0.5, align='center',color='#691e91')
    ax.set_xticks(xx)
    ax.set_xticklabels(nombres)
    ax.set_ylabel('Pixeles')
    ax.set_xlabel('Cuantiles')
    plt.show()
path_r = 'C:/Dropbox (LANCIS)/FOMIX/fmx_estudio_tecnico/diagnostico/talleres/sectores/agricultura/aptitud/agrie_agricultura_riego_sigindex.tif'

#lista_val,lista_cuantiles,lista_pix = cuantiles(path_r,10)
lista_val,lista_pix= equidistantes(path_r,3)
grafica_cats(lista_val,lista_pix,3)






