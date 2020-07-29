import math 
layer = iface.activeLayer()
extent = layer.extent()

xmin, xmax,ymin,ymax = extent.xMinimum(), extent.xMaximum(),extent.yMinimum(),extent.yMaximum()

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
    print(k,v)
    

tam_pixel = 15

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