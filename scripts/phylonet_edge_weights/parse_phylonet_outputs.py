import sys

with open(sys.argv[1], "r+") as outfile:

    network_line = False

    for line in outfile:
        if line.startswith("("):
            print(line)
            
