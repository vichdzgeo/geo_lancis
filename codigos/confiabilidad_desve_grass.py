#!/usr/bin/env python3

import grass.script as gscript




def calcula_ds(mapa_nominal,criterio,fp):

    mapa_salida = criterio+'_avedev_'+fp

    gscript.run_command('r.stats.zonal', 

                        base=mapa_nominal+'@PERMANENT',

                        cover=criterio+'@PERMANENT',

                        method='average',

                        overwrite=True,

                        output=mapa_salida)



    mapas=",".join([mapa_nominal+'@PERMANENT', mapa_salida+'@PERMANENT'])

    gscript.run_command('r.stats', 

                        input=mapas,

                        flags='An')



def main():
    calcula_ds('exposicion_yuc_wf_1_3_5catsmin0max1','distancia_manglar_exp','1_3')


if __name__ == '__main__':
    main()
