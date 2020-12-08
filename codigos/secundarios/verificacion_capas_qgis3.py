# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayer, QgsProject
import os
from os import listdir,walk
from os.path import isfile, join,splitext
import processing as pr

def nombre_capa(path_shape):
    nombre_capa=(path_shape.split("/")[-1:])[0]
    return nombre_capa

def lista_shape(path):
    lista_shp=[]
    for root, dirs, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                ruta = (root.replace("\\","/")+"/").replace("//","/")+name
                lista_shp.append(ruta)
    return lista_shp

def busca_prj(path_shape):
    path_directorio = "/".join(path_shape.split("/")[:-1])+"/"
    directorio = (path_directorio.replace("\\","/")+"/").replace("//","/")
    fileNames=[]
    for root, dirs, files in walk(path_directorio):
        fileNames+=([f for f in listdir(root) if isfile(join(root, f))if f.split(".")[-1:][0]=='prj'])
    
    capa = (path_shape.split("/")[-1:][0].split(".")[0])+".prj"
    if capa  not in fileNames:
        valor = 0
    if capa in fileNames:
        valor =  10
        
    return valor
    
def busca_xml(path_shape):
    path_directorio = "/".join(path_shape.split("/")[:-1])+"/"
    directorio = (path_directorio.replace("\\","/")+"/").replace("//","/")
    fileNames=[]
    for root, dirs, files in walk(path_directorio):
        fileNames+=([f for f in listdir(root) if isfile(join(root, f))if f.split(".")[-1:][0]=='xml'])
    
    capa = (path_shape.split("/")[-1:][0].split(".")[0])+".xml"
    if capa  not in fileNames:
        valor = 0
    if capa in fileNames:
        valor =  10
        
    return valor
    
def topologia(vlayer,path_topologia):
    
    if not vlayer == "error":
               
        dir_topo = path_topologia+"/topologia"
        if "topologia" not in os.listdir(path_topologia):
            os.mkdir(dir_topo)
        nombre_capa = path_shape.split("/")[-1:][0].split(".")[0]
        p_val = dir_topo+"/"+nombre_capa+"_valido.shp"
        p_error = dir_topo+"/"+nombre_capa+"_error.shp"
        p_invalido = dir_topo+"/"+nombre_capa+"_invalido.shp"
        
        dicc={'INPUT_LAYER':vlayer,
                    'METHOD':2,
                    'VALID_OUTPUT':p_val,
                    'INVALID_OUTPUT':p_invalido,
                    'ERROR_OUTPUT':p_error,
                    'IGNORE_RING_SELF_INTERSECTION':True}
        
        pr.run("qgis:checkvalidity",dicc)
        error_layer=QgsVectorLayer(p_error,"","ogr")
        valid_layer=QgsVectorLayer(p_val,"","ogr")
        
        total_original = int(vlayer.featureCount())
        total_errores = int(error_layer.featureCount())
        total_validos = int(valid_layer.featureCount())
        
        #vlayer,valid_layer,error_layer="","",""
        
        identificador = 0
        if total_original == total_validos:
            identificador=10
        else:
            identificador = 10 -(total_errores*2)
        #print identificador 
        if identificador <0:
            identificador=0
    #    for archivo in os.listdir(dir_topo):
    #        os.remove(dir_topo+"/"+ archivo)
        return identificador
    return "error"
def cargar_capa(path_shape):
    nombre = nombre_capa(path_shape).split(".")[0]
    layer = QgsVectorLayer(path_shape, nombre, "ogr")
    validacion = validar_capa(layer)
    if validacion==1:
        return layer
    elif validacion==0:
        return "error"

def validar_capa(vlayer):
    if vlayer.isValid():
        return 1
    else:
        return 0
        
def tipo_geometria(vlayer):
    if not vlayer == "error":
        if vlayer.geometryType()==0:
            tipo="punto"
        elif vlayer.geometryType()==1:
            tipo= "linea"
        elif vlayer.geometryType()==2:
            tipo = "poligono"
            return tipo
    return "error"

def total_campos(vlayer):
    
    if not vlayer == "error":
        campos = [field.name() for field in vlayer.fields()]
        total = len(campos)
        return total
    return "error"
def total_geometrias(vlayer):
    if not vlayer == "error":
        total = int(vlayer.featureCount())
        return total
    return "error"
def nombre_proyeccion(path_shape,vlayer):
    existe_prj = busca_prj(path_shape)
    proyeccion = ''
    if existe_prj ==10:
        
        proyeccion = vlayer.crs().authid()
        return proyeccion
    else:
        return "capa sin archivo prj"


def campos_nulos(vlayer):
    
    if not vlayer == "error":
        campos = [field.name() for field in vlayer.fields()]
        dicc={}
        for campo in campos:
            dicc[campo]=0
        for poligono in vlayer.getFeatures():
 
            for campo in campos:
                lista_vacio=0
                if not poligono[campo]:
                    if poligono[campo]==NULL:
                        lista_vacio+=1
                if lista_vacio > 0:
                    dicc[campo]+=1

        lista_campos_nulos=[]
 
        for key,value in dicc.items():
            if value>0:
                lista_campos_nulos.append(key)
                
        binario=10
        total = len(lista_campos_nulos)
        if total >0:
            binario=0
        return binario
    
    return "error"

def sin_geometria(vlayer):
    lena=0
    identificador=10
    for element in vlayer.getFeatures():
        if element.geometry() ==None:
            lena+=1
    if lena >0:
        identificador=0
    return identificador
def codificacion_contenido(vlayer):
    
    
    total = int(vlayer.featureCount())
    campos = [field.name() for field in vlayer.fields() if field.typeName()=="String"]
    dicc_campos={}
    for campo in campos:
        dicc_campos[campo]={'valido':0,'invalido':0,'como_txt':0,'vacio':0}
    
    for pol in vlayer.getFeatures():
        for campo in campos:
            if not pol[campo]:
                 if pol[campo]==NULL:
                     cadena=''
                     dicc_campos[campo]['vacio']+=1
            else:
                cadena=pol[campo]
            
            permisible=(((cadena.replace(" ","")).replace(".","")).replace("-","")).replace("/","")
              
            num=666
            alfanum=999
            if cadena.replace(".","").isdigit():
                num =1
            elif permisible.isalnum():
                alfanum =2
#            print (pol['nomgeo'],campo,num,alfanum)
            status =''
            if num==1:
                status="numero codificado como texto"
                dicc_campos[campo]['como_txt']+=1
            elif alfanum==2:
                status="codificado correctamente"
                dicc_campos[campo]['valido']+=1
            else:
                status="error en la codificacion"
                dicc_campos[campo]['invalido']+=1
    valor=0
    campos_mal = []
    campos_texto =[]
    
    for key,value in dicc_campos.items():
        valor+=((value['valido']*100)/total)
        if value['invalido'] >0 :
            permisible=(((key.replace(" ","")).replace("_","")).replace("-","")).replace("/","")
            if permisible.isalnum():
                campos_mal.append(key)
            else:
                campos_mal.append("error detectado")
        if value['como_txt']>0:
            permisible=(((key.replace(" ","")).replace("_","")).replace("-","")).replace("/","")
            if permisible.isalnum():
                campos_texto.append(key)
            else:
                campos_texto.append("error detectado")

        
        
        #print (key,"el ",((value['correcto']*100)/total),"por ciento de los datos esta codificado correctamente")
    valor_final = valor
    indicador=0
    if valor_final ==len(campos)*100:
        indicador=10
    total = len(campos_mal)+len(campos_texto)
    c_mal = campos_mal +campos_texto
    
    return indicador

def diagnostico_capas(path_shape,path_topologia):
    suma=0
    diagnostico = {"nombre":"",
                            "total_campos":'-',
                            "metadatos":'-',
                            "proyeccion":'-',
                            "geometria_completa":'-',
                            "sobrelapados":'-',
                            "sin_atributo":'-',
                            "huecos":'-',
                            "nulos":'-',
                            "significado":'-',
                            "unidades":'-',
                            "codificados":'-',
                            "resolucion":'-',
                            "fecha":'-',
                            "linaje":'-',
                            "fuente":'-',
                            "nombre_proyeccion":'-',
                            "ruta":'-'}
    vlayer = cargar_capa(path_shape)
   
    if not vlayer == "error":
        diagnostico["nombre"]=nombre_capa(path_shape)
        diagnostico["total_campos"]=total_campos(vlayer)
        diagnostico["metadatos"]=busca_xml(path_shape)
        diagnostico["proyeccion"]=busca_prj(path_shape)
        diagnostico["geometria_completa"]=sin_geometria(vlayer)
        diagnostico["sobrelapados"]=topologia(vlayer,path_topologia)
        diagnostico["sin_atributo"]="NA"#sin_geometria(vlayer) #falta cargarla
        diagnostico["huecos"]="NA"
        diagnostico["nulos"]=campos_nulos(vlayer)
        diagnostico["significado"]="NA"
        diagnostico["unidades"]="NA" 
        diagnostico["codificados"]=codificacion_contenido(vlayer)
        diagnostico["resolucion"]="NA"
        diagnostico["fecha"]="NA"
        diagnostico["linaje"]="NA"
        diagnostico["fuente"]="NA"
        diagnostico["nombre_proyeccion"]=nombre_proyeccion(path_shape,vlayer)
        diagnostico["ruta"]=path_shape
        
        for key,value in diagnostico.items():
            if not key=='total_campos':
                if isinstance(value, int) and not isinstance(value, tuple):
                    suma+=value
                if isinstance(value, tuple):
                    suma+=value[0]
        
        diagnostico['suma']=suma
        
        return diagnostico
    return diagnostico



# path = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/insumos/poetcy/faltantes/"
# path_salida = "C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/diagnostico/fomix_poetcy/csv_diagnostico/"
# path_rst = "C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/diagnostico/fomix_poetcy/rst/"
# path_topologia = "C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/diagnostico/fomix_poetcy/"
# bitacora = open("C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/diagnostico/fomix_poetcy/bitacora_poetcy_faltantes.csv","w")
# criterios_diagnosticos = ["nombre",
#                             "metadatos",
#                             "proyeccion",
#                             "geometria_completa",
#                             "sobrelapados",
#                             "sin_atributo",
#                             "huecos",
#                             "nulos",
#                             "significado",
#                             "unidades",
#                             "codificados",
#                             "resolucion",
#                             "fecha",
#                             "linaje",
#                             "fuente",
#                             "nombre_proyeccion",
#                             "suma"]
# encabezado =''
# for criterio in criterios_diagnosticos:
#     encabezado+=(criterio+",")
# encabezado +="\n"
# bitacora.write(encabezado)


# lista_shp=lista_shape(path)

# for path_shape in lista_shp:
    
#     print ("Procesando capa :",nombre_capa(path_shape))
#     linea = ''
#     diagnostico=diagnostico_capas(path_shape,path_topologia)
#     linea =str(diagnostico["nombre"])+","+\
#             str(diagnostico["metadatos"])+","+\
#             str(diagnostico["proyeccion"])+","+\
#             str(diagnostico["geometria_completa"])+","+\
#             str(diagnostico["sobrelapados"])+","+\
#             str(diagnostico["sin_atributo"])+","+\
#             str(diagnostico["huecos"])+","+\
#             str(diagnostico["nulos"])+","+\
#             str(diagnostico["significado"])+","+\
#             str(diagnostico["unidades"])+","+\
#             str(diagnostico["codificados"])+","+\
#             str(diagnostico["resolucion"])+","+\
#             str(diagnostico["fecha"])+","+\
#             str(diagnostico["linaje"])+","+\
#             str(diagnostico["fuente"])+","+\
#             str(diagnostico["nombre_proyeccion"])+","+\
#             str(diagnostico["suma"])+"\n"
    
#     bitacora.write(linea)
# bitacora.close()

