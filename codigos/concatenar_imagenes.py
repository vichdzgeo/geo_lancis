import cv2 

imagen1 = cv2.imread("C:/Dropbox (LANCIS)/FOMIX/fmx_estudio_tecnico/diagnostico/talleres/sphinx/docs/source/recursos/conflictos/mapa_milpa_maya_eq_cruza_conservacion_eq.png")

scale_percent = 15 # percent of original size
width = int(imagen1.shape[1] * scale_percent / 100)
height = int(imagen1.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
imagen_1 = cv2.resize(imagen1, dim, interpolation = cv2.INTER_AREA)

# Concatenando imágenes
concat_h1 = cv2.hconcat([imagen_1, imagen_1, imagen_1])
concat_h2 = cv2.hconcat([imagen_1, imagen_1, imagen_1])
concat_h3 = cv2.hconcat([imagen_1, imagen_1, imagen_1])
concat_v = cv2.vconcat([concat_h1, concat_h2,concat_h3])
cv2.imshow('concat_v', concat_v)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/codigos/concatena_imagenes/union.png',concat_v) 