import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
#promedios = pd.read_csv('V:/Mi unidad/residuales/promedios.csv')


def residuales_gower(path_csv_promedios,path_residuales):
    promedios = pd.read_csv(path_csv_promedios)
    criterios = list(promedios.columns)[1:]
    promedios_c = promedios.filter(items=criterios).mean(axis=1)
    promedios_r = promedios.filter(items=criterios).mean(axis=0)
    promedios_prom = promedios.filter(items=criterios).to_numpy().mean()
    residuales = promedios.copy(deep=True)
    for k,v in promedios.filter(items=criterios).items():
        for k2,v2 in v.items():
            residual=v2-promedios_r[k]-promedios_c[k2]+promedios_prom
            residuales[k][k2]=residual

    print (residuales)
    residuales.round(3).to_csv(path_residuales,index=False)


promedios = pd.read_csv('C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/pruebas_sigzonning/pca_yuc/bd_promedios_grupos.csv')
print (promedios)
criterios = list(promedios.columns)[1:]
promedios_c = promedios.filter(items=criterios).mean(axis=1)
promedios_r = promedios.filter(items=criterios).mean(axis=0)
promedios_prom = promedios.filter(items=criterios).to_numpy().mean()
residuales = promedios.copy(deep=True)

for k,v in promedios.filter(items=criterios).items():
    for k2,v2 in v.items():
        residual=v2-promedios_r[k]-promedios_c[k2]+promedios_prom
        residuales[k][k2]=residual

print (residuales)
#residuales.round(3).to_csv('C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/pruebas_sigzonning/pca_bc/bd_residuales_grupos.csv',index=False)
residuales.round(3)
N=len(residuales)
ind = np.arange(N)
#plt.figure()
residuales.filter(items=criterios).plot(kind='bar',width=0.35)
l_grupos = ["grupo "+str(i) for i in range(1,len(residuales)+1)]
plt.xticks(ind, (l_grupos))
plt.axhline(0, color='k')
plt.show()
