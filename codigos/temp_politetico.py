







# r.mapcalc expression="pca1a_CC" = "pca1a@PERMANENT" * "x372_06RY_CC_100m@PERMANENT"
# r.mapcalc expression="pca1b_CC" = "pca1b@PERMANENT" * "x372_06RY_CC_100m@PERMANENT"
# r.mapcalc expression="pca1b_DE" = "pca1b@PERMANENT" * "x372_09RY_DE_100m@PERMANENT" 
# r.mapcalc expression="pca1a_DE" = "pca1a@PERMANENT" * "x372_09RY_DE_100m@PERMANENT"
# r.mapcalc expression="pca1a_HIDR" = "pca1a@PERMANENT" * "x372_25RY_HIDR_100m@PERMANENT"
# r.mapcalc expression="pca1b_HIDR" = "pca1b@PERMANENT" * "x372_25RY_HIDR_100m@PERMANENT"
# r.mapcalc expression="pca1b_CP" = "pca1b@PERMANENT" * "x372_34RY_CP_100m@PERMANENT" 
# r.mapcalc expression="pca1a_CP" = "pca1a@PERMANENT" * "x372_34RY_CP_100m@PERMANENT"

capas = {'CP':"x372_34RY_CP_100m@PERMANENT",
         'HIDR':"x372_25RY_HIDR_100m@PERMANENT",
         'DE':"x372_09RY_DE_100m@PERMANENT",
         'CC':"x372_06RY_CC_100m@PERMANENT"}

mascaras = ["pca1a1_mask",
            "pca1a2_mask",
            "pca1b1_mask",
            "pca1b2_mask"]

# for mascara in mascaras:
#     cadena = 'r.null map='+mascara+'@PERMANENT setnull=0'
#     print (cadena)


insumos_intermedios =[]
for mascara in mascaras:
    for k,v in capas.items():
        nombre_salida = mascara.split("_")[0]+"_"+k
        #print("---")
        cadena = 'r.mapcalc expression="'+mascara.split("_")[0]+"_"+k+' = '+mascara+'@PERMANENT * '+v+'"'
        insumos_intermedios.append(nombre_salida)
        #print (cadena)

#print (insumos_intermedios)


pca_salidas=['pca1a1','pca1a2','pca1b1','pca1b2']

for pca in pca_salidas:
    cadena ='i.pca --overwrite input='
    for insumo_int in insumos_intermedios:
        if pca in insumo_int:
            cadena+=insumo_int+"@PERMANENT,"
    print (cadena[:-1]+' output='+pca+' rescale=1,11')


