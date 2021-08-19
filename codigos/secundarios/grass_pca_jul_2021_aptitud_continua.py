#!/usr/bin/env python3

import grass.script as gscript
import csv 
import operator

def getPuntoDeCorte(data, numCategorias):
    f_t = [0] * numCategorias # genera una lista del tamano de las categorias para guardar los valores de los pixeles de data

    for l in data:
        l_contents = l.split(',') # separa los elementos por coma
        if '*' is not l_contents[0]: # hace un filtrado solo para las categorias
            idx = int(l_contents[0]) # el numero de la categoria se guarda en idx
            f_t[idx-1] = int(l_contents[1])  # guarda el valor de idx en la posición -1 de una lista
    sum_f=0     #variable inicializada en cero
    sum_fx=0 #variable inicializada en cero
    sum_fx2=0 #variable inicializada en cero
    li_var_a=[] # lista vacia
    li_d_sig=[] # lista vacia
    corte=0 #variable inicializada en cero

    for i in range(len(f_t)):
        var_a=0
        x_=i+1 # numero de categoria
        f=f_t[i] # numero de pixeles  de la categoria
        fx=f*x_ # producto de la categoria por el numero de pixeles
        fx2=(x_*x_)*f  # el producto del cuadrado del numero de la categoria y el numero de pixeles
        sum_f += float(f)  #sumatoria del numero de los pixeles
        sum_fx += float(fx) # sumatoria del producto  por el numero de pixeles
        sum_fx2 += float(fx2) #sumatoria del resultado del producto del cuadrado del numero de la categoria y el numero de pixeles
        var_a=(sum_fx2/sum_f)-((sum_fx/sum_f)**2)

        li_var_a.append(var_a)  #agrega a una lista los valores calculados para la variable var_a

    var_total=var_a # toma el ultimo valor de la lista como varianza total

    for i in range(len(f_t)):
        var_b=0
        x_=i+1 # numero de categoria
        f=f_t[i] # numero de pixeles  de la categoria
        fx=f*x_ # producto de la categoria por el numero de pixeles
        fx2=(x_*x_)*f # el producto del numero de la categoria por el cuadrado del numero de pixeles
        sum_f -= float(f) #resta el numero de los pixeles de la categoria al valor sum_f
        sum_fx -= float(fx) #resta el producto  por el numero de pixeles por el numero la categoria al valor sum_fx
        sum_fx2 -= float(fx2) # resta a la variable sum_fx_2 el producto del numero de la categoria por el cuadrado del numero de pixeles
        if i == 10:   # cuanto el contador esta en la ultima posición
            sum_f=f   # la variable sum_f toma el valor de los pixeles de la ultima categoria
            sum_fx=fx # la variable sum_f toma el valor producto de la categoria por el numero de pixeles
            sum_fx2=fx2 # la variable sum_fx2 toma el valor del producto del numero de la categoria por el cuadrado del numero de pixeles
        var_b=(sum_fx2/sum_f)-((sum_fx/sum_f)**2) #
        #print ('var_b',var_b)
        d_sig=var_total-(li_var_a[i]+var_b) # al varlor de var_total le resta el valor de la suma  del valor de la lista  li_var_a en la posición i y el valor var_b
        li_d_sig.append(d_sig)  # se agrega a una lista el valor d_sig
    #print (li_d_sig)
    m=max(li_d_sig)# se obtiene el valor maximo de la lista li_d_sig
    lugar_corte=[i for i, j in enumerate(li_d_sig) if j == m]  #obtiene la posicion o posiciones del valor maximo en la lista li_d_sig
    #delta_corte = abs((li_d_sig[lugar_corte[0]]-li_d_sig[lugar_corte[0]-1]))


    if len(lugar_corte) == 1: # and delta_corte < 0.1: # si el lugar de corte solo contiene una posicion
        corte=lugar_corte[0]+1 # regresa el valor como la posicion +1 ( ya que el indice de las listas de python comienzan en cero )
    elif len(lugar_corte) != 1: # si el tamaño de la lista es diferente a 1
        for ii in range(len(f_t)):  # itera la lista que contiene los numeros de pixeles
            f_v1=ii  # numero de posicion en la lista de 0 a 10
            f_v2=f_t[ii]  # numero de pixeles de la categoria
            #print ("f_v2",f_v2)
            for iii in range(len(lugar_corte)):  # para cada posicion en la lista f_t itera la lista que contiene las posiciones en las que se encuentran los valores maximos
                if lugar_corte[iii] == f_v1:  # si el valor de la posicion en la lista lugar de corte es igual al numero de posicion en la lista
                    if f_v2 == 0:
                        corte = f_v1
                        break

    return corte
def getPuntoDeCorte2(data):
    f_t = {} # genera una lista del tamano de las categorias para guardar los valores de los pixeles de data

    for l in data:
        l_contents = l.split(',') # separa los elementos por coma
        if '*' is not l_contents[0]: # hace un filtrado solo para las categorias
            idx = int(l_contents[0]) # el numero de la categoria se guarda en idx
            f_t[idx] = int(l_contents[1])  # guarda el valor de idx en la posición -1 de una lista
    sum_f=0     #variable inicializada en cero
    sum_fx=0 #variable inicializada en cero
    sum_fx2=0 #variable inicializada en cero
    li_var_a={} # lista vacia
    corte=0 #variable inicializada en cero
    define_corte={}
    for cat in list(f_t.keys()):
        var_a=0
        x_=cat # numero de categoria
        f=f_t[cat] # numero de pixeles  de la categoria
        fx=f*x_ # producto de la categoria por el numero de pixeles
        fx2=(x_*x_)*f  # el producto del cuadrado del numero de la categoria y el numero de pixeles
        sum_f += float(f)  #sumatoria del numero de los pixeles
        sum_fx += float(fx) # sumatoria del producto  por el numero de pixeles
        sum_fx2 += float(fx2) #sumatoria del resultado del producto del cuadrado del numero de la categoria y el numero de pixeles
        var_a=(sum_fx2/sum_f)-((sum_fx/sum_f)**2)

        li_var_a[cat]=var_a  #agrega a una lista los valores calculados para la variable var_a

    var_total=var_a # toma el ultimo valor de la lista como varianza total

    for cat in list(f_t.keys()):
        var_b=0
        x_=cat # numero de categoria
        f=f_t[cat] # numero de pixeles  de la categoria
        fx=f*x_ # producto de la categoria por el numero de pixeles
        fx2=(x_*x_)*f # el producto del numero de la categoria por el cuadrado del numero de pixeles
        sum_f -= float(f) #resta el numero de los pixeles de la categoria al valor sum_f
        sum_fx -= float(fx) #resta el producto  por el numero de pixeles por el numero la categoria al valor sum_fx
        sum_fx2 -= float(fx2) # resta a la variable sum_fx_2 el producto del numero de la categoria por el cuadrado del numero de pixeles
        if cat == max(list(f_t.keys())):   # cuanto el contador esta en la ultima posición
            sum_f=f   # la variable sum_f toma el valor de los pixeles de la ultima categoria
            sum_fx=fx # la variable sum_f toma el valor producto de la categoria por el numero de pixeles
            sum_fx2=fx2 # la variable sum_fx2 toma el valor del producto del numero de la categoria por el cuadrado del numero de pixeles
        var_b=(sum_fx2/sum_f)-((sum_fx/sum_f)**2) #
        d_sig=var_total-(li_var_a[cat]+var_b) # al varlor de var_total le resta el valor de la suma  del valor de la lista  li_var_a en la posición i y el valor var_b
        define_corte[cat]=d_sig

    corte = max(define_corte.items(), key=operator.itemgetter(1))[0]
    print(var_total)
    print(define_corte)
    return corte

def capas_i(capas):

    cadena = ",".join(capas)

    return cadena



def pca (capas_input,salida,path_salida):

    gscript.run_command('i.pca',

                        input = capas_input,

                        output = salida,

                        rescale = '1,11',

                        overwrite = True)

    pca1 = salida+'.1'

    print (pca1)
    

    gscript.run_command('r.out.gdal',flags='cm',

                        overwrite=True,

                        input=pca1+'@PERMANENT',

                        format='GTiff',

                        output=path_salida+pca1.split('.')[0]+'.tif',

                        type='Byte')
    return pca1

                   

def eliminar_pca2end (capas,nombre_pca):

    numero = len(capas)

    '''
    for i in range(2,numero+1):
        gscript.run_command('g.remove',flags='f',
                                        type='raster',
                                        name=nombre_pca+'.'+str(i)+'@PERMANENT')           
    '''
        


def consulta_data(capa):

    datos = gscript.pipe_command('r.stats',flags="cn",input=capa,separator='comma')
    data = []
    for line in datos.stdout:
       data.append(str(line).replace("\\r\\n","").replace("b","").replace("'",""))
    return data


def stadistica (capa,ruta):

    gscript.run_command('r.stats',flags='cn',
                    input=capa+'@PERMANENT',
                    separator='comma',
                    overwrite=True,
                    output=ruta+capa.replace('.1','')+'.csv')

    return data_list(ruta+capa.replace('.1','')+'.csv')

def data_list(path_csv):
    with open(path_csv, newline='') as csvfile:
        stat_csv = csv.reader(csvfile, delimiter=',')
        line = []
        for row in stat_csv:
            line.append(','.join(row))
    return line           

def separar_pca(capa,corte):

    capa_a='mask_'+capa+'a'

    capa_b='mask_'+capa+'b'

    capas_salidas = [capa_a,capa_b]

    operacion_a = capa_a + ' = ('+capa+'@PERMANENT <='+str(corte)+')*1'

    operacion_b = capa_b + ' = ('+capa+'@PERMANENT >'+str(corte)+')*1'

    lista_operaciones = [operacion_a,operacion_b]

    for mask in lista_operaciones:

        gscript.run_command('r.mapcalc',

                            overwrite=True,

                            expression=mask)

    for salida in capas_salidas:

        gscript.run_command('r.null',

                            map=salida+'@PERMANENT',

                            setnull=0)

        gscript.run_command('r.out.gdal',flags='cm',

                    overwrite=True,

                    input=salida+'@PERMANENT',

                    format='GTiff',

                    output='grupo_'+salida+'.tif',

                    type='Byte')

    return capas_salidas






def capa_grupos(capas_salidas,path_salida):
    operacion = ''
    suma_grupos =[]
    for capa,i in zip(capas_salidas,range(1,len(capas_salidas)+1)):
        operacion = 'tp_'+capa+'=('+capa+'@PERMANENT <=11)*'+str(i)

        print (operacion)
        
        gscript.run_command('r.mapcalc',

                            overwrite=True,

                            expression=operacion)


        gscript.run_command('r.null',



                            map='tp_'+capa+'@PERMANENT',



                            null=0)

        

        suma_grupos.append('tp_'+capa+'@PERMANENT')

     

    ecuacion = ' + '.join(suma_grupos)
     



    gscript.run_command('r.mapcalc',



                            overwrite=True,



                            expression='grupos='+ecuacion)



    

    gscript.run_command('r.null',



                            map='grupos'+'@PERMANENT',



                            setnull=0)

    
    '''
    gscript.run_command('r.out.gdal',flags='cm',



                        overwrite=True,



                        input='grupos'+'@PERMANENT',



                        format='GTiff',



                        output=path_salida+'grupos.tif',



                        type='Byte')'''





    for capa,i in zip(capas_salidas,range(1,len(capas_salidas)+1)):



        gscript.run_command('r.null',



                            map='tp_'+capa+'@PERMANENT',



                            setnull=0)




    
def promedios_grupos(capas,ruta):



    inputs = ",".join(capas)



    gscript.run_command('r.stats',flags='An',



                    input=inputs,



                    separator='comma',



                    overwrite=True,



                    output=ruta+'promedios_grupos.csv')




def aplicar_mascara(mascaras,capas):

    insumos_con_mascara_a = []

    insumos_con_mascara_b = []

    for mascara in mascaras:

        for capa in capas:

           nombre_c = mascara+'_'+capa.split('@')[0]

           ecuacion = nombre_c+' = '+mascara+'@PERMANENT * '+capa

           gscript.run_command('r.mapcalc',

                            overwrite=True,

                            expression=ecuacion)

           if mascara[-1]=='a':

                insumos_con_mascara_a.append(nombre_c+'@PERMANENT')

           elif mascara[-1]=='b':

                insumos_con_mascara_b.append(nombre_c+'@PERMANENT')

    return insumos_con_mascara_a,insumos_con_mascara_b

def main():

    ruta = 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/pca/prueba_julio/'



    
    
    ruta = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_aptitud/politetico_divisivo/grass/grupos_100m_2_jul_v2/'
    capas = [
    'acuacultura_dulce_n@PERMANENT',
    'acuacultura_salobre_n@PERMANENT',
    'agricultura_n@PERMANENT',
    'apicultura_n@PERMANENT',
    'bovino_n@PERMANENT',
    'conservacion_n@PERMANENT',
    'energia_n@PERMANENT',
    'forestal_n@PERMANENT',
    'industrial_n@PERMANENT',
    'milpa_maya_n@PERMANENT',
    'mineria_n@PERMANENT',
    'pesca_n@PERMANENT',
    'porcino_avicola_n@PERMANENT',
    'tur_naturaleza_n@PERMANENT',
    'tur_sol_playa_n@PERMANENT',
    'urbano_n@PERMANENT']
    
    nombre_pca='pca1'
    capas_input = capas_i(capas)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    #eliminar_pca2end(capas,nombre_pca)
    data = stadistica(capa_pca,ruta)
    corte =getPuntoDeCorte(data,11)
    print(nombre_pca,"corte en ",corte)
    mascaras = separar_pca(capa_pca,corte)#6
    insumos_a,insumos_b = aplicar_mascara(mascaras,capas)

    
    # corte a

    nombre_pca = 'pca1a'
    capas_input = capas_i(insumos_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    #eliminar_pca2end(capas,nombre_pca)
    data = stadistica(capa_pca,ruta)
    corte =getPuntoDeCorte(data,11)
    print(nombre_pca,"corte en ",corte)
    mascaras = separar_pca(capa_pca,corte) #4
    insumos_a_a,insumos_a_b = aplicar_mascara(mascaras,capas)



    #### --- INICIA BLOQUE IZQUIERDO  ----####
    nombre_pca = 'pca1aa'
    capas_input = capas_i(insumos_a_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    #eliminar_pca2end(capas,nombre_pca)
    data = stadistica(capa_pca,ruta)
    if len(data)>0:
        corte =getPuntoDeCorte(data,11)
        print(nombre_pca,"corte en ",corte)
        mascaras = separar_pca(capa_pca,corte)
        insumos_a_a_a,insumos_a_a_b = aplicar_mascara(mascaras,capas)
        
        nombre_pca = 'pca1aaa'
        capas_input = capas_i(insumos_a_a_a)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) #4
            insumos_a_a_a_a,insumos_a_a_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1aaaa'
            capas_input = capas_i(insumos_a_a_a_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_a_a_a_a_a,insumos_a_a_a_a_b = aplicar_mascara(mascaras,capas)
            
            nombre_pca = 'pca1aaab'
            capas_input = capas_i(insumos_a_a_a_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #stadistica(capa_pca,ruta)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_a_a_a_b_a,insumos_a_a_a_b_b = aplicar_mascara(mascaras,capas)
        else:
            print ("se pudo cortar hasta",nombre_pca)


        nombre_pca = 'pca1aab'  #ver linea 417
        capas_input = capas_i(insumos_a_a_b)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) 
            insumos_a_a_b_a,insumos_a_a_b_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1aaba'
            capas_input = capas_i(insumos_a_a_b_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_a_a_b_a_a,insumos_a_a_b_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1aabb'
            capas_input = capas_i(insumos_a_a_b_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_a_a_b_b_a,insumos_a_a_b_b_b = aplicar_mascara(mascaras,capas)
        else:
            print ("se pudo cortar hasta",nombre_pca)
    else:
        print ("se pudo cortar hasta",nombre_pca)
    #### --- TERMINA BLOQUE IZQUIERDO  ----####
    #### --- INICIA BLOQUE DERECHO  ----####

    nombre_pca = 'pca1ab'  
    capas_input = capas_i(insumos_a_b) #ver linea  
    capa_pca= pca(capas_input,nombre_pca,ruta)
    #eliminar_pca2end(capas,nombre_pca)
    data = stadistica(capa_pca,ruta)
    if len(data)>0:
        corte =getPuntoDeCorte(data,11)
        print(nombre_pca,"corte en ",corte)
        mascaras = separar_pca(capa_pca,corte)
        
        insumos_a_b_a,insumos_a_b_b = aplicar_mascara(mascaras,capas)

        nombre_pca = 'pca1aba'
        capas_input = capas_i(insumos_a_b_a)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) #4
            insumos_a_b_a_a,insumos_a_b_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1abaa'
            capas_input = capas_i(insumos_a_b_a_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte)
            # insumos_a_b_a_a_a,insumos_a_b_a_a_b = aplicar_mascara(mascaras,capas)
            
            nombre_pca = 'pca1abab'
            capas_input = capas_i(insumos_a_b_a_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) 
            # insumos_a_b_a_b_a,insumos_a_b_a_b_b = aplicar_mascara(mascaras,capas)
        else:
            print("se pudo cortar hasta",nombre_pca)

        
        nombre_pca = 'pca1abb'  #ver linea 490
        capas_input = capas_i(insumos_a_b_b)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) #4
            insumos_a_b_b_a,insumos_a_b_b_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1abba'
            capas_input = capas_i(insumos_a_b_b_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            ##eliminar_pca2end(capas,nombre_pca)
            #data = stadistica(capa_pca,ruta)
            #corte = getPuntoDeCorte(data,11)
            #print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_a_b_b_a_a,insumos_a_b_b_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1abbb'
            capas_input = capas_i(insumos_a_b_b_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) 
            # insumos_a_b_b_b_a,insumos_a_b_b_b_b = aplicar_mascara(mascaras,capas)
        else:
            print("se pudo cortar hasta",nombre_pca)
    else:
        print("se pudo cortar hasta",nombre_pca)
    
    ######--- COMIENZA CORTE 1B ----###

    nombre_pca = 'pca1b'  # nombre del corte superior
    capas_input = capas_i(insumos_b) # capas de los insumos recortadas 
    capa_pca= pca(capas_input,nombre_pca,ruta)  # genera el pca para los insumos anteriores 
    #eliminar_pca2end(capas,nombre_pca) ## elimina los pca 2 al n
    data = stadistica(capa_pca,ruta) # calcula el histograma y lo regresa en forma de lista
    corte =getPuntoDeCorte(data,11) # regresa el intervalo que sera el corte
    print(nombre_pca,"corte en ",corte)
    mascaras = separar_pca(capa_pca,corte)#5   ## separa el pca dado el numero de corte
    insumos_b_a,insumos_b_b = aplicar_mascara(mascaras,capas) #aplica las mascaras a los inumos  y los separa para el siguiente paso


    #### --- INICIA BLOQUE IZQUIERDO  ----####
    nombre_pca = 'pca1ba' 
    capas_input = capas_i(insumos_b_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    #eliminar_pca2end(capas,nombre_pca)
    data = stadistica(capa_pca,ruta)
    if len(data)>0:
        corte =getPuntoDeCorte(data,11)
        print(nombre_pca,"corte en ",corte)
        mascaras = separar_pca(capa_pca,corte) #6
        insumos_b_a_a,insumos_b_a_b = aplicar_mascara(mascaras,capas)

        nombre_pca = 'pca1baa'
        capas_input = capas_i(insumos_b_a_a)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) #4
            insumos_b_a_a_a,insumos_b_a_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1baaa'
            capas_input = capas_i(insumos_b_a_a_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_b_a_a_a_a,insumos_b_a_a_a_b = aplicar_mascara(mascaras,capas)
            
            nombre_pca = 'pca1baab'
            capas_input = capas_i(insumos_b_a_a_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # stadistica(capa_pca,ruta)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_b_a_a_b_a,insumos_b_a_a_b_b = aplicar_mascara(mascaras,capas)
        else:
            print("se pudo cortar hasta:",nombre_pca)

        nombre_pca = 'pca1bab'  #ver linea 417
        capas_input = capas_i(insumos_b_a_b)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            mascaras = separar_pca(capa_pca,corte) #4
            print(nombre_pca,"corte en ",corte)
            insumos_b_a_b_a,insumos_b_a_b_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1baba'
            capas_input = capas_i(insumos_b_a_b_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_b_a_b_a_a,insumos_b_a_b_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1babb'
            capas_input = capas_i(insumos_b_a_b_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_b_a_b_b_a,insumos_b_a_b_b_b = aplicar_mascara(mascaras,capas)
        else:
            print("se pudo cortar hasta:",nombre_pca)
    else:
        print ("se pudo cortar hasta",nombre_pca)
    
    #### --- TERMINA BLOQUE IZQUIERDO  ----####
    #### --- INICIA BLOQUE DERECHO  ----####
    nombre_pca = 'pca1bb'  
    capas_input = capas_i(insumos_b_b) #ver linea 406 
    capa_pca= pca(capas_input,nombre_pca,ruta)
    #eliminar_pca2end(capas,nombre_pca)
    data = stadistica(capa_pca,ruta)
    if len(data)>0:
        corte =getPuntoDeCorte(data,11)
        print(nombre_pca,"corte en ",corte)
        mascaras = separar_pca(capa_pca,corte) 
        insumos_b_b_a,insumos_b_b_b = aplicar_mascara(mascaras,capas)

        nombre_pca = 'pca1bba'
        capas_input = capas_i(insumos_b_b_a)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) #4
            insumos_b_b_a_a,insumos_b_b_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1bbaa'
            capas_input = capas_i(insumos_b_b_a_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte)
            # insumos_b_b_a_a_a,insumos_b_b_a_a_b = aplicar_mascara(mascaras,capas)
            
            nombre_pca = 'pca1bbab'
            capas_input = capas_i(insumos_b_b_a_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # stadistica(capa_pca,ruta)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) 
            # insumos_b_b_a_b_a,insumos_b_b_a_b_b = aplicar_mascara(mascaras,capas)
        else:
            print("se pudo cortar hasta",nombre_pca)
    

        nombre_pca = 'pca1bbb'  #ver linea 490
        capas_input = capas_i(insumos_b_b_b)
        capa_pca= pca(capas_input,nombre_pca,ruta)
        #eliminar_pca2end(capas,nombre_pca)
        data = stadistica(capa_pca,ruta)
        if len(data)>0:
            corte = getPuntoDeCorte(data,11)
            print(nombre_pca,"corte en ",corte)
            mascaras = separar_pca(capa_pca,corte) #4
            insumos_b_b_b_a,insumos_b_b_b_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1bbba'
            capas_input = capas_i(insumos_b_b_b_a)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) #7
            # insumos_b_b_b_a_a,insumos_b_b_b_a_b = aplicar_mascara(mascaras,capas)

            nombre_pca = 'pca1bbbb'
            capas_input = capas_i(insumos_b_b_b_b)
            capa_pca= pca(capas_input,nombre_pca,ruta)
            # #eliminar_pca2end(capas,nombre_pca)
            # data = stadistica(capa_pca,ruta)
            # corte = getPuntoDeCorte(data,11)
            # print(nombre_pca,"corte en ",corte)
            # mascaras = separar_pca(capa_pca,corte) 
            # insumos_b_b_b_b_a,insumos_b_b_b_b_b = aplicar_mascara(mascaras,capas)
        else:
            print("se pudo cortar hasta",nombre_pca)
    else:
        print("se pudo cortar hasta",nombre_pca)




    
    insumos_grupos= ['pca1aaaa.1',
                    'pca1aaab.1',
                    'pca1aaba.1',
                    'pca1aabb.1',
                    'pca1abaa.1',
                    'pca1abab.1',
                    'pca1abba.1',
                    'pca1abbb.1',
                    'pca1baaa.1',
                    'pca1baab.1',
                    'pca1baba.1',
                    'pca1babb.1',
                    'pca1bbaa.1',
                    'pca1bbab.1',
                    'pca1bbba.1',
                    'pca1bbbb.1']

    #capa_grupos(insumos_grupos,ruta)



    

    insumos = ['grupos@PERMANENT']



    for i in capas:

        insumos.append(i)



    #promedios_grupos(insumos,ruta)

    
                        

if __name__ == '__main__':
    main()
