import networkx as nx
import pandas as pd
import numpy as np
import time
from Parsers import HpoParser, PhenotypeAnnotationsParser

class genEdgeList():
    def __init__(self, enrich, output):
        self.hpos = HpoParser()
        self.hpos_df = pd.read_csv('./_data/hpo/hpo2int.csv', usecols=['Name', 'Id'])
        self.nodes = self.hpos_df.Id #getting all nodes
        self.hpos_dict = self.hpos_df.set_index('Name')['Id'].to_dict() #key pair values for fast mapping
        self.graph = nx.Graph() #empty graph
        self.graph.add_nodes_from(self.nodes) #introducing all nodes in hpo.csv
        self.enrich = enrich
        self.output = output
        t0 = time.time()
        '''
        for each phenotype in hpo.csv, get all its children and create edges
        (phenotype_i, children_j), but only if children exists in hpo.csv
        '''
        for term in self.hpos_df.Name:
            children = self.hpos.get_children(term)
            for name in children:
                if self.hpos_dict.get(name) is not None:
                    self.graph.add_edge(self.hpos_dict[term], self.hpos_dict[name])

        if self.enrich:
            anns = PhenotypeAnnotationsParser()
            t0 = time.time()
            dic = anns.orpha
            items = list(dic.keys())

            for id in items:
                before = len(self.graph.edges())
                print(dic[id]['hpos'])
                self.enrich_from_annotations(dic[id]['hpos'])
                lista = list(self.graph.edges())
                diff = len(self.graph.edges())-before
                print(diff, lista[(len(lista)-diff):])

        print(time.time() - t0)
        nx.readwrite.edgelist.write_edgelist(self.graph, self.output+'_.edgelist')

        f = open(self.output+'_.edgelist', "r") #I have to delete this file
        g = open(self.output+'.edgelist', "w")

        for line in f:
            g.write(line.replace("{}", ""))

        f.close()
        g.close()

    def enrich_from_annotations(self, array):
        if len(array) > 1 and self.hpos_dict.get(array[0]) is not None:
            for ix in range(1, len(array)):
                if self.hpos_dict.get(array[ix]) is not None:
                    self.graph.add_edge(self.hpos_dict[array[0]], self.hpos_dict[array[ix]])

        if len(array) > 1:
            array = np.delete(array, 0)
            self.enrich_from_annotations(array)


genEdgeList(enrich=True, output="./_data/graph/hp-obo-orpha")
