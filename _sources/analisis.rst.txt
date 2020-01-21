Analisis de sensibilidad
#############################

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Aliquam at turpis lacus. Pellentesque vitae efficitur lacus. 
Proin eu lectus ultrices mauris viverra vehicula. Proin ante justo, 
ultrices eu leo ac, vulputate tristique sapien. Aenean vel enim a elit mollis commodo. 
Proin laoreet quis quam quis auctor. Vestibulum nec nisl pretium, bibendum ligula in, 
suscipit neque. Nunc placerat ac ipsum vel pellentesque. Phasellus lacinia cursus porttitor. 
Donec viverra faucibus nisl, non vestibulum quam posuere sit amet. Nulla a sodales urna. 
Donec vestibulum purus purus, iaculis pellentesque eros cursus quis. Maecenas ac maximus sem.


Entrada de datos
*******************

El usuario debe reemplazar en el código las variables como pesos **w**,
nombre de los criterios, y  la **ruta** de donde se encuentran las capas
raster.


Salida de datos
******************

la variable **p_procesamiento** indica la ruta donde se escribirán las 
capas integradas y el archivo csv que contendrá el análisis de sensibilidad

.. code-block:: python

    dicc = {
        'criterio_A': {'w':0.5,
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


.. automodule:: sensibilidad
    :members: