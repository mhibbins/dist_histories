#!/bin/sh

for i in {1..1000}
do
python3 make_phylonet_nexus.py 10dim_sims/10dim_P3intoP2_AB_$i.txt phylonet_inputs/10dim_P3intoP2_AB_$i.nex
python3 make_phylonet_nexus.py 10dim_sims/10dim_P3intoP2_BC_$i.txt phylonet_inputs/10dim_P3intoP2_BC_$i.nex
python3 make_phylonet_nexus.py 10dim_sims/10dim_P2intoP3_AB_$i.txt phylonet_inputs/10dim_P2intoP3_AB_$i.nex
python3 make_phylonet_nexus.py 10dim_sims/10dim_P2intoP3_BC_$i.txt phylonet_inputs/10dim_P2intoP3_BC_$i.nex
echo "Finished replicate $i out of 1000"
done
