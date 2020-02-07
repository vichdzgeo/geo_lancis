import pandas as pd
import os 
def lista_shp(path_carpeta):

    for root, dirs, files in os.walk(path_carpeta):
        lista=[]
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                lista.append(extension)
    return lista

def union_csv_shape(path_csv,path_vector,vector_id,bd_csv_id,path_salida):

        '''
        Funcion para unir una base de datos csv a un archivo shapefile, por medio de un campo en comun.
        El resultado es una nueva capa vectorial con la union tabular.
        Parametros
        path_csv: ruta del archivo csv, usar / en vez de '\'
        path_vector: ruta de la capa vectorial
        n_campo_comun: nombre del campo en comun
        path_salida:ruta de salida para la nueva capa vectorial que contiene la union
        '''
        vector = QgsVectorLayer(path_vector, "", "ogr")
        QgsProject.instance().addMapLayer(vector)
        #abre  el archivo csv

        bd_csv_uri = "file:///"+path_csv+"?delimiter=%s&encoding=%s" % (",","utf-8")
        bd_csv = QgsVectorLayer(bd_csv_uri, "", "delimitedtext")
        QgsProject.instance().addMapLayer(bd_csv)

        #Nombre de los campos de ID para relacionar las tablas
        #union del archivo csv y vector.
        
#        unionC = QgsVectorLayerJoinInfo()
#        unionC.joinLayerId = bd_csv.id()
#        unionC.joinFieldName = vector_id
#        unionC.targetFieldName = bd_csv_id
#        unionC.memoryCache= True
#        vector.addJoin(unionC)
        
        joinObject = QgsVectorLayerJoinInfo()
        joinObject.setJoinFieldName(bd_csv_id)
        joinObject.setTargetFieldName(vector_id)
        joinObject.setJoinLayerId(bd_csv.id())
        joinObject.setUsingMemoryCache(True)
        joinObject.setJoinLayer(bd_csv)
        vector.addJoin(joinObject)

        QgsVectorFileWriter.writeAsVectorFormat(vector,path_salida,'utf-8',vector.crs(),"ESRI Shapefile")


path_sig = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/"

path_bd = path_sig + "insumos/stressing_scenarios_equidista.csv"
path_vector =path_sig + "insumos/agebs_cdmx.shp"
path_salida = path_sig + "indice_leesallee/"
path_salida_s = path_sig + "indice_leesallee/shapes/"


'''
#Procesamiento de la base de datos para la separación de experimentos 


datos = pd.read_csv(path_bd)

datos2 = datos.filter(['year','censusblock_id','budget','budget_split','stress','scarcity_vulnerability_cat', 'scaricity_exposure_cat'])

budget_split = datos2.budget_split.unique()
budgets = datos2.budget.unique()
escenarios = datos2.stress.unique()

datos_action_budget = datos2.query('budget_split=="action_budget" and year==2060')
datos_system_budget = datos2.query('budget_split=="system_budget" and year==2060')


for budget in budgets:
    datos_ac = datos_action_budget.query('budget=='+str(budget))
    datos_sys = datos_system_budget.query('budget=='+str(budget))
    if budget==50:
        presupuesto='bajo'
    elif budget==1000:
        presupuesto='medio'
    elif budget==2000:
        presupuesto='alto'
        
    for escenario in escenarios:
        datos_ac_f=datos_ac.query('stress=='+'"'+escenario+'"')
        datos_sys_f=datos_sys.query('stress=='+'"'+escenario+'"')
        
        ac = "action_budget_"+presupuesto+"_"+escenario
        sys ="system_budget_"+presupuesto+"_"+escenario
        datos_ac_f.to_csv(path_salida+ac+".csv",index=False)
        datos_sys_f.to_csv(path_salida+sys+".csv",index=False)
        
        union_csv_shape(path_salida+ac+".csv",path_vector,"ageb_id","censusblock_id",path_salida_s+ac+".shp")
        union_csv_shape(path_salida+sys+".csv",path_vector,"ageb_id","censusblock_id",path_salida_s+sys+".shp")
        

'''

lista_shape = lista_shp(path_salida_s)

vlayer_base = QgsVectorLayer(path_salida_s + 'action_budget_medio_base.shp',"","ogr")
vlayer_model = QgsVectorLayer(path_salida_s + 'action_budget_bajo_base.shp',"","ogr")

#agebs_base = []
#agebs_alto = []
#union = []
#interseccion = []
#for a,b in zip(layer_base.getFeatures(),layer_base_alto.getFeatures()):
#    if a['_scarcity_']==5:
#        agebs_base.append(a['ageb_id'])
#        union.append(a['ageb_id'])
#    if b['_scarcity_']==5:
#        agebs_alto.append(b['ageb_id'])
#        union.append(a['ageb_id'])
#    if a['_scarcity_']==5 and b['_scarcity_']==5:
#        interseccion.append(b['ageb_id'])
#
#union_conjunto = set(union)
##print (len(agebs_base),len(agebs_alto),len(interseccion),len(union_conjunto))
#print (len(interseccion) / len(union_conjunto))
#
#area_interseccion =0
#area_union =0
#
#for i in layer_base.getFeatures():
#    for ageb_union in union_conjunto:
#        if i['ageb_id']==ageb_union:
#            area_union += i.geometry().area()
#    for ageb_interseccion in interseccion:
#        if i['ageb_id']==ageb_interseccion:
#            area_interseccion += i.geometry().area()
#
#print (area_interseccion / area_union )

def indice_lee_salee(vlayer_base,vlayer_model,campo_categoria,categoria,id='ageb_id'):   
    
    union = []
    interseccion = []
    for a,b in zip(vlayer_base.getFeatures(),vlayer_model.getFeatures()):
        if a[campo_categoria]==categoria:
            union.append(a[id])
        if b[campo_categoria]==categoria:
            union.append(a[id])
        if a[campo_categoria]==categoria and b[campo_categoria]==categoria:
            interseccion.append(b[id])

    union_conjunto = set(union)
    #print (len(agebs_base),len(agebs_alto),len(interseccion),len(union_conjunto))
    indice_lee_count = round((len(interseccion) / len(union_conjunto)),4)

    area_interseccion =0
    area_union =0

    for i in vlayer_base.getFeatures():
        for ageb_union in union_conjunto:
            if i[id]==ageb_union:
                area_union += i.geometry().area()
        for ageb_interseccion in interseccion:
            if i[id]==ageb_interseccion:
                area_interseccion += i.geometry().area()
    indice_lee = round(area_interseccion / area_union,4)
    return indice_lee_count,indice_lee
    
print(indice_lee_salee(vlayer_base,vlayer_model,'_scarcity_',5,id='ageb_id'))