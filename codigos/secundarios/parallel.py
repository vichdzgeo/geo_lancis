import plotly.express as px
import pandas as pd 



df = pd.read_csv("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/vulnerabilidad_costera_localidades/procesamiento/estadistica_integrada/localidades_yuc/localidades_yuc_promedios_criterios_sensibles.csv")
cols = df.columns.tolist()
lista = [x for x in range(1,len(df)+1)]

df['id']=lista

fig = px.parallel_coordinates(df, #color="id",
                              dimensions=cols[1:],
                              #range_color="localidad",
                              color_continuous_scale=px.colors.sequential.Viridis,
                              title="localidades_yuc",
                              color_continuous_midpoint=25)
fig.show()


# from matplotlib import pyplot as plt
# import pandas as pd 
# df = pd.read_csv('https://gist.github.com/curran/a08a1080b88344b0c8a7/raw/639388c2cbc2120a14dcf466e85730eb8be498bb/iris.csv')
# pd.plotting.parallel_coordinates(
#         df, 'species',
#         color=('#556270', '#4ECDC4', '#C7F464'))
# plt.show()