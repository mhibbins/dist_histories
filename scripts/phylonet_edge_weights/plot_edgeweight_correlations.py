# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:03:05 2022

@author: Mark
"""
import re
from ete3 import Tree
import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

### Read in network files 

P2intoP3_displayed = []
P3intoP2_displayed = []

with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/branchingorder_methods_test/method_outputs/phylonet_outputs/P2intoP3_phylonet_displayed_trees.txt", 'r') as P2intoP3_file:
    for line in P2intoP3_file:
        if len(line.strip()) > 0:
            P2intoP3_displayed.append(line.strip())
        
with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/branchingorder_methods_test/method_outputs/phylonet_outputs/P3intoP2_phylonet_displayed_trees.txt", 'r') as P3intoP2_file:
    for line in P3intoP2_file:
        if len(line.strip()) > 0:
            P3intoP2_displayed.append(line.strip())
            
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
P2intoP3_displayed = chunks(P2intoP3_displayed, 4)
P3intoP2_displayed = chunks(P3intoP2_displayed, 4)
        
### Function to get introgression edge weight from displayed trees 

def get_tree_topology(newick_str):
    
    tree = Tree(newick_str)
    
    #Gets the topology of a single gene tree 
    
    AB_dist = tree.get_distance("A", "B", topology_only = True)
    AC_dist = tree.get_distance("A", "C", topology_only = True)
    BC_dist = tree.get_distance("B", "C", topology_only = True)
    
    if AB_dist < AC_dist and AB_dist < BC_dist:
        return "AB"
    elif AC_dist < AB_dist and AC_dist < BC_dist:
        return "AC"
    else:
        return "BC"
    

def get_estimated_delta(network_info):
    
    if network_info[0] == "One displayed tree":
        if get_tree_topology(network_info[1]) == "AB":
            return 0
        elif get_tree_topology(network_info[1]) == "BC":
            return 1
        else:
            return None
    else:
        minor_edge_weight = float(re.findall("\d+\.\d+", network_info[3])[0])
        
        if get_tree_topology(network_info[2]) == "BC":
            return 1 - minor_edge_weight
        elif get_tree_topology(network_info[0]) == "BC" or get_tree_topology(network_info[1]) == "BC":
                return minor_edge_weight
        else:
            return None
        
P2intoP3_deltas = []
P3intoP2_deltas = []

for network in P2intoP3_displayed:
    delta = get_estimated_delta(network)
    P2intoP3_deltas.append(delta)
    
for network in P3intoP2_displayed:
    delta = get_estimated_delta(network)
    P3intoP2_deltas.append(delta)
    
### Get simulated delta values and gene tree freqs

sim_deltas = []

with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_params.csv", 'r') as params_file:
    params_reader = csv.reader(params_file)
    for row in params_reader:
        if row[5] == "AB":
            sim_deltas.append(float(row[1]))
            
sim_deltas = sim_deltas[0:999]
sim_deltas = [round(num, 1) for num in sim_deltas]
            
sim_BC_freqs = []
            
with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_features.csv", 'r') as features_file:
    features_reader = csv.reader(features_file)
    for row in features_reader:
        if row[3] != "BC_freq" and row[-1] == "AB":
            sim_BC_freqs.append(float(row[3]))

P3intoP2_BC_freqs = sim_BC_freqs[0:999]
P2intoP3_BC_freqs = sim_BC_freqs[1000:1999]

### Plot results 

P3intoP2_df = pd.DataFrame(list(zip(P3intoP2_deltas, sim_deltas, 
                                    P3intoP2_BC_freqs)),
                           columns = ["estimated_delta", "simulated_delta",
                                      "simulated_BC_frequency"])

P2intoP3_df = pd.DataFrame(list(zip(P2intoP3_deltas, sim_deltas, 
                                    P2intoP3_BC_freqs)),
                           columns = ["estimated_delta", "simulated_delta",
                                      "simulated_BC_frequency"])

sns.set_theme(style="whitegrid")
            
ax1 = sns.boxplot(x="simulated_delta", y="estimated_delta", 
                  data = P3intoP2_df)
ax1.set(ylim=(-0.1,1.1))
plt.clf()
ax2 = sns.boxplot(x="simulated_delta", y="estimated_delta", 
                  data = P2intoP3_df)
ax2.set(ylim=(-0.1,1.1))
plt.clf()
ax3 = sns.boxplot(x="simulated_delta", y="simulated_BC_frequency", 
                  data = P2intoP3_df)
ax3.set(ylim=(-0.1,1.1))
plt.clf()
ax4 = sns.boxplot(x="simulated_delta", y="simulated_BC_frequency", 
                  data = P3intoP2_df)
ax4.set(ylim=(-0.1,1.1))
            
        
        
        
        
                


    