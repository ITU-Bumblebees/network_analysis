# graph as an input
# give list of which nodes to delete as input
# delete based on list, make projection, homophily per class, community 

from Graph import Graph
from collections import defaultdict
import numpy as np
import pandas as pd 
import networkx as nx 
from networkx.algorithms import bipartite 
from sklearn.metrics import normalized_mutual_info_score
import networkx.algorithms.community as nx_comm
from networkx.algorithms.community import greedy_modularity_communities



class GraphAnalysis:
    def __init__(self, G, nodes, d_nodes):
        """
        Inputs:
        --------------
        G: Graph object
        nodes: list of the nodes that we want removed (could be top 20)
        """
        self.G = G 
        self.nodes = nodes  
        self.d_nodes = d_nodes
        
    def final_analysis(self) -> pd.DataFrame:
        """
        Outputs:
        -------------
        df_homophily: data frame with the classes as columns and the homophily as value,
                      one row per iteration
        df_community: data frame with ...
        largest_component: list with the probability of being in the largest component for each iteration
        diameter: list of the diameter for each iteration
        """
        self.homophily_dict = defaultdict(list)
        self.comm_dict = defaultdict(list)
        
    
        largest_component = list()
        diameter = []
        for i in range(len(self.nodes)):
            # remove node
            self.G.remove_node(self.nodes[i])
            Gp = bipartite.weighted_projected_graph(self.G, self.d_nodes)
            # get prob of being in largest component
            largest_component.append(len(max(nx.connected_components(Gp), key = len)) / len(Gp.nodes))    
            # do homophily
            self.homophily_per_group(Gp) # dict of lists
            # do community discovery
            self.greedy_community(Gp)
            # computing diameter 
            #diameter.append(nx.diameter(Gp))   

        df_community = pd.DataFrame(self.comm_dict)    
        df_homophily = pd.DataFrame(self.homophily_dict)
        
        return df_homophily, df_community, largest_component #diameter
        
    def homophily_per_group(self, Gp):
        """
        Calculates the homophily of a graph
        Returns a dictionary of diseases and their homophily values
        """
        types_diseases = defaultdict(list)
        for node in Gp.nodes():
            group = Gp.nodes[node]['1']
            count = 0 
            num_neighbors= len([Gp.neighbors(node)]) 
            for n_node in list(Gp.neighbors(node)):
                n_group= Gp.nodes[n_node]['1']
                
                if group == n_group: 
                    count +=1
                    
            types_diseases[group].append(count/num_neighbors)
            
        for key,val in types_diseases.items():
            value = sum(val) / len(val)
            types_diseases.update({key: value})
            self.homophily_dict[key].append(value)


        
    def greedy_community(self, Gp):
        """
        Computes the greedy modularity of a Graph object,
        Returns a list of lists with [node, label, real label]
        """

        c = greedy_modularity_communities(Gp)

        expected = pd.DataFrame(Gp.nodes())
        expected["color"]= 0
        expected.columns = ["node", "group_num"]
        expected['nodes']= Gp.nodes()

        exp = expected.set_index("node")

        for i, lst in enumerate(c):
            for nod in list(lst):
                exp.loc[nod]['group_num'] = i

        groups= []
        for node in exp['nodes']:
            groups.append(Gp.nodes[node]['1'])
        exp['group']= groups 
        
        NMI = normalized_mutual_info_score(exp['group_num'], exp['group'])
        modularity = nx_comm.modularity(Gp, c)
        
        self.comm_dict['nmi'].append(NMI)
        self.comm_dict['modularity'].append(modularity)


if __name__ == '__main__':
    G, d_nodes = Graph().get_bipartite_graph()
    nodes = [3854, 3653, 3875, 2569, 3913, 3943, 3609, 3555, 3706, 2120, 2568, 3192, 3851, 3164, 3803, 3759, 3831, 3958, 3821, 2434]
    ga = GraphAnalysis(G, nodes, d_nodes)
    print(ga.final_analysis())