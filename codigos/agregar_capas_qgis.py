def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa
def ordena_lista_shp(lista_shp):
    lista_preordenada =[]
    for capa in lista_shp:    
        lista_preordenada.append(capa.split("/")[-1].split(".")[0])
    lista_ordenada=sorted(lista_preordenada,reverse = True)
    paths_ordenados=[]
    for ordenada in lista_ordenada:
        for capa in lista_shp:
            if ordenada == capa.split("/")[-1].split(".")[0]:
                paths_ordenados.append(capa)
    return paths_ordenados

def cargar_capa(path_shape):
    nombre = nombre_capa(path_shape).split(".")[0]
    layer = QgsRasterLayer(path_shape, nombre)
    QgsProject.instance().addMapLayer(layer)

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
                                                                                                                'criterios':{'entidades_protectoras':{'w':0.84,'ruta':p_sig_res + 'biologica/serv_ambientales/prot_costera_yuc/fv_entidades_protectoras.tif'},
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
   cargar_capa(path_criterio)