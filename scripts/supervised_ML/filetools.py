# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:29:48 2022

@author: Mark
"""

import numpy as np
import pandas as pd

### This script has tools for handling file inputs and outputs 

def write_model_output(filepath, importance_scores, accuracy_scores): 
    
    #Writes model accuracy scores and feature importance scores
    #to file
    
    model_results = open(filepath, 'w')
    
    model_lines = ["Logistic regression: " + str(accuracy_scores[0]) + "\n",
                   "SVM: " + str(accuracy_scores[1]) + "\n",
                   "Gaussian Naive Bayes: " + str(accuracy_scores[2]) + "\n",
                   "Decision tree: " + str(accuracy_scores[3]) + "\n",
                   "Random forest: " + str(accuracy_scores[4]) + "\n"]
    
    model_results.write("Performance of models on test set:\n")
    model_results.write("\n")
    model_results.writelines(model_lines)
    model_results.write("\n")
    
    model_results.write("Feature importance for logistic regression model:\n")
    model_results.write("\n")
    model_results.writelines(importance_scores[0])
    model_results.write("\n")

    model_results.write("Feature importance for SVM model:\n")
    model_results.write("\n")
    model_results.writelines(importance_scores[1])
    model_results.write("\n")

    model_results.write("Feature importance for Gaussian Naive Bayes model:\n")
    model_results.write("\n")
    model_results.writelines(importance_scores[2])
    model_results.write("\n")

    model_results.write("Feature importance for decision tree model:\n")
    model_results.write("\n")
    model_results.writelines(importance_scores[3])
    model_results.write("\n")

    model_results.write("Feature importance for random forest regression model:\n")
    model_results.write("\n")
    model_results.writelines(importance_scores[4])
    model_results.write("\n")
    
    model_results.close()
    
def write_simulation_params(filepath, dim):
    
    #Writes the parameters used to generate the simulated data to a
    #csv file 
    
    delta_vals = np.linspace(0.01, 0.9, dim)
    t1_vals = np.linspace(2000, 23000, dim)
    
    delta_list = []
    t1_list = []
    tm_list = []
    
    for i in range(len(delta_vals)):
        for j in range(len(t1_vals)):
            tm_vals = np.linspace(1, t1_vals[j], dim)
            for k in range(len(tm_vals)):
                delta_list.append(delta_vals[i])
                t1_list.append(t1_vals[j])
                tm_list.append(t1_vals[j] - tm_vals[k])
                
    direction = np.repeat("P3 into P2", len(delta_list))
    other_direction = np.repeat("P2 into P3", len(delta_list))
    
    sptree = np.repeat("AB", len(delta_list))
    other_sptree = np.repeat("BC", len(delta_list))
    
    dir_list = []
    dir_list.extend([direction, other_direction, direction, other_direction])
    dir_list = [x for xs in dir_list for x in xs]
    sptree_list = []
    sptree_list.extend([sptree, sptree, other_sptree, other_sptree])
    sptree_list = [x for xs in sptree_list for x in xs]
    
    delta_list = [delta_list*4][0]
    t1_list = [t1_list*4][0]
    tm_list = [tm_list*4][0]
    
    params_df = np.transpose(np.array([delta_list, t1_list, tm_list, dir_list, sptree_list]))
    
    params_df = pd.DataFrame(params_df,
                             columns = ["delta", "t1", "tm", "dir", "sptree"])
    
    params_df.to_csv(filepath)
    
    
    
    
    
    
    
    
    
                
    
                
    
    
    
    