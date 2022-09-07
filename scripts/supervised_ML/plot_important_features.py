# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 11:58:24 2022

@author: Mark
"""

model = []
feature = []
importance = []

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

with open(
    'C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_results.txt', 'r') as results_file:
    
    current_model = ""
    
    for line in results_file:
        
        if "logistic regression model" in line:
            current_model = "logit"
        elif "SVM model" in line:
            current_model = "svm"
        elif "Gaussian Naive Bayes model" in line:
            current_model = "gnb"
        elif "decision tree model" in line:
            current_model = "dt"
        elif "random forest regression model" in line:
            current_model = "rf"
        
        splitline = line.split()
        
        if len(splitline) > 1 and splitline[0] != "Feature":
            if current_model == "logit":
                model.append("logit")
                feature.append(splitline[0])
                importance.append(splitline[1])
            elif current_model == "svm":
                model.append("svm")
                feature.append(splitline[0])
                importance.append(splitline[1])
            elif current_model == "gnb":
                model.append("gnb")
                feature.append(splitline[0])
                importance.append(splitline[1])
            elif current_model == "dt":
                model.append("dt")
                feature.append(splitline[0])
                importance.append(splitline[1])
            elif current_model == "rf":
                model.append("rf")
                feature.append(splitline[0])
                importance.append(splitline[1])
                
n_features = len(set(feature))
features = list(set(feature))

importance_matrix = [[0]*n_features,
                     [0]*n_features,
                     [0]*n_features,
                     [0]*n_features,
                     [0]*n_features]

for i in range(len(feature)):
    feature_index = features.index(feature[i])
    
    if model[i] == "logit":
        importance_matrix[0][feature_index] = float(importance[i])
    elif model[i] == "svm":
        importance_matrix[1][feature_index] = float(importance[i])
    elif model[i] == "gnb":
        importance_matrix[2][feature_index] = float(importance[i])
    elif model[i] == "dt":
        importance_matrix[3][feature_index] = float(importance[i])
    elif model[i] == "rf":
        importance_matrix[4][feature_index] = float(importance[i])

importance_sums = np.sum(np.array(importance_matrix), axis=0)

for i in range(len(importance_matrix)):
    importance_matrix[i] = [x for y, x in sorted(zip(importance_sums, importance_matrix[i]),
                                                 reverse=True)]

xticks = [x for y, x in sorted(zip(importance_sums, features), reverse=True)]
yticks = ["Logistic regression", "SVM", "Naive Bayes",
          "Decision tree", "Random forest"]
        
heatmap = sns.heatmap(importance_matrix, fmt = "g", 
                      xticklabels = xticks, yticklabels = yticks,
                      cmap = "viridis")
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation = 30)
heatmap.set_xticklabels(heatmap.get_xmajorticklabels(), fontsize = 15)
heatmap.set_yticklabels(heatmap.get_ymajorticklabels(), fontsize = 15)
plt.title("Feature importance for recovering species tree", fontsize = 20)

heatmap.show()
    

    
            
    
