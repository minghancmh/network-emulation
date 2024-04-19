#!/bin/bash

# Generate the topologypdf, topologyjson, as well as the routing table
python ./topo-gen.py -c config -o output
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to generate topology and routing tables.\033[0m"
    exit 1
fi

echo "Topology generated. Check routing_tables.json for routing tables."
