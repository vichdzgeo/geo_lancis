OWA
#############################

descarga el código de ejemplo 

:download:`owa_raster.py <../../codigos/owa_raster.py>`.


Requerimientos generales 
--------------------------

Para asegurar la ejeución correcta del código es importante 
garantizar la instalación y funcionamiento de los siguientes elementos:


- Qgis y librerias de Osgeo4W 3.4 o superior
- librerias python:
 - Numpy
 - Pandas
 - GDAL
 - reduce

Requerimientos generales de los insumos
----------------------------------------

Es importante que todas las capas raster cumplan con las siguientes condiciones


- Misma proyección cartográfica
- Mismo tamaño de pixel
- Misma extensión de capa



Ejemplo
------------

Insumos 
========

Descarga los insumos para este ejemplo :download:`aqui <>`

Procedimiento
==============

1. Abre el código
*****************

Abre el código **owa_raster.py** en Qgis 3.4 o superior, 
Si tienes dudas de como hacerlo visualiza la guia_

.. _guia: https://vichdzgeo.github.io/geo_lancis/ejecucion.html

.. image:: ../../owa/images/codigo.PNG

2. Rellena el diccionario
********************************

Las capas raster de entrada y sus respectivos pesos son ingresados
a la función mediante un diccionario, es importante seguir la 
estructura como el siguiente ejemplo:

.. code-block:: python

     dicc_capas = {'capa_1':{'ruta':path_insumos +"biologica/v_acuatica_yuc/fv_v_acuatica_yuc.tif",'w':0.08},
             'capa_2':{'ruta':path_insumos +"biologica/v_costera_yuc/fv_v_costera_distancia_yuc.tif",'w':0.42},
             'capa_3':{'ruta':path_insumos +"fisica/ancho_playa_yuc/fv_distancia_playa_yuc.tif",'w':0.065},
             'capa_4':{'ruta':path_insumos +"fisica/elev_yuc/fv_elevacion_yuc.tif",'w':0.435},
             }

Dónde:

- **capa_#**:  corresponde a la capa conforme van agregandose al diccionario,

- **ruta** : Corresponde a la ruta o path del la capa raster

- **w** : Corresponde al peso asociado a esa capa o criterio

.. note::

    Si desea agregar una capa adicional la línea quedaria de la siguiente forma,
    donde se tiene que agregar el consecutivo a la llave de la capa, en este caso
    capa_5.

    'capa_5':{'ruta':path_tiff,'w':#.###},
    }

3. Indica la capa maestra
***************************

El código transforma los datos tiff en arreglos matriciales
es por ello que se requiere asociar cualquier capa de los insumos
a la variable **path_capa_maestra**, una vez calculado 
owa para cierto alpha, el arreglo matricial tiene que transformarse
en un archivo tiff

.. code-block:: python

    path_capa_maestra = "../../*.tif"


4. Declara el EPGS
***********************

Es el código de referencia geoespacial que Indica
la proyección y el datum asociados a la capa, este código
tiene que ser el mismo de los insumos, declara el código 
en la variable **EPSG** 

.. code-block:: python

    EPSG = 32616

5. Indica el direcctorio de salida
*************************************

El código genera una capa para cada alpha dado, estos
son nombrados automaticamente con el valor del alpha,
es por ello que solo se tiene que indicar el directorio de
salida.

.. code-block:: python

    path_salida = "../../"

6. Verifica las variables asociadas a la funcion **insumos_base**
*******************************************************************

la función **insumos_base** recibe como parametro el diccionario
de capas y pesos, es por ello que tienes que asegurarte de que el
nombre del diccionario coincida con el que recibe la función.

Esta función regresa una lista de dataframes de las capas y una lista 
de pesos, por default se llaman **capas** y **w** respectivamente

.. code-block:: python

    capas, w = insumos_base(dicc_capas)


7. Indica los valores de alpha
******************************************
El código esta programado para recibir una 
lista de valores de alpha y con ella, generar 
un mapa por cada alpha declarado en dicha lista.
los valores de alpha son declarados en la variable
**owa_alphas**.

.. code-block:: python

    owa_alphas = [0.0001,0.1,0.5,1.0,2.0,10.0,1000.0]


8. Verificar que todo este correcto en la función genera_owa
**************************************************************

La función **genera_owa** es la encargada de recibir 
las variables declaradas 


.. code-block:: python

    genera_owa(capas,w,owa_alphas,path_capa_maestra,EPSG,path_salida)


Documentación dentro del código
-----------------------------------


.. automodule:: owa_raster
    :members: