# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:58:09 2017
@author: moghb
"""
from stringdb import get_interactions, get_interactions_image, resolve
from complexPortaldb import do_request_complexdb
import xml.etree.ElementTree as et
import os
import pandas as pd
import numpy as np

your_project_directory=os.getcwd()

"""
Save network image of interactions to file.
`identifiers` is the protein name
"""

get_interactions_image(['NUP53'],'evidence','image.png')

"""
Search the database for proteins with the name in `identifier`.
Allows us to later resolve the names which are ambiguous.
"""
resolve(['NUP53'])

"""
Saving result in .xml format
"""
#results = get_interactions(['NUP53'], q_format='psi-mi')
#et.ElementTree(results).write(open(os.path.join(your_project_directory,'outfile.xml'), 'wb'))


def creat_model_input(identifier, species=None, limit=100):
    res =get_interactions( identifier=identifier, limit=limit,  species=species ,q_format='psi-mi-tab')
    df_=res.filter(items=['Alternative identifier for interactor A', 
                                    'Alternative identifier for interactor B'])
    df_.columns=['interactor_A','interactor_B']
    foo = lambda x: (i for i in reversed(x['Confidence score'].split("|")))
    boo = lambda y:  dict(item.split(":") for item in y)
    score= res.apply(foo, axis=1)
    scores= score.apply(boo)
    columns=[ 'score', 'nscore', 'fscore', 'pscore',
              'hscore', 'ascore', 'escore', 'dscore', 'tscore']
    df = pd.DataFrame(list(scores), columns = columns)
    df= df.fillna(0)  
    result =pd.merge(df_, df, left_index=True, right_index=True)
    result[columns] = result[columns].apply(pd.to_numeric)
    return result

"""
Example
creat_model_input(['NUP53'], 'Human',20)
"""

def make_test_dataset(identifier, species=None, limit=100):
    result = creat_model_input(identifier, species, limit)
    res = result[(result['interactor_A'] == identifier) | (result['interactor_B'] == identifier)]
    interactors = do_request_complexdb(identifier)
    if identifier in interactors: interactors.remove(identifier)
    Y = res[['interactor_A','interactor_B']].isin(interactors)
    Y = (Y['interactor_A'] == True) | (Y['interactor_B'] == True)
    Y = np.array(Y.astype(int))
    X = np.array(res[['nscore', 'fscore', 'pscore','hscore', 'ascore', 'escore', 'dscore', 'tscore']])
    Z = res[['interactor_A','interactor_B']]
    return X,Y,Z

def make_train_dataset(identifier, species=None, limit=100):
    X,Y,Z = make_test_dataset(identifier, species, limit)
    return X,Y