# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 01:35:24 2017

@author: moghb
"""
import requests
import logging


logger = logging.getLogger(__name__)

CRAPOME_REQUEST_TEMPLATE ="http://crapome.org/?q=ws/{detail}/{gene_symbol}/{organism}/{version}"


def do_request_crapome( detail, gene_symbol, organism, version):
    """
    Send actual HTTP request to API.
    """
    url = CRAPOME_REQUEST_TEMPLATE.format(
            detail=detail,
            gene_symbol=gene_symbol,
            organism=organism,
            version=version)
    resp = requests.get(url)
    logger.debug('Requested {}'.format(resp.url))

    if resp.status_code == 200:
        return resp
    else:
        raise Exception(resp)
        
        
#do_request_crapome("proteindetail","TUBB","human","1.1")


url="https://www.crapome.org/?q=geneprofiledetail/TUBB/human/1.1"
res=requests.get(url)
res.status_code
