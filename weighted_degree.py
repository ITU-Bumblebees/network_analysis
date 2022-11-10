import pandas as pd
import numpy as np
import networkx as nx

class WeightedDegrees:
    def __init__(self, nodelist, edgelist):
        self.nodelist = nodelist
        self.edgelist = edgelist
        self.G = self.makegraph()
        self.computeweighteddegrees()

    def makegraph(self):
        attributes= pd.read_csv(self.nodelist, delimiter=';')
        edgelist= pd.read_csv(self.edgelist,delimiter=';')
        g_attributes= attributes[attributes['0']=='gene']
        d_attributes = attributes[attributes['0']=='disease']

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
        return G

    def computeweighteddegrees(self):
        weighted_degrees = {}
        for gene in self.G.nodes:
            if self.G.nodes[gene]['0'] == 'gene':
                neighbours = self.G.neighbors(gene)
                for neighbour in neighbours:
                    if gene not in weighted_degrees:
                        weighted_degrees[gene] = 1/len(list(self.G.neighbors(neighbour)))
                    else:
                        weighted_degrees[gene] += 1/len(list(self.G.neighbors(neighbour)))
        print(weighted_degrees)


def main():
    nodepath = 'Data/nodeattribute.csv'
    edgepath = 'Data/edgelist.csv'
    w = WeightedDegrees(nodepath, edgepath)

if __name__ == '__main__':
    main()