import csv 
import operator
import pandas as pd

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
    return corte

def data_list(path_csv):
    with open(path_csv, newline='') as csvfile:
        stat_csv = csv.reader(csvfile, delimiter=',')
        line = []
        for row in stat_csv:
            line.append(','.join(row))
    return line 

ruta = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/procesamiento/analisis_aptitud/politetico_divisivo/grass/'
path_csv = ruta +'grupos_100m_sin_acu_pesca/pca1bab.csv'
datos = data_list(path_csv)
print('funcion lancis',getPuntoDeCorte(datos,11))
print('funcion modificada',getPuntoDeCorte2(datos))
