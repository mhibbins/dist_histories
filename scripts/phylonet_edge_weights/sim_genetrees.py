# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:29:48 2022

@author: Mark
"""

import msprime
from ete3 import Tree
import numpy as np
import pandas as pd
import re
import sys

def sim_introgression(t1, t2, tm, delta, Ne, direction, sptree_top):
    
    ### Function to simulate introgression on a species tree
    ### using msprime. t1, t2, and tm are in units of generations.
    
    if sptree_top == "AB":
        sptree = "(C:" + str(t2) + ",(B:" + str(t1) + ",A:" + str(t1) + "):" + str(t2-t1) + ");"
    elif sptree_top == "BC":
        sptree = "(A:" + str(t2) + ",(B:" + str(t1) + ",C:" + str(t1) + "):" + str(t2-t1) + ");"

    demo = msprime.Demography.from_species_tree(sptree,
                                            initial_size = Ne)

    if direction == "P3intoP2":
        if sptree_top == "AB":
            demo.add_mass_migration(tm, source = "B",
                                    dest = "C", proportion = delta)
        elif sptree_top == "BC":
            demo.add_mass_migration(tm, source = "B",
                                    dest = "A", proportion = delta)
    elif direction == "P2intoP3":
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

def convert_units(tree):

    oldlengths = re.findall("\d+\.\d+", tree)
    newlengths = [str(float(oldlength)/20000) for oldlength in oldlengths]

    for i in range(len(oldlengths)):
        tree = tree.replace(oldlengths[i], newlengths[i])

    return tree


def write_sims_to_newick(ts_sims):

    genetrees_newick = []

    for treeset in ts_sims:
        trees = []

        for tree in treeset.trees():

            genetree = str(tree.as_newick())
            genetree = genetree.replace("n2", "A")
            genetree = genetree.replace("n1", "B")
            genetree = genetree.replace("n0", "C")
            trees.append(genetree)
    
        trees = trees[0::3]

        for i, genetree in enumerate(trees):
            newtree = convert_units(genetree)
            trees[i] = newtree

        genetrees_newick.append(trees)

    return genetrees_newick 

def write_newick_trees_to_file(newick_trees, outpath_prefix):

    for i, treeset in enumerate(newick_trees):
        outpath = outpath_prefix + "_" + str(i) + ".txt"

        genetree_file = open(outpath, 'w')

        for genetree in treeset:
            genetree_file.write(str(genetree) + "\n")

        genetree_file.close()

test_sims = simulate_param_matrix(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
test_newick_trees = write_sims_to_newick(test_sims)
test_newick_file = write_newick_trees_to_file(test_newick_trees, str(sys.argv[4]))




