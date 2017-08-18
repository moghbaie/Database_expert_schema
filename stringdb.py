# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:30:04 2017

@author: moghb
"""

import csv
import json
import logging
import requests
import pandas as pd
import xml.etree.ElementTree as et
from six import StringIO, string_types

logger = logging.getLogger(__name__)

PSIMITAB_COLUMNS = [
    'Unique identifier for interactor A',
    'Unique identifier for interactor B',
    'Alternative identifier for interactor A',
    'Alternative identifier for interactor B',
    'Aliases for A',
    'Aliases for B',
    'Interaction detection methods',
    'First author surname(s)',
    'Identifier of the publication',
    'NCBI Taxonomy identifier for interactor A',
    'NCBI Taxonomy identifier for interactor B',
    'Interaction types',
    'Source databases',
    'Interaction identifier(s)',
    'Confidence score',
]

STRINGDB_REQUEST_TEMPLATE = "{http}://{address}/api/{format}/{request}"

def do_request_stringdb(request, req_format, params, https=False, database='string-db.org'):
    """
    Send actual HTTP request to API.
    """
    url = STRINGDB_REQUEST_TEMPLATE.format(
        http='https' if https else 'http',
        address=database,
        format=req_format,
        request=request)
    resp = requests.get(url, params=params)
    logger.debug('Requested {}'.format(resp.url))

    if resp.status_code == 200:
        return resp
    else:
        raise Exception(resp)

def get_interactions(identifier, species=None, required_score=400, limit=100, q_format='psi-mi', *args):
    """
    Query DB for interaction network in PSI-MI 2.5 format or PSI-MI-TAB format (similar to tsv).
    `identifier` is the protein name
    `format` may be 'psi-mi' or 'psi-mi-tab'
    If 'psi-mi', the response is returned in PSI-MI 2.5 XML format. This method will return
    an xml ElementTree object
    `species` may be specified (e.g. Human 9606, see: http://www.uniprot.org/taxonomy)
    Example:
    ########
    results = stringdb.get_interactions(['ALK'], q_format='psi-mi')
    If `format='psi-mi-tab'` results are returned in Tab-delimited form of PSI-MI
    (similar to tsv, modeled after the IntAct specification,
        Contains less info than XML response.)
    This method will return a pandas.DataFrame object.
    Example:
    ########
    results = stringdb.get_interactions(['ALK'], q_format='psi-mi-tab')
    results.to_csv('outfile.tsv', delimiter='\t', index=False)
    """
    if q_format not in {'psi-mi', 'psi-mi-tab'}:
        raise Exception("format has to be one of ('psi-mi', 'psi-mi-tab'). {} is invalid.".format(q_format))
    resp = do_request_stringdb('interactions', q_format,
        {'identifier': identifier, 'required_score': required_score, 'limit': limit, 'species': species}, *args)
    if q_format == 'psi-mi':
        return et.fromstring(resp.text)
    elif q_format == 'psi-mi-tab':
        sio = StringIO(resp.text)
        return pd.read_csv(sio, delimiter='\t', header=None, names=PSIMITAB_COLUMNS)

    
def get_interactions_image(identifier, flavor, filename, required_score=950,
    limit=50, *args):
    """
    Save network image of interactions to file.
    `identifiers` is the protein name
    `flavor` is one of:
        'evidence' for colored multilines
        'confidence' for singled lines where hue correspond to confidence score
        'actions' for stitch only.
    `filename` is the file to save the png to.
    """

    r = do_request_stringdb('network', 'image',
        {'identifier': identifier, 'required_score': required_score, 'limit': limit}, *args)
    with open(filename, 'wb') as outfile:
        for chunk in r:
            outfile.write(chunk)
            
def resolve(identifier, species=None, *args, **kwargs):
    """
    Search the database for proteins with the name in `identifier`.
    Allows us to later resolve the names which are ambiguous.
    """
    req_format = kwargs.pop('req_format', 'json')

    request_name = 'resolve' if isinstance(identifier, string_types) else 'resolveList'
    id_param_name = 'identifier' if isinstance(identifier, string_types) else 'identifiers'
    identifier = identifier if isinstance(identifier, string_types) else '\n'.join(identifier)

    resp = do_request_stringdb(request_name, req_format, {id_param_name: identifier, 'species': species}, *args, **kwargs)
    if not resp.status_code == 200:
        raise Exception(resp)
    try:
        return json.loads(resp.text)
    except:
        sio = StringIO(resp.text)
        return list(csv.reader(sio, delimiter='\t'))