#!/bin/bash

# This script installs the routing table into every kind node. ipaddr.json must be generated before this using ./getip.sh

if [ ! -f "ipaddr.json" ]; then
    echo "ipaddr.json does not exist"
    echo "trying to genereate ipaddr.json"
    ./getip.sh
fi

# Read the node names into an array
node_names=($(jq -r 'keys[]' ipaddr.json))

# Iterate over the node names
for node in "${node_names[@]}"; do
  # Extract the IP address for the current node
  ip=$(jq -r --arg node "$node" '.[$node]' ipaddr.json)
  docker cp ./topology-generator/routing_tables.json $node:/app/routing_tables.json
  docker cp ./ipaddr.json $node:/app/ipaddr.json
done
echo ""
echo "Copied to all cluster nodes. Please check the following nodes:"
for node in "${node_names[@]}"; do
  # Extract the IP address for the current node
    echo "SUCCESSFUL: $node"
done