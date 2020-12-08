import pandas as pd 


o_data = pd.read_csv("C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/centroide/clasificaciones.csv") 
data = o_data.sort_values('rank_order',ascending=True).copy()
one_n = 1/len(data.alternatives)

data2=data.assign(one_k=1/data.rank_order)
print (data2)
data2['w']=0
for  i in range(len(data.alternatives)):
     data2.w.loc[i]=one_n*sum(data2.one_k[i:len(data.alternatives)])
print (data2)
data3 =data2.filter(['rank_order','alternatives','w'])

data3.to_csv("C:/Dropbox (LANCIS)/CARPETAS_TRABAJO/vhernandez/geo_lancis/centroide/clasificaiones_w_centroid.csv",index=False)