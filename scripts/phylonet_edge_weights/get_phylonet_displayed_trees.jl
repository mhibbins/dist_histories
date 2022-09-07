using PhyloNetworks;

networks = readMultiTopology(ARGS[1])

displayed_trees = displayedTrees(networks[1], 0.0)
major_tree = displayedTrees(networks[1], 0.5)
minor_edge = PhyloNetworks.minorreticulationgamma(networks[3])

for network in networks
	displayed_trees = displayedTrees(network, 0.0)
	major_tree = displayedTrees(network, 0.5)
	minor_edge = PhyloNetworks.minorreticulationgamma(network)

	if length(displayed_trees) == 1
		print("One displayed tree")
		print("\n")
		print(writeTopology(displayed_trees[1]))
		print("\n")
		print("Ignore")
		print("\n")
		print("Ignore")
		print("\n")
	else
		print(writeTopology(displayed_trees[1]))
		print("\n")
		print(writeTopology(displayed_trees[2]))
		print("\n")
		print(writeTopology(major_tree[1]))
		print("\n")
		print(minor_edge)
		print("\n")
	end
end

# print(displayedTrees(networks[3], 0.0))
# test_displayed = displayedTrees(networks[3], 0.0)
# print(PhyloNetworks.minorreticulationgamma(networks[3]))
# for network in networks
# 	print(displayedTrees(network, 0.0))
# end
