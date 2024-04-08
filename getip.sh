#!/bin/bash

# This executable outputs an ipaddr.json file for use by applyRoutingTable.sh. This file gets the ip of all nodes, and puts them in a 
# json file with key=name, value=ip.

# check if nodes exist first
if ! kubectl get nodes -o wide | grep "test-cluster" > /dev/null; then
    echo "No nodes starting with test-cluster. Have you run kind create cluster?"
    exit 1
fi

# Generate nodes.txt file from kubectl info
kubectl get nodes -o wide > nodes.txt

# Run the parser on it to get the file
python3 ./kubNodesInfoParser.py -n nodes.txt

# Remove files starting with 'output'
rm -f nodes.txt

echo "Look in ipaddr.json to get node ip"
