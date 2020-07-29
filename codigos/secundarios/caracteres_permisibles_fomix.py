def permisible (cadena):

    caracteres_permitidos = [' ','-','_',',',"  ",'á','é','í','ó','ú',]
    caracteres_remplazo = ['','','','','','a','e','i','o','u']
    str=cadena.lower()
    for x in caracteres_permitidos:
        if  x in str:
            
            for a,b in zip(caracteres_permitidos,caracteres_remplazo):
                str=str.replace(a,b)
                permisible(str)
                print(str)
        else:
                return str
            

    
#a ="México mágico Avión"
a ='Zona citrícola'
print(a.isalnum())
aa=permisible(a)
if  aa.isalnum():
    x=0
else:
    print ("No es una cadena válida")
print(aa.isalnum())