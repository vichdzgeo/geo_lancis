import grass.script as gscript
import pandas as pd 


def elimina_capa(nombre):
    gscript.run_command('g.remove',
                            name=nombre,
                            type='raster',
                            overwrite=True,
                            flags='f')
def importa_capa_raster(path_r,nombre):
    gscript.run_command('r.import',
                        input=path_r,
                        output=nombre,
                        overwrite=True,
                        )
def calculadora_mapas(criterio,v_prom,capa_clasificada,categoria):
    gscript.run_command('r.mapcalc',
                        expression=ecuacion,
                        overwrite=True)


#### FUNCIONES PARA ANALISIS DE COMBINACION LINEAL PONDERADA  Y ANALISIS DE SENSIBLIDAD

def ecuacion_clp(lista):
    parametros = []
    for l in lista:
        parametros.append(str(l[0])+'*'+l[1])
    return  " + ".join(parametros)

def lista_criterios(dicc):
    '''

    Esta funcion regresa una lista de los criterios de un diccionario
    :param dicc: Diccionario que contiene nombres, rutas y pesos para el
    analisis de vulnerabilidad / sensibilidad
    :type dicc: diccionario python
    '''

    criterios = []
    for k1,v1 in dicc.items():
        for k2,v2 in v1['criterios'].items():
            elementos = list(v2.keys())
            if 'ruta' in elementos:
                criterios.append(k2+"|"+v2['ruta'])
            if 'criterios' in elementos:
                for k3,v3 in v2['criterios'].items():
                    elementos = list(v3.keys())
                    if 'ruta' in elementos:
                        criterios.append(k3+"|"+v3['ruta'])
                    if 'criterios' in elementos:
                        for k4,v4 in v3['criterios'].items():
                            elementos = list(v4.keys())
                            if 'ruta' in elementos:
                                criterios.append(k4+"|"+v4['ruta'])
                            if 'criterios' in elementos:
                                for k5,v5 in v4['criterios'].items():
                                    elementos = list(v5.keys())
                                    if 'ruta' in elementos:
                                        criterios.append(k5+"|"+v5['ruta'])
                                    if 'criterios' in elementos:
                                        for k6,v6 in v5['criterios'].items():
                                            elementos = list(v6.keys())
                                            if 'ruta' in elementos:
                                                criterios.append(k6+"|"+v6['ruta'])



    return criterios




