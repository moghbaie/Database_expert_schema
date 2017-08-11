# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:58:09 2017

@author: moghb
"""
from stringdb import get_interactions, get_interactions_image, resolve
import xml.etree.ElementTree as et
import os

your_project_directory="C:\\Users\\moghb\\OneDrive\\Documents\\Database\\expert_schema"

get_interactions_image(['TP53'],'evidence','image.png')

resolve(['TP53'])

results1 = get_interactions(['ALK'], q_format='psi-mi-tab')
results1.to_csv(os.path.join(your_project_directory,'outfile.tsv'), index=False)


results2 = get_interactions(['ALK'], q_format='psi-mi')
et.ElementTree(results2).write(open(os.path.join(your_project_directory,'outfile.xml'), 'wb'))


foo = lambda x: (i for i in reversed(x['Confidence score'].split("|")))
boo = lambda y:  dict(item.split(":") for item in y)
score= results1.apply(foo, axis=1)
scores= score.apply(boo)

for key, value in scores[1].items():
    print(key, value) 
    


