import pandas as pd
import numpy as np

import networkx as nx
from networkx.algorithms import bipartite 

class Graph:
    def __init__(self):
        #read the data from the csv file
        self.attributes= pd.read_csv('Data/nodeattribute.csv', delimiter=';') #the dataframe with all the attributes
        self.edgelist= pd.read_csv('Data/edgelist.csv',delimiter=';')

        #make two lists of the attributes: one for genes and one for diseases
        self.g_attributes= self.attributes[self.attributes['0']=='gene'] #gene attributes
        self.d_attributes = self.attributes[self.attributes['0']=='disease'] #disease attributes

        #attributes but stored as a dictionary
        self.attributes_dict = self.attributes.set_index('Id').to_dict(orient='index') #dictionary with attributes
        self.g_nodes_attr = self.g_attributes.set_index('Id').to_dict(orient='index') #gene attributes as a dictionary
        self.d_nodes_attr= self.d_attributes.set_index('Id').to_dict(orient='index') #disease attributes as a dictionary

        self.g_nodes= self.g_attributes['Id'].to_list()
        self.d_nodes= self.d_attributes['Id'].to_list()
        self.edges= self.edgelist.values.tolist()

    def get_bipartite_graph(self):
        #create a bipartite graph
        self.G = nx.Graph()
        self.G.add_nodes_from(self.g_nodes, bipartite=0)
        self.G.add_nodes_from(self.d_nodes, bipartite=1)
        nx.set_node_attributes(self.G, self.attributes_dict)
        self.G.add_edges_from(self.edges)

        return self.G

    def get_projected_graph_deseases(self):
        G = self.get_bipartite_graph()
        return bipartite.weighted_projected_graph(G, self.d_nodes)

    def get_projected_graph_genes(self):
        G = self.get_bipartite_graph()
        return bipartite.weighted_projected_graph(G, self.g_nodes)

    def get_attributes(self):
        return self.attributes

