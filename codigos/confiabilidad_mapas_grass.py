#!/usr/bin/env python3
##DATOS ACTUALIZADOS NOVIEMBRE 2020


import grass.script as gscript
import pandas as pd 




def lista_criterios(dicc):

    '''

    Esta funcion regresa una lista de los criterios de un diccionario



    :param dicc: Diccionario que contiene nombres, rutas y pesos para el

    analisis de vulnerabilidad / sensibilidad

    :type dicc: diccionario python

    '''

    criterios = []

    for k1,v1 in dicc.items():

        for k2,v2, in v1['criterios'].items():

            elementos = list(v2.keys())

            if 'ruta' in elementos:

                criterios.append(k2+"|"+v2['ruta'])

            if 'criterios' in elementos:

                for k3,v3, in v2['criterios'].items():

                    elementos = list(v3.keys())

                    if 'ruta' in elementos:

                        criterios.append(k3+"|"+v3['ruta'])

                    if 'criterios' in elementos:

                        for k4,v4, in v3['criterios'].items():

                            elementos = list(v4.keys())

                            if 'ruta' in elementos:

                                criterios.append(k4+"|"+v4['ruta'])

                            if 'criterios' in elementos:

                                for k5,v5, in v4['criterios'].items():

                                    elementos = list(v5.keys())

                                    if 'ruta' in elementos:

                                        criterios.append(k5+"|"+v5['ruta'])

                        

    return criterios

def elimina_capa(nombre):




    gscript.run_command('g.remove',

                            name=nombre,

                            type='raster',

                            overwrite=True,

                            flags='f'

                            )


def importa_capa_raster(path_r,nombre):



    gscript.run_command('r.import',

                        input=path_r,

                        output=nombre,

                        overwrite=True,

                        )


def genera_condicional_menor(criterio,v_prom,capa_clasificada,categoria):







    gscript.run_command('r.mapcalc',



                        expression="condicional_menor = if("+criterio+"<"+str(v_prom)+"&&"+capa_clasificada+'=='+str(categoria)+",1)",



                        overwrite=True)


def genera_condicional_mayor(criterio,v_prom,capa_clasificada,categoria):



    gscript.run_command('r.mapcalc',

                        expression="condicional_mayor = if("+criterio+">"+str(v_prom)+"&&"+capa_clasificada+'=='+str(categoria)+",1)",

                        overwrite=True)

def conteo_celdas(condicional):

    datos = gscript.pipe_command('r.stats',flags="cn",input=condicional,separator='comma')



    data = []

    for line in datos.stdout:

       data.append(str(line).replace("\\r\\n","").replace("b","").replace("'",""))

    if len(data)>1:

        no_pixeles = str(data[1]).split(",")

       

        if no_pixeles[0]=='1':

            #print (no_pixeles[1])

            return int(no_pixeles[1])

    else:

        print ("la condicional no se cumplio")

        return 0


def main():

    p_sig = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/'

    #INSUMOS

    p_sig_exp= 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/exposicion/'

    p_sig_sens= 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/susceptibilidad/'

    p_sig_res= 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/resiliencia/'



    dicc = {
    'exposicion': {'w':0.33,
                        'criterios':{'biologico':{'w':0.50,
                                                        'criterios':{'v_acuatica_exp':{'w':0.16,'ruta':p_sig_exp+'biologica/v_acuatica_yuc/fv_v_acuatica_yuc_100m.tif'},
                                                                        'v_costera_exp':{ 'w':0.84,
                                                                                            'criterios':{'distancia_manglar_exp':{'w':0.75,'ruta':p_sig_exp + 'biologica/v_costera_yuc/fv_distancia_manglar_yuc_100m.tif'},
                                                                                                        'distancia_dunas_exp':{'w':0.25,'ruta':p_sig_exp + 'biologica/v_costera_yuc/fv_distancia_dunas_yuc_100m.tif'}}}}},
                                        'fisico':{'w':0.50,
                                                    'criterios':{'elevacion_exp':{ 'w':0.87,'ruta':p_sig_exp+ 'fisica/elev_yuc/fv_elevacion_yuc_100m.tif'},
                                                                    'ancho_playa_exp':{'w':0.13,'ruta':p_sig_exp+ 'fisica/ancho_playa_yuc/fv_distancia_playa_yuc_100m.tif'}
                                                                }
                                                }
                                    }
                    },
    'susceptibilidad': {'w':0.33,
                            'criterios':{'biologico':{'w':0.50 ,
                                                            'criterios':{'v_costera_sus':{ 'w':1.0,'ruta':p_sig_sens + 'biologica/v_costera_yuc/fv_v_costera_presencia_yuc_100m.tif'}}},
                                            'fisico':{'w':0.50,
                                                        'criterios':{'elevacion_sus':{ 'w':0.26,'ruta':p_sig_sens + 'fisica/elev_yuc/fv_elevacion_yuc_100m.tif' },
                                                                        'duna_costera_sus':{'w':0.10,'ruta':p_sig_sens + 'fisica/duna_yuc/fv_duna_yuc_100m.tif'},
                                                                        'tipo_litoral_sus':{'w':0.64,'ruta':p_sig_sens + 'fisica/t_litoral_yuc/fv_tipo_litoral_yuc_100m_corregida.tif'}
                                                                    }
                                                    }
                                        }
                        },
    'resiliencia': {'w':0.33,
                            'criterios':{'biologico':{'w':0.50 ,
                                                            'criterios':{'biodiversidad_res':{'w':0.50,'ruta':p_sig_res + 'biologica/biodiversidad/fv_biodiversidad_yuc_100m.tif'},
                                                                        'servicios_ambientales_res':{'w':0.50,
                                                                            'criterios':{'proteccion_costera_res':{'w':0.75,
                                                                                                                'criterios':{'entidades_protectoras_res':{'w':0.84,'ruta':p_sig_res + 'biologica/serv_ambientales/prot_costera_yuc/fv_entidades_protectoras.tif'},
                                                                                                                                #'criterios':{'dunas_costeras_res':{'w':0.20,'ruta':p_sig_res + 'biologica/serv_ambientales/prot_costera_yuc/fv_dunas_presencia_yuc_100m.tif'},
                                                                                                                                #            'manglar_res':{'w':1.00,'ruta':p_sig_res + 'biologica/serv_ambientales/prot_costera_yuc/fv_manglar_presencia_yuc_100m.tif'},
                                                                                                                                #            }},
                                                                                                                            'v_acuatica_res':{'w':0.16,'ruta':p_sig_res + 'biologica/serv_ambientales/prot_costera_yuc/fv_v_acuatica_yuc_100m.tif'}
                                                                                                                            }
                                                                                                                    },
                                                                                        'provision_res':{'w':0.25,'ruta':p_sig_res + 'biologica/serv_ambientales/provision_yuc/fv_provision_yuc_100m.tif'}}
                                                                                                    }
                                                                        }
                                                    },
                                        'fisico':{'w':0.50,
                                                        'criterios':{'elevacion_res':{'w':0.60,'ruta':p_sig_res + 'fisica/elev_yuc/fv_elev_yuc.tif'},
                                                                    'tipo_litoral_res':{'w':0.40,'ruta':p_sig_res + 'fisica/t_litoral_yuc/fv_tipo_litoral_yuc.tif'}
                                                                    }
                                                }
                                        }
                    }

    }
    
    
    criterios = lista_criterios(dicc)

    nombre_criterios=[]

    ruta_criterios = []

    for criterio in criterios:

       n_criterio = criterio.split("|")[0]

       path_criterio = criterio.split("|")[1]

       importa_capa_raster(path_criterio,n_criterio)
       #elimina_capa(n_criterio+'@PERMANENT')

    '''
    #Clasificaciones

    p_clasificaciones = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/vulnerabilidad_costera/vuln_con_tipolitoral_corregida/clasificaciones/'
    factores_vulnerabilidad = ['exposicion','resiliencia','susceptibilidad']

    factores_progresion=['1_3','1_5','1_7','2_0']

    nombres_clasificaciones = []

    for factor in factores_vulnerabilidad:

        for fp in factores_progresion:

            nombre_clasificacion = factor+"_yuc_"+"wf_"+fp+"_5cats"

            ruta_clasificacion = p_clasificaciones+nombre_clasificacion+".tif"

            importa_capa_raster(ruta_clasificacion,nombre_clasificacion)
            #elimina_capa(nombre_clasificacion+'@PERMANENT')
            nombres_clasificaciones.append(nombre_clasificacion)

    
    
    factor_progresion =['1_3','1_5','1_7','2_0']
    for fp in factor_progresion:

        factor_v ='exposicion'

        cat = '5'

        factor_vulne = factor_v+'_yuc_'

        wf= 'wf_'+fp+'_5cats'

        mapa_categorias = factor_vulne+wf



        

        csv_nuevos_promedios = p_sig +'procesamiento/vulnerabilidad_costera/sensibilidad_tau/'+factor_v+'/cat_'+cat+'/bd_'+factor_v[0:3]+'_nueva_fv_prom_'+fp+'.csv'

        nuevos_promedios = pd.read_csv(csv_nuevos_promedios)

        campos = nuevos_promedios.columns[2:]

        campos_nuevos = [x.replace("mean_","") for x in campos]

        renombre={a:b for a,b in zip(campos,campos_nuevos)}

        umbrales= nuevos_promedios.rename(columns=renombre,errors='raise')

        modifica_umbrales = umbrales.copy(deep=False)

        criterios = umbrales.columns[2:]

        for criterio in criterios:

            #print (criterio)

            for i in umbrales[criterio].items():

                cambio_de =umbrales['cambio_de'][i[0]]

                cambio_a =umbrales['cambio_a'][i[0]]

                umbral = i[1]

                #print (cambio_de, cambio_a, umbral)

                if umbral ==-9999:

                    modifica_umbrales[criterio][i[0]]=-9999

                else:

                    categoria = cambio_de

                    genera_condicional_mayor(criterio+'@PERMANENT',umbral,mapa_categorias+'@PERMANENT',categoria)

                    mayor = conteo_celdas('condicional_mayor@PERMANENT')

                    modifica_umbrales[criterio][i[0]]=mayor

        campos_pixeles = ['pixeles_'+x for x in campos_nuevos]

        renombre_pix={a:b for a,b in zip(campos_nuevos,campos_pixeles)}

        salida= modifica_umbrales.rename(columns=renombre_pix,errors='raise')

        salida.to_csv(csv_nuevos_promedios.split(".")[0]+"_nopixeles_mayores.csv",index=False)

    



     ### Proceso manual para la consulta## 
    #criterio = 'distancia_manglar_exp'#'elevacion_exp'#'distancia_manglar_exp'
    #criterio = 'v_costera_sus'#'tipo_litoral_sus'#'elevacion_sus'#'v_costera_sus'
    criterio = 'ancho_playa_res' #'provision_yuc'#'manglar_res'#'biodiversidad_res'#'duna_costera_res'#'ancho_playa_res'#'v_acuatica_res'#'dunas_costeras_res'

    #factor_vulne = 'exposicion_yuc_'

    #factor_vulne = 'susceptibilidad_yuc_'

    factor_vulne = 'resiliencia_yuc_'

    wf= 'wf_2_0_5cats'

    mapa_categorias = factor_vulne+wf

    categoria = 3

    vnp = 0.481

    
    genera_condicional_mayor(criterio+'@PERMANENT',vnp,mapa_categorias+'@PERMANENT',categoria)

    genera_condicional_menor(criterio+'@PERMANENT',vnp,mapa_categorias+'@PERMANENT',categoria)

    mayor = conteo_celdas('condicional_mayor@PERMANENT')

    menor = conteo_celdas('condicional_menor@PERMANENT')
   
    print(' Existen ',menor," pixeles menor que ", vnp)

    #print(' Existen ',mayor," pixeles mayor que ", vnp)

    '''
if __name__ == '__main__':
    main()






    