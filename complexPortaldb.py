# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 00:40:21 2017

@author: moghb
"""

from bioservices import IntactComplex
s = IntactComplex()
s.search('ndc80')
s.search('ndc80', first=0, number=10,
    filters='species_f:("Homo sapiens")',
    facets='ptype_f')
s.search('GO:0016491', first=10, number=10)
