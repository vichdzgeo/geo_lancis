Cobertura de uso y tipo de suelo a nivel municipal
####################################################


Objetivo:

Generar bases de datos  a nivel municipal que cuantiquen el área en hectaréas por clase
de uso de suelo y vegetación

# Insumos 

- Series I - VI de uso de suelo y vegetacíón INEGI
- Municipios del estado de Yucatán (2018)



## Procedimiento

Se unificarón las categorias para las seis series publicadas de la siguiente manera:
(Solo aplica para el estado de Yúcatan)


id_clase - Categoria
1 - Agricultura de riego
2 -Agricultura de temporal
3 - Cuerpo de agua
4 - Manglar
5 - Pastizal
6 - Selva baja
7 - Selva mediana
8 - Sin vegetación
9 - Asentamiento humano
10 - Vegetación de duna costera
11 - Vegetación de petén
12 - Vegetación secundaria de selva baja
13 - Vegetación secundaria de selva mediana
14 - Vegetación secundaria de manglar
15 - Acuícola
16 - Bosque cultivado/Palmar inducido
17 - Tular
18 - Vegetación halófila hidrófila
19 - Sábana


Se genera el script **datos_nivel_municipio.py** el cual genera
realiza los siguientes pasos:

- Se declara **path_mun** la ruta de la capa de municipios 
- se realiza un iterador (for) del 1 al 6 para procesar las 6 series de USV
- Se declara **path_usv** mediante el for la ruta de la capa usv_serie_i_yuc.shp (donde i, va del 1 al 6)
- Se declara **path_mun_usv**  mendiante el for la ruta del archivo que resultará de la intersección de municipios y USV  (agregados)
- Se declara **path_mun_usv_csv** mediante el for la ruta del archivo csv que contendrá las áreas (Ha) por clase por municipio
- se declara **path_mun** como la capa **municipios**
- se declara **path_usv** como la cap **usv** 
- Se crea una copia de la capa de municipio 
- Se declara **path_interseccion**, mendiante el for que  es la ruta y nombre del resultado de la intersección de municipios y USV
- Se crea una lista municipios mendiante el campo **cve_mun** de la capa **municipios**
- Se crea una lista de las categorias mediante el campo **id_clase** de la capa **usv**
- Se realiza la intersección **path_mun_usv** y **path_usv** se indica la ruta y nombre de salida con **path_interseccion**
- se declara **path_mun_usv** como la capa **mun_usv**
- Se llama a la funcion **campos_clases** pasando como parametros la cap  **mun_usv** y la lista_clases, esta función creará los campos en la capa vectorial 
como "clase_i" donde i es el número de id de la clase
- se declara **path_interseccion** como la capa **consulta_intersect** 
- Se inicia la edición de la capa **mun_usv**
- se realiza un iterador (for) de la lista_clases
 - Se inicializa la variable area = 0
 - Se realiza un iterador (for) de la lista_mun
    - se restablece la variable area = 0
    - se realiza un filtro mediante una consulta por municipio y por numero de clase **request_mun**
    - se realiza un filtro mediante una consulta por municipio  **request_mun_o**
    - Se realiza un iterador (for) de los elementos de la capa **consulta_interect** pasando la consulta **request_mun**
        - Se realiza la suma de los elmentos de la seleccion mediante la funcion geometry().area() y se va guardando en **area**
    - Se realiza un iterdor (for) de los elementos de la capa **mun_usv**  pasando la consulta **request_mun**
        - Se escribe en el campo **clase_i** (donde i es el id de la clase) el valor del área dividido entre 10,000 y redondeado a 2 dígitos
    - Se actualizan los elementos de la capa **mun_usv**
- al finalizar la serie de iteradores se guardan los cambios en **mun_usv**
- Se manda a llamar a la función **vector_to_usv** donde se recibe como parametros la capa **mun_usv** y la variable **path_mun_usv_csv** que es la ruta y el nombre del archivo csv


al finalizar se obtiene

- 6 capas vectoriales a nivel municipal, una por serie **mun_usv_si.shp** (donde i va del 1 al 6)
- 6 capas vectoriales resultado de las intersecciones **tp_inters_mun_usv_si.shp**(donde i va del 1 al 6), una por serie **mun_usv_si.shp** donde i va del 1 al 6)
se entrega como producto final

- 6 archivos csv a nivel municipal, uno por serie **mun_usv_si.csv** (donde i va del 1 al 6) que son copia de los atributos de la capa vectorial correspondiente
ruta : SIG\desarrollo\sig_fomix\entregables\municipios_usv\
