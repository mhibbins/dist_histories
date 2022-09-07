#!/bin/sh

python3 sim_genetrees.py 10 P3intoP2 AB 10dim_sims/10dim_P3intoP2_AB
python3 sim_genetrees.py 10 P3intoP2 BC 10dim_sims/10dim_P3intoP2_BC
python3 sim_genetrees.py 10 P2intoP3 AB 10dim_sims/10dim_P2intoP3_AB
python3 sim_genetrees.py 10 P2intoP3 BC 10dim_sims/10dim_P2intoP3_BC

cp -r ../branchingorder_methods_test/ /mnt/c/Users/18126/OneDrive\ -\ University\ of\ Toronto/Projects/sp_branching_order/

