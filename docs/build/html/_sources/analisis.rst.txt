Análisis de sensibilidad
#############################

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Aliquam at turpis lacus. Pellentesque vitae efficitur lacus. 
Proin eu lectus ultrices mauris viverra vehicula. Proin ante justo, 
ultrices eu leo ac, vulputate tristique sapien. Aenean vel enim a elit mollis commodo. 
Proin laoreet quis quam quis auctor. Vestibulum nec nisl pretium, bibendum ligula in, 
suscipit neque. Nunc placerat ac ipsum vel pellentesque. Phasellus lacinia cursus porttitor. 
Donec viverra faucibus nisl, non vestibulum quam posuere sit amet. Nulla a sodales urna. 
Donec vestibulum purus purus, iaculis pellentesque eros cursus quis. Maecenas ac maximus sem.

descarga el código de ejemplo 

:download:`sensibilidad.py <../../codigos/sensibilidad.py>`.

Entrada de datos
*******************

El usuario debe reemplazar en el código las variables como pesos **w**,
nombre de los criterios, y  la **ruta** de donde se encuentran las capas
raster.


ver a partir de la línea 364 en el código de ejemplo

.. code-block:: python

    dicc = {
        'exposicion': {'w':0.5,
                            'criterios':{'biologico':{'w':0.50,
                                                            'criterios':{'v_acuatica':{'w':0.16,'ruta':''},
                                                                            'v_costera':{ 'w':0.84,'ruta':''}}},
                                            'fisico':{'w':0.50,
                                                        'criterios':{'elevacion':{ 'w':0.87,'ruta':''},
                                                                        'ancho_playa':{'w':0.13,'ruta':''}
        }}}},
        'susceptibilidad': {'w':0.5,
                                'criterios':{'biologico':{'w':0.50 ,
                                                                'criterios':{'v_costera':{ 'w':1.0,'ruta':''}}},
                                                'fisico':{'w':0.50,
                                                            'criterios':{'elevacion':{ 'w':0.26,''ruta':'' },
                                                                            'duna_costera':{'w':0.10,'ruta':''},
                                                                            'tipo_litoral':{'w':0.64,'ruta':''},
        }}}}
        
        }

Salida de datos
******************

la variable **p_procesamiento** indica la ruta donde se escribirán las 
capas integradas y el archivo csv que contendrá el análisis de sensibilidad


Ejemplo
*********


Insumos 
========

Descarga los insumos para este ejemplo  :download:`aqui <../../analisis_sensibilidad/insumos/insumos.zip>`


Procedimiento
================

Abre el código **sensibilidad.py** en Qgis 3.14 o superior, 
Si tienes dudas de como hacerlo visualiza la guia_

.. _guia: https://vichdzgeo.github.io/geo_lancis/ejecucion.html


Modificar las rutas donde se encuentran los insumos y 
elegir una carpeta en donde se escribiran los resultados 

.. image:: ../../analisis_sensibilidad/images/modificar_paths.PNG



El tiempo de ejecución del código en este ejemplo es de 10 minutos. 
al finalizar se mostrará la consola de la siguiente manera:

.. image:: ../../analisis_sensibilidad/images/fin_ejecucion.PNG


el archivo csv de salida que contiene los datos es el siguiente:

.. csv-table:: Analisis de sensibilidad
    :file: ../../analisis_sensibilidad/salida/sensibilidad_por_criterio.csv
    :header-rows: 1


Documentación del código
**************************

.. automodule:: sensibilidad
    :members: