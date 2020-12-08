import os, sys, subprocess, processing 
import string 
import json
import processing 


def leer_json(path):
        '''
        Esta lee un archivo json
        :param path: Ruta del archivo json
        :type path: String 
        '''
        data = json.load(open(path))
        return data

def raster_min_max(path_raster):
    '''

    Ejemplo de uso: 
    min, max = raster_min_max('/../raster.tif')
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")

    extent = rlayer.extent()
    provider = rlayer.dataProvider()

    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    min = stats.minimumValue
    max = stats.maximumValue
    return min,max

def normalize100(xmax, xmin):
        
        

        ecuacion = '(100.0 * (A -'+ xmin +') / ('+ xmax +'-' + xmin +'))'
        return ecuacion
def normalize100_center(center,xmax, xmin):
        
        
        ecuacion = '(100.0 * ('+center +'-'+ xmin +') / ('+ xmax +'-' + xmin +'))'
        return ecuacion

def logistica(k, center, xmax, xmin):
        
        ecuacion ='1 / (1.0' +\
                    '+ numpy.exp(-'+k+' * ( '+\
                    '(100 * (A - '+ xmin+') / ('+ xmax +' - '+xmin+'))' +\
                    ' - (100 * ('+center+"-"+xmin+") / ("+xmax+' - '+xmin+")))))"
        return ecuacion

def logistica_invertida(k, center, xmax, xmin):
        
        ecuacion = '1 - ('+ logistica(k, center, xmax, xmin)+')'
        return ecuacion 
def gaussian(a, center, xmax, xmin):
       
        ecuacion = 'numpy.exp(0.0 - (('+\
                '('+normalize100(xmax,xmin)+\
                '-'+normalize100_center(center,xmax,xmin)+') / ('+ a +'))**2))'
        return ecuacion 

def campana_invertida(a, center, xmax, xmin):
        '''
        '''
        ecuacion = '1.0 - (' + gaussian(a, center, xmax, xmin)+')'
        return ecuacion

def concava_decreciente(gama, xmax, xmin):
        ecuacion = '((numpy.exp('+ gama + '* ('+\
                '100.0 - (100.0 * (A - '+xmin+')'+\
                '/ ('+ xmax +'-'+ xmin +'))))) - 1) / (numpy.exp('+gama+'* 100) -1)'
        return ecuacion 

def concava_creciente(gama, xmax, xmin): 
        ecuacion = '((numpy.exp(' +\
                gama + '* (100' +\
                '*'+\
                '(A -'+xmin+')'+\
                '/'+\
                '('+xmax+'-'+xmin+')))) - 1) / (numpy.exp('+gama+' * 100) -1)'
        return ecuacion
                
def convexa_decreciente(gama, xmax, xmin):
        ecuacion = '1.0 - '+concava_creciente(gama,xmax,xmin)
        return ecuacion 

def convexa_creciente(gama, xmax, xmin):
        ecuacion = '1.0 -'+ concava_decreciente(gama, xmax, xmin)
        return ecuacion 

def linear(m, b):
        ecuacion = '(' + m +' * A) + '+b
        return ecuacion
def linear_decreciente(path_raster):
    min,max = raster_min_max(path_raster)
    no_data =raster_nodata(path_raster)
    xmax_menos_xmin = max-min
    xmax_menos_xmin_xmax = xmax_menos_xmin / max
    xmax_mas_xmin = max + min
    xmax_mas_xmin_xmax = xmax_mas_xmin / max
    ec_norm ='((-A * '+str(xmax_menos_xmin_xmax)+') / '+str(xmax_menos_xmin)+') + '+str(xmax_mas_xmin_xmax)  # llevar a ideal 
    return ec_norm

def norm_estandar(path_raster):
    entries = []

    #abre el archivo raster1
    fileInfo = QFileInfo(path_raster)
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    layer1 = QgsRasterLayer(path, baseName)
    var1 = QgsRasterCalculatorEntry()
    var1.ref = 'layer1@1'
    var1.raster = layer1
    var1.bandNumber = 1
    entries.append( var1 )
    
    xmin,xmax = raster_min_max(path)
    ecuacion = "("+ 'layer1@1' +" - "+str(xmin)+")/("+str(xmax)+" - "+str(xmin)+")"
    raster_salida  = path.split(".")[0]+"_n.tif"
    calc = QgsRasterCalculator(ecuacion, 
                                raster_salida, 
                                'GTiff', 
                                layer1.extent(), 
                                layer1.width(), 
                                layer1.height(),
                                entries)
                                
    calc.processCalculation()

def gdal_calculadora(ecuacion,path_a,salida):
    dicc ={        
            'INPUT_A':path_a,
            'BAND_A':1,
            'FORMULA':ecuacion,
            'NO_DATA': -9999.0,
            'RTYPE':5,
            'EXTRA':'--co="COMPRESS=LZW"',
            'OUTPUT':salida}
    pr.run("gdal:rastercalculator",dicc)


def funcion_valor(path_A,archivo_json,salida):
    data = leer_json(archivo_json)
#    tipo = tipo_raster(path_A)
    tipo_funcion = data['function_name']
    # if tipo =='UInt16' or tipo =='Int16' or tipo =='Byte' or tipo =='Float64':
    #         path_A=raster_float(path_A)

    if tipo_funcion == 'logistic':
            center = data['center']
            xmin = data['min']
            xmax = data['max']
            k = data['k']
            ecuacion = logistica(k, center, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)
    elif tipo_funcion == 'convexa_creciente':
            gama = data['gama']
            xmin = data['min']
            xmax = data['max']
            ecuacion = convexa_creciente(gama, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)
    elif tipo_funcion == 'concava_creciente':
            gama = data['gama']
            xmin = data['min']
            xmax = data['max']
            ecuacion = concava_creciente(gama, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)
    elif tipo_funcion == 'logistica_invertida':
            center = data['center']
            xmin = data['min']
            xmax = data['max']
            k = data['k']
            ecuacion = logistica_invertida(k, center, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida_tp)
            norm_estandar(salida)
    elif tipo_funcion == 'convexa_decreciente':
            gama = data['gama']
            xmin = data['min']
            xmax = data['max']
            ecuacion = convexa_decreciente(gama, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)

    elif tipo_funcion == 'concava_decreciente':
            gama = data['gama']
            xmin = data['min']
            xmax = data['max']
            ecuacion = concava_decreciente(gama, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)
    elif tipo_funcion == 'gaussian':
            a = data['a']
            center = data['center']
            xmin = data['min']
            xmax = data['max']
            ecuacion = gaussian(a, center, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)
    elif tipo_funcion == 'campana_invertida':
            a = data['a']
            center = data['center']
            xmin = data['min']
            xmax = data['max']
            ecuacion = campana_invertida(a, center, xmax, xmin)
            gdal_calculadora(ecuacion,path_A,salida)
            norm_estandar(salida)
