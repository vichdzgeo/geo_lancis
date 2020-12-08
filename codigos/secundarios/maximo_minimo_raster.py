# -*- coding: utf-8 -*-


from osgeo import gdal, osr



def raster_min_max(path_raster):
    '''
    esta funciÃ³n regresa el valor mÃ­nimo y mÃ¡ximo de un
    raster

    Ejemplo de uso: 
    min, max = raster_min_max('/../raster.tif')
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")

    extent = rlayer.extent()
    

    provider = rlayer.dataProvider()
    rows = rlayer.rasterUnitsPerPixelY()
    cols = rlayer.rasterUnitsPerPixelX()
    block = provider.block(1, extent,  rows, cols)
    
    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    min = stats.minimumValue
    max = stats.maximumValue
    promedio = stats.mean
    no_data = block.noDataValue()
    dimension = rlayer.height(),rlayer.width()
    pixel = rlayer.rasterUnitsPerPixelX(), rlayer.rasterUnitsPerPixelY()
    return min,max,no_data,extent,dimension,pixel

layer = iface.activeLayer()
path = layer.dataProvider().dataSourceUri()
min,max,nodata,extent,dimension,pixel = raster_min_max(path)
print ("valor minimo :",min)
print ("valor maximo :",max)
print ("valor nodata :",nodata)
print ("extension de capa:", extent)
print ("renglones, columnas:",dimension)
print ("tamaño de pixel X,Y",pixel)
