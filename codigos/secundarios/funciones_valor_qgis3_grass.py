import os, sys, subprocess
import string 
import json
import processing as pr

def raster_nodata(path_raster):
    '''

    '''
    rlayer = QgsRasterLayer(path_raster,"raster")
    extent = rlayer.extent()
    provider = rlayer.dataProvider()
    rows = rlayer.rasterUnitsPerPixelY()
    cols = rlayer.rasterUnitsPerPixelX()
    block = provider.block(1, extent,  rows, cols)
    no_data = block.noDataValue()

    return no_data

def remove_raster(path_r):
    '''
    Esta función elimina una capa del sistema

    :param path_r: ruta de la capa 
    :type path_r: str

    '''
    os.remove(path_r)


def get_region(path_layer):
        '''
        Esta función regresa en forma de cadena de texto 
        las coordenadas de la extensión de una capa raster xmin,xmax,ymin,ymax

        param path_layer: ruta de la capa raster
        type path_layer: str
        '''

        layer = QgsRasterLayer(path_layer,"")
        ext = layer.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()

        region = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)
        return region 
def calculadora_grass_full(ecuacion,path_salida,path_a,path_b=None,path_c=None,path_d=None,path_e=None,path_f=None):
        '''
        :param ecuacion: expresión matemática en formato string, donde las capas raster se representan por las letras A,B,C,D,E,F
        :type ecuacion: str
        :param path_salida: ruta de la capa resultado de aplicar la máscara
        :type path_salida: str

        :param path_a: ruta de la capa "A" 
        :type path_capa: str

        :param path_b: ruta de la capa "B" 
        :type path_capa: str
        
        :param path_c: ruta de la capa "C" 
        :type path_capa: str
        
        :param path_d: ruta de la capa "D" 
        :type path_capa: str

        :param path_e: ruta de la capa "E" 
        :type path_capa: str

        :param path_f: ruta de la capa "F" 
        :type path_capa: str
        '''
        region = get_region(path_a)

        dicc = {'a':path_a,
        'b':path_b,
        'c':path_c,
        'd':path_d,
        'e':path_e,
        'f':path_f,
        'expression':ecuacion,
        'output':path_salida,
        'GRASS_REGION_PARAMETER':region,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        pr.run("grass7:r.mapcalc.simple", dicc)

def calculadora_grass(path_capa, ecuacion,path_salida):
        '''
        Esta función aplica la máscara de la zona de estudio

        :param path_mascara: ruta de la mascara en formato tiff
        :type path_mascara: str


        :param path_capa: ruta de la capa a la cual se requiere aplicar la máscara
        :type path_capa: str

        :param path_salida: ruta de la capa resultado de aplicar la máscara
        :type path_salida: str

        :param region: coordenadas de la región del estudio  xmin,xmax,ymin,ymax
        :type region: str
        '''
        region = get_region(path_capa)

        dicc = {'a':path_capa,
        'b':None,
        'c':None,
        'd':None,
        'e':None,
        'f':None,
        'expression':ecuacion,
        'output':path_salida,
        'GRASS_REGION_PARAMETER':region,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}
        pr.run("grass7:r.mapcalc.simple", dicc)
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
                    '+exp(-'+k+' * ( '+\
                    '(100 * (A - '+ xmin+') / ('+ xmax +' - '+xmin+'))' +\
                    ' - (100 * ('+center+"-"+xmin+") / ("+xmax+' - '+xmin+")))))"
        return ecuacion

def logistica_invertida(k, center, xmax, xmin):
        
        ecuacion = '1 - ('+ logistica(k, center, xmax, xmin)+')'
        return ecuacion 
def gaussian(a, center, xmax, xmin):
       
        ecuacion = 'exp(0.0 - (('+\
                '('+normalize100(xmax,xmin)+\
                '-'+normalize100_center(center,xmax,xmin)+') / ('+ a +'))**2))'
        return ecuacion 

def campana_invertida(a, center, xmax, xmin):
        '''
        '''
        ecuacion = '1.0 - (' + gaussian(a, center, xmax, xmin)+')'
        return ecuacion

def concava_decreciente(gama, xmax, xmin):
        ecuacion = '((exp('+ gama + '* ('+\
                '100.0 - (100.0 * (A - '+xmin+')'+\
                '/ ('+ xmax +'-'+ xmin +'))))) - 1) / (exp('+gama+'* 100) -1)'
        return ecuacion 

def concava_creciente(gama, xmax, xmin): 
        ecuacion = '((exp(' +\
                gama + '* (100' +\
                '*'+\
                '(A -'+xmin+')'+\
                '/'+\
                '('+xmax+'-'+xmin+')))) - 1) / (exp('+gama+' * 100) -1)'
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
        no_data = raster_nodata(path_raster)
        xmax_menos_xmin = max-min
        xmax_menos_xmin_xmax = xmax_menos_xmin / max
        xmax_mas_xmin = max + min
        xmax_mas_xmin_xmax = xmax_mas_xmin / max
        ec_norm ='((-A * '+str(xmax_menos_xmin_xmax)+') / '+str(xmax_menos_xmin)+') + '+str(xmax_mas_xmin_xmax)  # llevar a ideal 
        return ec_norm

def funcion_valor_D(path_A,archivo_txt,salida):
        reglas = open(archivo_txt,'r')
        lista =[]
        for line in reglas:
                linea = line.rstrip().replace(" ","")
                lista.append(linea.split("="))

        ec =[]
        for fv in lista:
                ec.append('(A=='+fv[0]+')*'+fv[1])

        ecuacion = " + ".join(ec)
        calculadora_grass(path_A,ecuacion,salida)
        

def funcion_valor(path_A,archivo_json,salida):
        data = leer_json(archivo_json)
        tipo_funcion = data['function_name']

        if tipo_funcion == 'logistic':
                center = data['center']
                xmin = data['min']
                xmax = data['max']
                k = data['k']
                ecuacion = logistica(k, center, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)

        elif tipo_funcion == 'convexa_creciente':
                gama = data['gama']
                xmin = data['min']
                xmax = data['max']
                ecuacion = convexa_creciente(gama, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)

        elif tipo_funcion == 'concava_creciente':
                gama = data['gama']
                xmin = data['min']
                xmax = data['max']
                ecuacion = concava_creciente(gama, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)
                norm_estandar(salida)
        elif tipo_funcion == 'logistica_invertida':
                center = data['center']
                xmin = data['min']
                xmax = data['max']
                k = data['k']
                ecuacion = logistica_invertida(k, center, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)
                

        elif tipo_funcion == 'convexa_decreciente':
                gama = data['gama']
                xmin = data['min']
                xmax = data['max']
                ecuacion = convexa_decreciente(gama, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)


        elif tipo_funcion == 'concava_decreciente':
                gama = data['gama']
                xmin = data['min']
                xmax = data['max']
                ecuacion = concava_decreciente(gama, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)
        elif tipo_funcion == 'gaussian':
                a = data['a']
                center = data['center']
                xmin = data['min']
                xmax = data['max']
                ecuacion = gaussian(a, center, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)
        elif tipo_funcion == 'campana_invertida':
                a = data['a']
                center = data['center']
                xmin = data['min']
                xmax = data['max']
                ecuacion = campana_invertida(a, center, xmax, xmin)
                calculadora_grass(path_A,ecuacion,salida)

