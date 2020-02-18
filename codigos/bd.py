import pandas as pd
import os


def weber_fechner(fp=2,min=0,max=1):
    dicc_e = {}
    lista_val = [0,]
    categorias = 5
    pm = max - min 
    cats = numpy.power(fp, categorias)
    e0 = pm/cats
    for i in range(1 , categorias + 1):
        dicc_e['e'+str(i)]= round((max - (numpy.power(fp,i) * e0)),3)
        

    dicc_cortes ={}
    for i in range(1 , categorias + 1):
        dicc_cortes['corte'+str(i)]= round(1 - dicc_e['e'+str(i)],3)
        lista_val.append(round(1 - dicc_e['e'+str(i)],3))

    return lista_val

def clasificar(valor,cortes):
    cat = ''
    categorias_txt = ['1','2','3','4','5']
       
    for i in range(len(cortes)-1):
        myMin = cortes[i]
        myMax = cortes[i+1]

        if valor >= myMin and valor <= myMax:
            return categorias_txt[i]






path_sig = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/stressing/"
path_bd = path_sig + "insumos/ss_equidista.csv"
path_bd_pf20  = path_sig + "insumos/ss_fp20.csv"

datos0 = pd.read_csv(path_bd)
datos = datos0.filter(['year','censusblock_id','budget','budget_split','stress','scarcity_vulnerability', 'scarcity_exposure'])



datos['scarcity_exposure_v'] = (1-datos.scarcity_exposure)
max_exposicion = datos.scarcity_exposure_v.max()

max_vulnerabilidad = datos.scarcity_vulnerability.max()
datos['scarcity_exposure_n'] = (datos.scarcity_exposure_v / max_exposicion)
datos['scarcity_vulnerability_n'] =(datos.scarcity_vulnerability / max_vulnerabilidad)


cortes =weber_fechner(fp=2.0)

datos['cat_scarcity_exposure']=datos.scarcity_exposure_n.apply(lambda x: clasificar(x,cortes))
datos['cat_scarcity_vulnerability']=datos.scarcity_vulnerability_n.apply(lambda x: clasificar(x,cortes))

datos.to_csv(path_bd_pf20,index=False)