import math 
layer = iface.activeLayer()
extent = layer.extent()
#region_peninsula = '145399.882634,526940.882019,1979440.790516,2391757.031490'
xmin, xmax,ymin,ymax = extent.xMinimum(), extent.xMaximum(),extent.yMinimum(),2391840
#extension_peninsula = '145399.0,526999.0,1979440.0,2391840.0'
def more_up(v_o):
    v_n = round(v_o)
    if v_n-v_o> 0:
         return v_n
    else:
        return v_n+1

extent_origin={'xmin':xmin,
                                    'xmax':xmax,
                                    'ymin':ymin,
                                    'ymax':ymax}

for k,v in extent_origin.items():
    print(k,round(v,3))
    

tam_pixel = 100

xmin_n = math.trunc(xmin)
xmax_tp = more_up(xmax)
dif_x_tp = xmax_tp-xmin_n
while dif_x_tp%tam_pixel != 0:
    xmax_tp+=1
    dif_x_tp = xmax_tp-xmin_n
xmax_n=xmax_tp

ymin_n =math.trunc(ymin)
ymax_tp = more_up(ymax)
dif_y = ymax_tp - ymin_n

while dif_y % tam_pixel != 0:
    ymax_tp+=1
    dif_y = ymax_tp - ymin_n
ymax_n=ymax_tp

extent_magic={
                                    'xmin':xmin_n,
                                    'xmax':xmax_n,
                                    'ymin':ymin_n,
                                    'ymax':ymax_n}
                                    
                                    
for k,v in extent_magic.items():
    print(k,v)
region = "%f,%f,%f,%f" % (xmin_n, xmax_n, ymin_n, ymax_n)
print ('region',region)
print  ("with",(xmax_n- xmin_n)/tam_pixel)
print  ("heith",(ymax_n- ymin_n)/tam_pixel)

