import pandas as pd 
import matplotlib as plp
import matplotlib.pyplot as plt
import os 
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.collections import LineCollection
import numpy as np 
from matplotlib.cm import ScalarMappable

path_csv = 'C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/repositorios_git/fomix/docs/source/recursos/tabla_fv_cat_suelo_silvopastoril.csv'
df = pd.read_csv(path_csv,index_col = 0)
print (df.columns)
fig, ax = plt.subplots()
df2 = df.sort_values('FV',ascending=False)
#ax.bar(df2['Categoría'], df2['FV'])
ax.set_xticklabels(df['Categoría'],rotation=0, horizontalalignment= 'center',fontsize = '9')
barra = {
        0.2:'#ffee7e',
        0.4:'#faaf3c',
        0.6:'#f35864',
        0.8:'#c9008c',
        1.0:'#691e91'}
lista_v = list(df2['FV'])
lista_color= []
for i in range(len(df2['FV'])):
    if lista_v[i]>0.8 and lista_v[i]<=1.0:
        lista_color.append(barra[1.0])
    elif lista_v[i]>0.6 and lista_v[i]<=0.8:
        lista_color.append(barra[0.8])
    elif lista_v[i]>0.4 and lista_v[i]<=0.6:
        lista_color.append(barra[0.6])
    elif lista_v[i]>0.2 and lista_v[i]<=0.4:
        lista_color.append(barra[0.4])
    elif lista_v[i]>=0 and lista_v[i]<=0.2:
        lista_color.append(barra[0.2])



# Use a boundary norm instead

colores_b =barra.values()
my_cmap =  ListedColormap(colores_b)
sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0,1))
sm.set_array([])
cbar = plt.colorbar(sm,ticks=[0,1])
cbar.ax.set_yticklabels(['Menos deseable', 'Más deseable']) 

plt.bar(df['Categoría'], df2['FV'], width=0.45,color=lista_color)

plt.show()
fig.savefig("C:/tmp/test_rasterization.png", dpi=500)
plt.close(fig)