# dist_histories
Code and data for Hibbins and Hahn 2022, "Distinguishing between histories of speciation and introgression using genomic data". See below for a description of the directory structures and relevant files.

# datasets 
## phylonet_edge_weights
Contains estimated networks (phylonet.txt) and displayed trees (phylonet_displayed.txt) estimated by PhyloNet for each combination of simulation parameters. The simulated direction of introgression is indicated as "P3intoP2" (C into B or A into B) and "P2intoP3" (B into C or B into A). The species tree used to simulate the data is indicated with "AB" for the tree ((A,B),C) and "BC" for the tree ((B,C),A). 

## supervised_ML
Contains the simulated features given as input to machine learning models (features.csv), the parameters used to simulate those features (params.csv), and a text file with accuracy and feature importance scores for each model (results.txt)

# scripts
**ML_logit_stepwise.R** - script to perform stepwise model selection for logistic regression on our simulated features.
## phylonet_edge_weights
These scripts were used to assess the ability of PhyloNet to accurately estimate edge weights under a known history of introgression. Used to generate the results in Figure 7.

**branchingorder_methods_test_pipeline.sh** - pipeline which simulates gene trees under each combination of parameters and writes the output files to a local directory.

**get_phylonet_displayed_trees.jl** - Julia script which extracts the displayed trees from a network estimated by phylonet. 

**make_phylonet_inputs.sh** - Pipeline which creates input NEXUS files for phylonet from simulated data under all parameter combinations.

**make_phylonet_nexus.py** - Creates a single phylonet input file from a simulated gene tree dataset. 

**parse_phylonet_outputs.py** - Parses the estimated network from a phylonet output file.

**plot_edgeweight_correlations.py** - Plots results of the analysis. Generated Figure 7.

**plot_prop_incorrect_tree.py** - Plots the proportion of cases where PhyloNet returned the wrong strictly bifurcating tree. Generated Supplementary Figure 5. 

**run_phylonet.sh** - Pipeline to run phylonet on all files across parameter combinations. 

**sim_genetrees.py** - Simulates gene tree datasets for input to phylonet.

## supervised_ML
These scripts were used for the supervised machine learning analyses. Generated the results in Table 1 and Figures 5 and 6. 

**filetools.py** - module for the ML analysis containing tools for file inputs and outputs.

**main.py** - main script for the ML analysis.

**modeltools.py** - module for the ML analysis containing tools for fitting and interpreting ML models.

**plot_important_features.py** - plots the results of the feature permutation analysis, used to generate Figure 5. 

**plot_important_variable_behavior.R** - plots the behavior of the most informative features, used to generate Figure 6 and Supplementary Figure 4.

**simtools.py** - module for the ML analysis containing tools for simulating training datasets. 

## theory
These scripts were used for the theory analyses. Generated the results in Figures 3 and 4. 

**min_node_heights.R** - theory for minimum node heights in gene trees. Generated Figure 4 and Supplementary Figure 3. 

**plot_mindelta_anomaly.R** - theory for minimum delta for gene tree frequencies. Used to generate Figure 3A. 

**plot_mindelta_parsimony.R** - theory for minimum delta for biallelic sites. Used to generate Figure 3B. 

**plot_parsimony_vs_quartets.R** - difference between gene tree frequencies and biallelic sites. Used to generate Figure 3C. 

**plot_quartet_method_space.R** - plots gene tree minimum node height as a 3D surface. Used to generate Supplementary Figure 2. 

