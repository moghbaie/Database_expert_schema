# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 20:49:14 2017

@author: moghb
"""
from getStringData import creat_model_input
import numpy as np
import networkx as nx
import nxviz as nv
import matplotlib.pyplot as plt

def draw_MatrixPlot(identifier, species=None, limit=100):
    result = creat_model_input(identifier, species, limit)
    G=nx.from_pandas_dataframe( result, 'interactor_A','interactor_B', 
                               [ 'score', 'nscore', 'fscore', 'pscore','hscore',
                                'ascore', 'escore', 'dscore', 'tscore'])
    am=nv.MatrixPlot(G)
    am.cmap = plt.cm.get_cmap('Greens')
    am.draw()
    plt.savefig(identifier+"_MatrixPlot.png", dpi=500) # save as png
    plt.show()
    
"""
Example:
draw_MatrixPlot('NUP53',limit=50)

A = nx.adjacency_matrix(G)
print(A.todense())
"""
# Checking bidirectionality
def check_symmetric(a, tol=1e-8):
    return np.allclose(a, a.T, atol=tol, equal_nan=False)
#check_symmetric(B.todense())

def draw_weighted_graph(identifier, species=None, limit=100):
    result = creat_model_input(identifier, species, limit)
    G=nx.from_pandas_dataframe( result, 'interactor_A','interactor_B', 
                               [ 'score', 'nscore', 'fscore', 'pscore','hscore',
                                'ascore', 'escore', 'dscore', 'tscore'])
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if float(d['score']) >0.7]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if float(d['score']) <=0.7]
    pos=nx.random_layout(G) # positions for all nodes
    nx.draw_networkx_nodes(G,pos,node_size=80)# nodes
    nx.draw_networkx_edges(G,pos,edgelist=elarge,
                        width=0.5) 
    nx.draw_networkx_edges(G,pos,edgelist=esmall,
                        width=0.5,alpha=0.5,edge_color='b',style='dashed')
    nx.draw_networkx_labels(G,pos,font_size=3,font_family='sans-serif') # labels
    plt.axis('off')
    plt.savefig(identifier+"_weighted_graph.png", dpi=500) # save as png
    plt.show() # display
 
"""
Example:
draw_weighted_graph('NUP53', limit=30)
"""

