#!/bin/bash

# Generate nodes.txt file from kubectl info
kubectl get nodes -o wide > nodes.txt

# Run the parser on it to get the file
python3 ./kubNodesInfoParser.py -n nodes.txt

# Remove files starting with 'output'
rm -f nodes.txt

echo "Look in ipaddr.json to get node ip"
