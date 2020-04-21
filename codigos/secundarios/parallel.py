import plotly.express as px
import pandas as pd 



# df = pd.read_csv("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/insumos/parallel_cat_cdmx_2060_escasez.csv")

# # lista = [x for x in range(1,len(df)+1)]

# # df['id']=lista

# fig = px.parallel_coordinates(df, color="budget",
#                               dimensions=['vul_id','budget','Vuln_cat','Exp_n','Vuln_n','Poblacion','UE','Ingreso'],
#                               #range_color="budget",
#                               color_continuous_scale=px.colors.sequential.Viridis,
#                               title="CDMX",
#                               color_continuous_midpoint=25)
# fig.show()


from matplotlib import pyplot as plt
import pandas as pd 
df = pd.read_csv('https://gist.github.com/curran/a08a1080b88344b0c8a7/raw/639388c2cbc2120a14dcf466e85730eb8be498bb/iris.csv')
pd.plotting.parallel_coordinates(
        df, 'species',
        color=('#556270', '#4ECDC4', '#C7F464'))
plt.show()