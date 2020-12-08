def permisible (cadena):

    caracteres_permitidos = [' ','-','_',',',"  ",'/','á','é','í','ó','ú',]
    caracteres_remplazo = ['','','','','','','a','e','i','o','u']
    str_txt=cadena.lower()
    for x in caracteres_permitidos:
        if  x in str_txt:
            
            for a,b in zip(caracteres_permitidos,caracteres_remplazo):
                str_txt=str_txt.replace(a,b)
                permisible(str_txt)               
        else:
                return str_txt

def codificacion_contenido(vlayer):
  
    campos = [field.name() for field in vlayer.fields() if field.typeName()=="String"]
    lista = []
    for pol in vlayer.getFeatures():
        for campo in campos:
             if not pol[campo]==NULL:
                cadena=permisible(pol[campo])
                if cadena.isalnum():
                    lista.append(1)
                else:
                    lista.append(2)
    lista2=list(set(lista))

    if len(lista2)>1 :
        return "error en la codificación"
    else:
        return "codificación correcta"
                    
            

    return indicador
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
        status = "no"
        total = len(lista_campos_nulos)
        if total >0:
            binario=0
            status="si"
        return status



dicc={}
lista_capas = []
for layer in iface.mapCanvas().layers():
        url = layer.dataProvider().dataSourceUri().split("|")[0]
        nombre = layer.name()
        if  nombre not in dicc:            
            dicc[nombre]={'url':url}

dicc_2 = {}

for k,v in dicc.items():
    if dicc[k]['url'].split(".")[1] =="shp":
        dicc_2[k]={'url':dicc[k]['url'],'nulos':'','codificacion':'','proyección':''}

cont = 0      
for k2,v2 in dicc_2.items():
    path_v = dicc_2[k2]['url']
    
    if 'aves'  not  in k2 and 'mamiferos' not  in k2 and 'reptiles' not in k2 and 'anfibios' not in k2 and 'plantas' not in k2:
        print(cont,k2)
        layer = QgsVectorLayer(path_v,"","ogr")
        dicc_2[k2]['nulos']= campos_nulos(layer)
        dicc_2[k2]['codificacion']= codificacion_contenido(layer)
        dicc_2[k2]['proyección']= layer.crs().authid()
        cont+=1

bitacora = open(r"C:\Dropbox (LANCIS)\SIG\desarrollo\sig_fomix\procesamiento\verificacion_capas.csv","w")
bitacora.write("nombre,nulos,codificación,proyección,url\n")
for k,v in dicc_2.items():
    cadena = k+","+dicc_2[k]['nulos']+","+dicc_2[k]['codificacion']+","+dicc_2[k]['proyección']+","+dicc_2[k]['url']+","+"\n"
    bitacora.write(cadena)
bitacora.close()