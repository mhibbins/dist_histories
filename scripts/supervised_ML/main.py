# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:12:32 2022

@author: Mark
"""

import simtools 
import modeltools
import pandas as pd
import filetools

dim = 10

### Simulate datasets 

print("Simulating datasets...")

ts_sim_list = [simtools.simulate_param_matrix(dim, "P3 into P2", "AB"),
               simtools.simulate_param_matrix(dim, "P2 into P3", "AB"),
               simtools.simulate_param_matrix(dim, "P3 into P2", "BC"),
               simtools.simulate_param_matrix(dim, "P2 into P3", "BC")]

#Get dataframe of features 

print("Parsing features...")

ts_sim_features = [simtools.get_feature_df(ts_sim_list[0], 10000, "AB"),
                   simtools.get_feature_df(ts_sim_list[1], 10000, "AB"),
                   simtools.get_feature_df(ts_sim_list[2], 10000, "BC"),
                   simtools.get_feature_df(ts_sim_list[3], 10000, "BC")]

ts_sim_features = pd.concat(ts_sim_features)

### Fit models 

print("Fitting models...")

models, scores, X_test, y_test = modeltools.fit_models(ts_sim_features)

print("Getting feature importance...")

importance_lines = [modeltools.get_feature_importance(models[0], X_test, y_test),
                    modeltools.get_feature_importance(models[1], X_test, y_test),
                    modeltools.get_feature_importance(models[2], X_test, y_test),
                    modeltools.get_feature_importance(models[3], X_test, y_test),
                    modeltools.get_feature_importance(models[4], X_test, y_test)]

print("Writing output files...")

filetools.write_model_output('C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/branchingorder_ML_results.txt', 
                             importance_lines, scores)

ts_sim_features.to_csv('C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/branchingorder_ML_features.csv')

filetools.write_simulation_params('C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/branchingorder_ML_params.csv', dim)



