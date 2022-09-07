# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:29:48 2022

@author: Mark
"""

import msprime
from ete3 import Tree
import numpy as np
import pandas as pd


### This script has tools for simulating training and test datasets

### Steps for msprime simulation: 
#1) Use demography.from_species_tree() to build a demographic model from
#an input Newick tree
#2) Add introgression to the demographic model
#3) Pass the demographic model into ancestry simulations to get tree sequences.
#Features of these tree sequences will then be used as inputs to the ML models


def sim_introgression(t1, t2, tm, delta, Ne, direction, sptree_top):
    
    ### Function to simulate introgression on a species tree
    ### using msprime. t1, t2, and tm are in units of generations.
    
    if sptree_top == "AB":
        sptree = "(C:" + str(t2) + ",(B:" + str(t1) + ",A:" + str(t1) + "):" + str(t2-t1) + ");"
    elif sptree_top == "BC":
        sptree = "(A:" + str(t2) + ",(B:" + str(t1) + ",C:" + str(t1) + "):" + str(t2-t1) + ");"

    demo = msprime.Demography.from_species_tree(sptree,
                                            initial_size = Ne)

    if direction == "P3 into P2":
        if sptree_top == "AB":
            demo.add_mass_migration(tm, source = "B",
                                    dest = "C", proportion = delta)
        elif sptree_top == "BC":
            demo.add_mass_migration(tm, source = "B",
                                    dest = "A", proportion = delta)
    elif direction == "P2 into P3":
        if sptree_top == "AB":
            demo.add_mass_migration(tm, source = "C",
                                    dest = "B", proportion = delta)
        elif sptree_top == "BC":
            demo.add_mass_migration(tm, source = "A",
                                    dest = "B", proportion = delta)
        
    demo.sort_events()

    ts_sims = msprime.sim_ancestry(samples = {"C":1, "B":1, "A":1},
                               demography = demo,
                               recombination_rate = 1e-8,
                               sequence_length = 1e7,
                               ploidy = 1)
    
    return ts_sims

def simulate_param_matrix(dim, direction, sptree):
    
    delta_vals = np.linspace(0.01, 0.9, dim)
    t1_vals = np.linspace(2000, 23000, dim)
    ts_sims = []
    
    #Simulates a matrix of parameter values 
    
    for i in range(len(delta_vals)):
        for j in range(len(t1_vals)):
            tm_vals = np.linspace(1, t1_vals[j], dim)
            for k in range(len(tm_vals)):
                ts_sims.append(sim_introgression(t1_vals[j], 24000, 
                                                 t1_vals[j] - tm_vals[k], 
                                                 delta_vals[i], 10000, 
                                                 direction, sptree))
        print("Finished iteration " + str(i+1) + 
              " out of " + str(len(delta_vals)))
                
    return ts_sims

def get_tree_topology(tree):
    
    #Gets the topology of a single gene tree 
    
    AB_dist = tree.get_distance("n2", "n1", topology_only = True)
    AC_dist = tree.get_distance("n2", "n0", topology_only = True)
    BC_dist = tree.get_distance("n1", "n0", topology_only = True)
    
    if AB_dist < AC_dist and AB_dist < BC_dist:
        return "AB"
    elif AC_dist < AB_dist and AC_dist < BC_dist:
        return "AC"
    else:
        return "BC"
    
def get_tree_freqs(trees):
    
    #Calculates topology frequencies for a set of gene trees 
    
    AB_count, AC_count, BC_count, total = 0, 0, 0, 0
    
    for tree in trees:
        
        top = get_tree_topology(tree)
        
        if top == "AB":
            AB_count += 1
        elif top == "AC":
            AC_count += 1
        elif top == "BC":
            BC_count += 1
            
        total += 1
        
    return [AB_count/total, AC_count/total, BC_count/total]
            
            
def get_tree_distances(tree, Ne):
    
    #Gets pairwise distances in a single gene tree
    
    topology = get_tree_topology(tree)
    
    AB_dist = tree.get_distance("n2", "n1", topology_only = False)/(2*Ne)
    AC_dist = tree.get_distance("n2", "n0", topology_only = False)/(2*Ne)
    BC_dist = tree.get_distance("n1", "n0", topology_only = False)/(2*Ne)
    
    
    return [topology, AB_dist, AC_dist, BC_dist]

def get_all_tree_distances(trees, Ne):
    
    #Gets pairwise distances and variances from a set of trees 
    
    AB_AB_dists, AB_AC_dists, AB_BC_dists = [], [], []
    AC_AB_dists, AC_AC_dists, AC_BC_dists = [], [], []
    BC_AB_dists, BC_AC_dists, BC_BC_dists = [], [], []    
    
    for tree in trees:
        
        dists = get_tree_distances(tree, Ne)
        
        if dists[0] == "AB":
            AB_AB_dists.append(dists[1])
            AB_AC_dists.append(dists[2])
            AB_BC_dists.append(dists[3])
        elif dists[0] == "AC":
            AC_AB_dists.append(dists[1])
            AC_AC_dists.append(dists[2])
            AC_BC_dists.append(dists[3])
        elif dists[0] == "BC":
            BC_AB_dists.append(dists[1])
            BC_AC_dists.append(dists[2])
            BC_BC_dists.append(dists[3])
    
    mean_dists = [np.mean(AB_AB_dists), np.mean(AB_AC_dists), 
                  np.mean(AB_BC_dists), np.mean(AC_AB_dists),
                  np.mean(AC_AC_dists), np.mean(AC_BC_dists),
                  np.mean(BC_AB_dists), np.mean(BC_AC_dists), 
                  np.mean(BC_BC_dists)]
    
    var_dists = [np.var(AB_AB_dists), np.var(AB_AC_dists), 
                  np.var(AB_BC_dists), np.var(AC_AB_dists),
                  np.var(AC_AC_dists), np.var(AC_BC_dists),
                  np.var(BC_AB_dists), np.var(BC_AC_dists), 
                  np.var(BC_BC_dists)]
    
    return mean_dists, var_dists
        

def get_tree_features(ts_sims, Ne):
    
    #Gets full set of features for a single observation
    
    genetrees_newick = []

    for tree in ts_sims.trees():
        genetrees_newick.append(tree.as_newick())
        
    #Thin gene trees to reduce autocorrelation
    genetrees_newick = genetrees_newick[0::3]
    
    genetrees_newick = [Tree(tree) for tree in genetrees_newick]
    
    freqs = get_tree_freqs(genetrees_newick)
    mean_dists, var_dists = get_all_tree_distances(genetrees_newick, Ne)
    
    obs = freqs + mean_dists + var_dists
    
    return obs

def get_feature_df(ts_sim_list, Ne, sptree_top):
    
    #Get dataframe with features across all observations 
    
    feature_array = []
    
    for i, sim in enumerate(ts_sim_list):
        sim_obs = get_tree_features(sim, Ne)
        sim_obs.append(sptree_top)
        feature_array.append(sim_obs)
        print("Finished iteration " + str(i) + 
              " out of " + str(len(ts_sim_list)))
    
    feature_cols = ["AB_freq", "AC_freq", "BC_freq", "AB_AB_dist",
                    "AB_AC_dist", "AB_BC_dist", "AC_AB_dist", "AC_AC_dist",
                    "AC_BC_dist", "BC_AB_dist", "BC_AC_dist", "BC_BC_dist",
                    "AB_AB_var","AB_AC_var", "AB_BC_var", "AC_AB_var", 
                    "AC_AC_var", "AC_BC_var", "BC_AB_var", "BC_AC_var", 
                    "BC_BC_var", "sptree"]
    
    feature_df = pd.DataFrame(feature_array, columns = feature_cols)
    
    return feature_df


