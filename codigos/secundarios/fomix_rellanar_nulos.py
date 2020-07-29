
def nulos(v):
    if v=='String':
        return 'nd'
    elif v=='Integer64':
        return -9999
    elif v=='Real':
        return -9999.0


path_layer = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_fomix/entregables/flora_fauna_yuc/registro_plantas.shp'
layer = QgsVectorLayer(path_layer,"","ogr")
campos = {field.name():field.typeName() for field in layer.fields()}
tipo_campos = set(campos.values())
total_campos = len(campos.keys())
print (tipo_campos)
layer.startEditing()
for k,v in campos.items():
    for poligon in layer.getFeatures():
        if poligon[k]==NULL:
            poligon[k]=nulos(v)
            layer.updateFeature(poligon)
layer.commitChanges()
print ("fin")