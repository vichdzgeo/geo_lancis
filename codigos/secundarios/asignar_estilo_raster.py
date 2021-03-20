import numpy as np 

def equidistantes (categories=5,min=0,max=1):
    '''
    Esta función regresa la lista de cortes equidistantes según el número 
    de categorias y el valor minimo y maximo ingresados.

    :param categories: número de categorias 
    :type categories: int 

    :param min: valor mínimo de la capa
    :type min: float

    :param max: valor máximo de la capa
    :type max: float
    
    '''

    list_val = [min,]
    incremento = (max - min) / categories
    for i in range(1,categories+1):
        valor = min + (incremento * i)
        list_val.append(valor)
    print (list_val)
    return list_val
def raster_min_max(rlayer):
    '''

    Ejemplo de uso: 
    min, max = raster_min_max('/../raster.tif')
    '''
    #rlayer = QgsRasterLayer(path_raster,"raster")

    extent = rlayer.extent()
    provider = rlayer.dataProvider()

    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    min = stats.minimumValue
    max = stats.maximumValue
    return min,max

def wf(fp=2, min=0, max=1, categories=5,sentido='directo'):
    '''
    Esta funcion regresa de cortes según el método de weber-fechner

    :param fp: factor de progresión 
    :type fp: float

    :param min: valor mínimo de la capa
    :type min: float

    :param max: valor máximo de la capa
    :type max: float

    :param categories: número de categorias
    :type categories: int 

    '''
    dicc_e = {}
    if sentido =='directo':
        list_val = [min,]
        pm = max - min 
        cats = np.power(fp, categories)
        e0 = pm/cats
        for i in range(1 , categories + 1):
            dicc_e['e'+str(i)]= min + (np.power(fp,i) * e0)
            
        for i in range(1, categories + 1):
            list_val.append(dicc_e['e'+str(i)])
            
    elif sentido =='inverso':
        list_val = [max,]
        pm = max - min 
        cats = np.power(fp, categories)
        e0 = pm/cats
        for i in range(1 , categories + 1):
            dicc_e['e'+str(i)]= max - (np.power(fp,i) * e0)
            
        for i in range(1, categories + 1):
            list_val.append(dicc_e['e'+str(i)])
        ist_val = list_val.reverse()
    return list_val

def asignar_estilo_raster(lista_val,raster,rampa = 'vr',ind=1,opacidad=1):
    if len(lista_val)==4:
        if ind==1 and rampa == 'vr':
            colDic = {'MB':'#fcf30a','M':'#f07424','MA':'#820f34'}
            #colDic = {'MB':'#267300','B':'#4ce600','M':'#ffff00','A':'#ff5500','MA':'#730000'}
        elif  ind==1 and rampa == 'av':
            colDic = {'MB':'#ffee7e','M':'#f35864','MA':'#691e91'}
        elif ind==-1 and rampa == 'vr':
            colDic = {'MB':'#730000','M':'#ffff00','MA':'#267300'}
        elif ind==-1 and rampa == 'av':
            colDic = {'MB':'#691e91','M':'#f35864','MA':'#ffee7e'}
        
        lst = [ QgsColorRampShader.ColorRampItem(lista_val[1],QColor(colDic['MB']),'MB:'+str(round(lista_val[0],3))+'-'+str(round(lista_val[1],3))),\
                QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['M']),'M:'+str(round(lista_val[1],3))+'-'+str(round(lista_val[2],3))), \
                QgsColorRampShader.ColorRampItem(lista_val[3]+0.001, QColor(colDic['MA']),'MA:'+str(round(lista_val[2],3))+'-'+str(round(lista_val[3],3)))]
        
        myRasterShader = QgsRasterShader()
        myColorRamp = QgsColorRampShader()
        
        myColorRamp.setColorRampItemList(lst)
        myRasterShader.setRasterShaderFunction(myColorRamp)
        myColorRamp.setColorRampType("DISCRETE") 
        myPseudoRenderer = QgsSingleBandPseudoColorRenderer(raster.dataProvider(), 
                                                        raster.type(), 
                                                        myRasterShader)
     
        raster.setRenderer(myPseudoRenderer)
        raster.renderer().setOpacity(opacidad)
        raster.triggerRepaint()

    elif len(lista_val)==5:
        if ind==1 and rampa=='vr':
            colDic = {'MB':'#267300','M':'#ffff00','A':'#ff5500','MA':'#730000'}
        elif ind==-1 and rampa=='vr':
            colDic = {'MB':'#730000','M':'#ffff00','A':'#4ce600','MA':'#267300'}
        
        lst = [ QgsColorRampShader.ColorRampItem(lista_val[1],QColor(colDic['MB']),'MB:'+str(round(lista_val[0],3))+'-'+str(round(lista_val[1],3))),\
                    QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['M']),'M:'+str(round(lista_val[1],3))+'-'+str(round(lista_val[2],3))), \
                    QgsColorRampShader.ColorRampItem(lista_val[3], QColor(colDic['A']),'A:'+str(round(lista_val[2],3))+'-'+str(round(lista_val[3],3))), \
                    QgsColorRampShader.ColorRampItem(lista_val[4], QColor(colDic['MA']),'MA:'+str(round(lista_val[3],3))+'-'+str(round(lista_val[4],3)))]
            
        myRasterShader = QgsRasterShader()
        myColorRamp = QgsColorRampShader()
        
        myColorRamp.setColorRampItemList(lst)
        myRasterShader.setRasterShaderFunction(myColorRamp)
        myColorRamp.setColorRampType("DISCRETE") 
        myPseudoRenderer = QgsSingleBandPseudoColorRenderer(raster.dataProvider(), 
                                                        raster.type(), 
                                                        myRasterShader)
        
        raster.setRenderer(myPseudoRenderer)
        raster.renderer().setOpacity(opacidad)
        raster.triggerRepaint()

    elif len(lista_val)==6:
        if ind==1 and rampa == 'vr':
            colDic = {'MB':'#fcf30a','B':'#fbb43b','M':'#f07424','A':'#dc1400','MA':'#820f34'}
            #colDic = {'MB':'#267300','B':'#4ce600','M':'#ffff00','A':'#ff5500','MA':'#730000'}
        elif  ind==1 and rampa == 'av':
            colDic = {'MB':'#ffee7e','B':'#faaf3c','M':'#f35864','A':'#c9008c','MA':'#691e91'}
        elif ind==-1 and rampa == 'vr':
            colDic = {'MB':'#730000','B':'#ff5500','M':'#ffff00','A':'#4ce600','MA':'#267300'}
        elif ind==-1 and rampa == 'av':
            colDic = {'MB':'#691e91','B':'#c9008c','M':'#f35864','A':'#faaf3c','MA':'#ffee7e'}
        
        lst = [ QgsColorRampShader.ColorRampItem(lista_val[1],QColor(colDic['MB']),'MB:'+str(round(lista_val[0],3))+'-'+str(round(lista_val[1],3))),\
                QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['B']),'B:'+str(round(lista_val[1],3))+'-'+str(round(lista_val[2],3))), \
                QgsColorRampShader.ColorRampItem(lista_val[3], QColor(colDic['M']),'M:'+str(round(lista_val[2],3))+'-'+str(round(lista_val[3],3))), \
                QgsColorRampShader.ColorRampItem(lista_val[4], QColor(colDic['A']),'A:'+str(round(lista_val[3],3))+'-'+str(round(lista_val[4],3))), \
                QgsColorRampShader.ColorRampItem(lista_val[5], QColor(colDic['MA']),'MA:'+str(round(lista_val[4],3))+'-'+str(round(lista_val[5],3)))]
        
        myRasterShader = QgsRasterShader()
        myColorRamp = QgsColorRampShader()
        
        myColorRamp.setColorRampItemList(lst)
        myRasterShader.setRasterShaderFunction(myColorRamp)
        myColorRamp.setColorRampType("DISCRETE") 
        myPseudoRenderer = QgsSingleBandPseudoColorRenderer(raster.dataProvider(), 
                                                        raster.type(), 
                                                        myRasterShader)
     
        raster.setRenderer(myPseudoRenderer)
        raster.renderer().setOpacity(opacidad)
        raster.triggerRepaint()

    else:
        print('Warning!!! por ahora el código solo puede asigar estilo a 3,4 o 5 categorias \n\n el estilo que se muestra no es el correcto')
        ##############
    for i in range(len(lista_val)):
        if i < len(lista_val)-1:
            #print ("categoria %d"%(i+1),round(lista_val[i],3)," - ",round(lista_val[i+1],3))
            print (" %d,"%(i+1),round(lista_val[i],3),",",round(lista_val[i+1],3))
    
raster = iface.activeLayer()
#min,max = raster_min_max(raster)
min,max = 0,1
fp = 1.3
categorias = 5
#intervalos = equidistantes(categorias,min,max)
intervalos = wf(fp,min,max,categorias,'inverso')
#asignar_estilo_raster(intervalos,raster,'av',1)

p_salida = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/aptitud_costera/turismo/sin_anp/cortes/'+'owa_cats_'+str(categorias)+'_wf_'+str(fp).replace(".","_")+".csv"
archivo = open(p_salida,"w")
archivo.write("categoria,corte_inf,corte_sup,\n")

for i in range(len(intervalos)):
    if i < len(intervalos)-1:
        cadena = (" %d,"%(i+1)+str(round(intervalos[i],3))+","+str(round(intervalos[i+1],3)))
        archivo.write(cadena+"\n")
archivo.close()