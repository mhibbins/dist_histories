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

with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/branchingorder_phylonet_test/method_outputs/phylonet_outputs/P2intoP3_phylonet_displayed_trees.txt", 'r') as P2intoP3_file:
    for line in P2intoP3_file:
        if len(line.strip()) > 0:
            P2intoP3_displayed.append(line.strip())
        
with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/branchingorder_phylonet_test/method_outputs/phylonet_outputs/P3intoP2_phylonet_displayed_trees.txt", 'r') as P3intoP2_file:
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
    

def get_wrongtree_cases(network_info):
    
    if network_info[0] == "One displayed tree":
        if get_tree_topology(network_info[1]) == "AB":
            return 0
        elif get_tree_topology(network_info[1]) == "AC":
            return 0
        elif get_tree_topology(network_info[1]) == "BC":
            return 1
    else:
        return 0

        
P2intoP3_wrongs = []
P3intoP2_wrongs = []

for network in P2intoP3_displayed:
    delta = get_wrongtree_cases(network)
    P2intoP3_wrongs.append(delta)
    
for network in P3intoP2_displayed:
    delta = get_wrongtree_cases(network)
    P3intoP2_wrongs.append(delta)
    
P2intoP3_wrongs = chunks(P2intoP3_wrongs, 100)
P3intoP2_wrongs = chunks(P3intoP2_wrongs, 100)

P2intoP3_propwrong = []
P3intoP2_propwrong = []

for chunk in P2intoP3_wrongs:
    propwrong = sum(chunk)/len(chunk)
    P2intoP3_propwrong.append(propwrong)
    
for chunk in P3intoP2_wrongs:
    propwrong = sum(chunk)/len(chunk)
    P3intoP2_propwrong.append(propwrong)
    
### Get simulated delta values

sim_deltas = []

with open("C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_params.csv", 'r') as params_file:
    params_reader = csv.reader(params_file)
    for row in params_reader:
        if row[5] == "AB":
            sim_deltas.append(float(row[1]))
            
sim_deltas = sim_deltas[0:999]
sim_deltas = [round(num, 1) for num in sim_deltas]
sim_deltas = list(set(sim_deltas))
            
### Plot results 

P3intoP2_df = pd.DataFrame(list(zip(P3intoP2_propwrong, sim_deltas)),
                           columns = ["prop_wrong", "simulated_delta"])

P2intoP3_df = pd.DataFrame(list(zip(P2intoP3_propwrong, sim_deltas)),
                           columns = ["prop_wrong", "simulated_delta"])

sns.set_theme(style="whitegrid")
            
ax1 = sns.barplot(x="simulated_delta", y="prop_wrong", 
                  data = P3intoP2_df)
#ax1.set(ylim=(-0.1,1.1))
plt.clf()
ax2 = sns.barplot(x="simulated_delta", y="prop_wrong", 
                  data = P2intoP3_df)
#ax2.set(ylim=(-0.1,1.1))

            
        
        
        
        
                


    