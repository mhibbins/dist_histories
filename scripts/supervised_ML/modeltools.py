# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:04:44 2022

@author: Mark
"""

from sklearn.linear_model import LogisticRegression 
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.inspection import permutation_importance

### This script has tools for training, validating,
### and interpreting models on the simulated datasets. 
### Trying logistic regression, SVM, decision tree / random forest, 
### and Naive Bayes 

def fit_models(sims):
    
    #Creates training and test datasets, then fits models
    
    X = sims.drop(["sptree"], axis = 1)
    y = sims["sptree"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size = 0.25)
    
    #Feature scaling
    
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    #Models 
    
    branchingorder_logit = LogisticRegression().fit(X_train, y_train)
    branchingorder_svm = SVC().fit(X_train, y_train)
    branchingorder_nb = GaussianNB().fit(X_train, y_train)
    branchingorder_dt = DecisionTreeClassifier().fit(X_train, y_train)
    branchingorder_rf = RandomForestClassifier().fit(X_train, y_train)
    
    branchingorder_models = [branchingorder_logit, branchingorder_svm,
                             branchingorder_nb, branchingorder_dt, 
                             branchingorder_rf]
    
    #Scores 
    
    branchingorder_scores = []
    
    branchingorder_scores.extend([branchingorder_logit.score(X_test, y_test),
                                branchingorder_svm.score(X_test, y_test),
                                branchingorder_nb.score(X_test, y_test),
                                branchingorder_dt.score(X_test, y_test),
                                branchingorder_rf.score(X_test, y_test)])
    
    return branchingorder_models, branchingorder_scores, X_test, y_test

def get_feature_importance(model, X_test, y_test):
    
    importance_lines = []
    #Gets the feature weights from a model
    
    feature_cols = ["AB_freq", "AC_freq", "BC_freq", "AB_AB_dist",
                    "AB_AC_dist", "AB_BC_dist", "AC_AB_dist", "AC_AC_dist",
                    "AC_BC_dist", "BC_AB_dist", "BC_AC_dist", "BC_BC_dist",
                    "AB_AB_var","AB_AC_var", "AB_BC_var", "AC_AB_var", 
                    "AC_AC_var", "AC_BC_var", "BC_AB_var", "BC_AC_var", 
                    "BC_BC_var", "sptree"]
    
    r = permutation_importance(model, X_test, y_test,
                               n_repeats = 30, random_state = 0)
    
    for i in r.importances_mean.argsort()[::-1]:
        if r.importances_mean[i] - 2 * r.importances_std[i] > 0:
            importance_lines.append(str(feature_cols[i]) + " " + 
                                    str(r.importances_mean[i]) + " " + 
                                    "+/- " + str(r.importances_std[i]) + 
                                    "\n")
    
    return importance_lines
 
            
    
            
    
    
    
    
    
    
    
    
    