#!/bin/sh

for i in {1..1000}
do
java -jar $PHYLONET PhyloNet.jar phylonet_inputs/10dim_P3intoP2_AB_$i.nex > method_outputs/phylonet_outputs/10dim_P3intoP2_AB_result_$i.txt
java -jar $PHYLONET PhyloNet.jar phylonet_inputs/10dim_P3intoP2_BC_$i.nex > method_outputs/phylonet_outputs/10dim_P3intoP2_BC_result_$i.txt
java -jar $PHYLONET PhyloNet.jar phylonet_inputs/10dim_P2intoP3_AB_$i.nex > method_outputs/phylonet_outputs/10dim_P2intoP3_AB_result_$i.txt
java -jar $PHYLONET PhyloNet.jar phylonet_inputs/10dim_P2intoP3_BC_$i.nex > method_outputs/phylonet_outputs/10dim_P2intoP3_BC_result_$i.txt
echo "Finished replicate $i out of 1000"
done
