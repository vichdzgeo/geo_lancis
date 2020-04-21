

#def input_owa(a,w):
w=[0.08,0.42,0.065,0.435]
no_criterios = len(w)
j = [x for x in range(1,no_criterios+1)]
##df = pd.DataFrame({'j':[1,2,3,4],
##                    'a':a,
##                    'w':w},
##                    columns=['j','a','w'])    
##
##
##
col_raster = ["r"+str(x)for x in range(1,no_criterios+1)]
#m3 = m2.apply(lambda x:x[r1])
#
#def valores(m3,w):
#    no_criterios = len(w)
#    col_raster = ["r"+str(x)for x in range(1,no_criterios+1)]
#    

m2 =mu1[0:10]

m3 = m2.filter(['id'])
m3['v'] = (m2['r1'].astype(float),m2['r2'].astype(float))


#
#m2['owa_0']=''
#m2['owa_01']=''
#m2['owa_05']=''
#m2['owa_1']=''
#m2['owa_2']=''
#m2['owa_10']=''
#m2['owa_1000']=''
#for index, row in m2.iterrows():
#    
#    a=[]
#    for cr in col_raster:
#        a.append(row[cr])
#    
#    df = pd.DataFrame({'j':j,
#                    'a':a,
#                    'w':w},
#                    columns=['j','a','w'])
#    #print(owa(df,'a','w',alpha=1))
#    m2['owa_0'][index]= owa(df,'a','w',alpha=0.0001)
#    m2['owa_01'][index]= owa(df,'a','w',alpha=0.1)
#    m2['owa_05'][index]= owa(df,'a','w',alpha=0.5)
#    m2['owa_1'][index]= owa(df,'a','w',alpha=1)
#    m2['owa_2'][index]= owa(df,'a','w',alpha=2)
#    m2['owa_10'][index]= owa(df,'a','w',alpha=10)
#    m2['owa_1000'][index]= owa(df,'a','w',alpha=1000)
#
#print ("fin")