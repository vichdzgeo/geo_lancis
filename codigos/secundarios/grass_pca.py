#!/usr/bin/env python3

import grass.script as gscript


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
    '''
    numero = len(capas)

    for i in range(2,numero+1):

        gscript.run_command('g.remove',flags='f',

                        type='raster',

                        name=nombre_pca+'.'+str(i)+'@PERMANENT')

      '''                  

        

def stadistica (capa,ruta):

    gscript.run_command('r.stats',flags='cn',

                    input=capa+'@PERMANENT',

                    separator='comma',

                    overwrite=True,

                    output=ruta+capa.replace('.1','')+'.csv')

                    

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

    ruta = 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/pca/'



    
    #gscript.run_command('g.region', flags='p')
    capas = ['x372_06RY_CC_100m@PERMANENT',
             'x372_09RY_DE_100m@PERMANENT',
             'x372_25RY_HIDR_100m@PERMANENT',
              'x372_34RY_CP_100m@PERMANENT']
    '''
    nombre_pca='pca1'
    capas_input = capas_i(capas)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    mascaras = separar_pca(capa_pca,6)
    insumos_a,insumos_b = aplicar_mascara(mascaras,capas)



    #segundo corte a

    nombre_pca = 'pca1a'
    capas_input = capas_i(insumos_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    mascaras = separar_pca(capa_pca,4)
    insumos_a_a,insumos_a_b = aplicar_mascara(mascaras,capas)

    nombre_pca = 'pca1aa'
    capas_input = capas_i(insumos_a_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)


    nombre_pca = 'pca1ab'
    capas_input = capas_i(insumos_a_b)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)


    #segundo corte b

    nombre_pca = 'pca1b'
    capas_input = capas_i(insumos_b)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    mascaras = separar_pca(capa_pca,5)
    insumos_b_a,insumos_b_b = aplicar_mascara(mascaras,capas)


    nombre_pca = 'pca1ba'
    capas_input = capas_i(insumos_b_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    mascaras = separar_pca(capa_pca,6)
    insumos_b_a_a,insumos_b_a_b = aplicar_mascara(mascaras,capas)


    nombre_pca = 'pca1bb'
    capas_input = capas_i(insumos_b_b)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)

    nombre_pca = 'pca1baa'
    capas_input = capas_i(insumos_b_a_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    mascaras = separar_pca(capa_pca,4)
    insumos_b_a_a_a,insumos_b_a_a_b = aplicar_mascara(mascaras,capas)

    nombre_pca = 'pca1bab'
    capas_input = capas_i(insumos_b_a_b)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)

    # tercer corte 
    nombre_pca = 'pca1baaa'
    capas_input = capas_i(insumos_b_a_a_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    mascaras = separar_pca(capa_pca,7)

    insumos_b_a_a_a_a,insumos_b_a_a_a_b = aplicar_mascara(mascaras,capas)
    nombre_pca = 'pca1baab'
    capas_input = capas_i(insumos_b_a_a_b)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    
    nombre_pca = 'pca1baaaa'
    capas_input = capas_i(insumos_b_a_a_a_a)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)

    nombre_pca = 'pca1baaab'
    capas_input = capas_i(insumos_b_a_a_a_b)
    capa_pca= pca(capas_input,nombre_pca,ruta)
    eliminar_pca2end(capas,nombre_pca)
    stadistica(capa_pca,ruta)
    '''

    insumos_grupos= ['pca1a.1',

                   'pca1bb.1',

                   'pca1bab.1',

                   'pca1baab.1',

                   'pca1baaaa.1',

                   'pca1baaab.1']

    capa_grupos(insumos_grupos,ruta)



    

    insumos = ['grupos@PERMANENT']



    for i in capas:

        insumos.append(i)



    promedios_grupos(insumos,ruta)

    
                        

if __name__ == '__main__':
    main()
