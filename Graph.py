import pandas as pd
import numpy as np

import networkx as nx
from networkx.algorithms import bipartite 


def read_data():
    #read the data provided
    attributes= pd.read_csv('Data/nodeattribute.csv', delimiter=';')
    edgelist= pd.read_csv('Data/edgelist.csv',delimiter=';')

    #attributes list
    g_attributes= attributes[attributes['0']=='gene']
    d_attributes = attributes[attributes['0']=='disease']


    #attributes stored as a dictionary
    nodes_attr = attributes.set_index('Id').to_dict(orient='index')
    g_nodes_attr = g_attributes.set_index('Id').to_dict(orient='index')
    d_nodes_attr= d_attributes.set_index('Id').to_dict(orient='index')


    g_nodes= g_attributes['Id'].to_list()
    d_nodes=d_attributes['Id'].to_list()
    edges= edgelist.values.tolist()


    G = nx.Graph()
    G.add_nodes_from(g_nodes, bipartite=0)
    G.add_nodes_from(d_nodes, bipartite=1)
    nx.set_node_attributes(G, nodes_attr)
    G.add_edges_from(edges)

    Gp = bipartite.weighted_projected_graph(G, d_nodes)

    return Gp
