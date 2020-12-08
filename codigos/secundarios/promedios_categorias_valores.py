 
 
path_csv = 'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/vulnerabilidad_costera/resiliencia_vs_wf_1_3.csv'
dicc = {'INPUT':'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/vulnerabilidad_costera/resiliencia_yuc_100m.tif',
                'BAND':1,
                'ZONES':'C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/procesamiento/vulnerabilidad_costera/clasificaciones/resiliencia_yuc_100m_wf_1_3_5cats.tif',
                'ZONES_BAND':1, 
                'REF_LAYER':0,
                'OUTPUT_TABLE':path_csv}

processing.run("native:rasterlayerzonalstats",dicc)