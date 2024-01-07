import numpy as np
import networkx as nx
import random
import copy
from divide_network_based_random import Divide
from NMF_algorithm import nmf
from DNMF import dnmf
from add_edges_with_inner import inner_Add 
from add_edges_with_intro import intro_Add
from sklearn.decomposition import NMF
from scipy.sparse import csr_matrix

class ednmfa(object):
    def __init__(self, train_graph):
        self.G = train_graph
        self.R = 20
        self.γ = 0.6
        self.η = 0.1

    def training(self):
        train_A = nx.adjacency_matrix(self.G)
        reconstructed_Gs = [copy.deepcopy(self.G)] * self.R
        S_all = []

        DNMF_model = dnmf(train_A)
        DNMF_model.pre_training()
        S_1 = DNMF_model.training()

        for reconstructed_GA in reconstructed_Gs:

            G1_add_model = inner_Add(S_1, self.G, reconstructed_GA)
            reconstructed_GA = G1_add_model.add(self.γ, self.η)

            reconstructed_A = nx.adjacency_matrix(reconstructed_GA)
            #Similar = self.nmf(reconstructed_A) 

            Similar_model = nmf(reconstructed_A)
            Similar = Similar_model.training()
            S_all.append(Similar)

        sum_matrix = S_all[0]
        for matrix in S_all[1:]:
            sum_matrix += matrix
        S = 1/self.R * sum_matrix
        
        return S


    def nmf(self, matrix):
        nmf_model = NMF(n_components=25,
                   init="random",
                   random_state=42,
                   max_iter=300)
        W = nmf_model.fit_transform(csr_matrix(matrix))
        H = nmf_model.components_
        S = np.dot(W, H)
        return S
