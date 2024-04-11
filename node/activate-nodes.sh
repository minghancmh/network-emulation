#!/bin/bash

# Command to activate the nodes
activate_command="python3 -u node.py"

# Get the list of nodes in the kind cluster
nodes=$(docker ps --format '{{.Names}}')

# Loop through each node and activate it
for node in $nodes; do
  echo "Activating node: $node"
#   activate each node using docker
  docker exec -d $node $activate_command > output_$node.txt 2> error_$node.txt
  echo "Node activated: $node"
  echo "---------------------------------"
  echo ""

done
