# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 00:40:21 2017

@author: moghb
"""
import json
import requests
import logging
from bioservices import IntactComplex

your_project_directory="C:\\Users\\moghb\\OneDrive\\Documents\\Database\\expert_schema"

s = IntactComplex()
r=s.search('nup53')['elements'][0]['complexAC']

logger = logging.getLogger(__name__)
url ="https://www.ebi.ac.uk/intact/complex-ws/details/"+r+"?format=json"

def do_request( ):
    resp = requests.get(url)
    logger.debug('Requested {}'.format(resp.url))

    if resp.status_code == 200:
        return resp
    else:
        raise Exception(resp)

j = json.loads(do_request().text)

with open(os.path.join(your_project_directory, 'data.txt'), 'w') as outfile:
    json.dump(j, outfile)
    
list(j["systematicName"].split(":"))

