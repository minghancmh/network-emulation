#!/bin/bash

# Generate the topologypdf, topologyjson, as well as the routing table
python ./topo-gen.py -c config -o output


echo "Topology generated. Check routing_tables.json for routing tables."
