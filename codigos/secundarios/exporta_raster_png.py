path_salida = 'C:\Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/vulnerabilidad_costera/analisis_3cats/imagenes/'
rlayer = iface.activeLayer()
path_image = path_salida+rlayer.source().split("/")[-1].split(".")[0]+'.png'
renderer = rlayer.renderer()
provider = rlayer.dataProvider()

pipe = QgsRasterPipe()
pipe.set(provider.clone())
pipe.set(renderer.clone())

file_writer = QgsRasterFileWriter(path_image)
file_writer.Mode(1)

file_writer.writeRaster(pipe, provider.xSize()/2, provider.ySize()/2, provider.extent(), provider.crs())

def exporta_tif_png(rlayer,path_salida):
    path_image = path_salida+"mapa_"+rlayer.source().split("/")[-1].split(".")[0]+'.png'
    renderer = rlayer.renderer()
    provider = rlayer.dataProvider()

    pipe = QgsRasterPipe()
    pipe.set(provider.clone())
    pipe.set(renderer.clone())

    file_writer = QgsRasterFileWriter(path_image)
    file_writer.Mode(1)

    file_writer.writeRaster(pipe, provider.xSize()/2, provider.ySize()/2, provider.extent(), provider.crs())