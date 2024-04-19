#!/bin/bash

# This script installs the routing table into every kind node. ipaddr.json must be generated before this using ./getip.sh

# Check if ipaddr.json exists, and attempt to generate it if it does not
if [ ! -f "ipaddr.json" ]; then
    echo "ipaddr.json does not exist"
    echo "Trying to generate ipaddr.json..."
    ./getip.sh
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mERROR: Failed to generate ipaddr.json.\033[0m"
        exit 1
    fi
fi

# Read the node names into an array
node_names=($(jq -r 'keys[]' ipaddr.json))
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to parse node names from ipaddr.json.\033[0m"
    exit 1
fi

# Iterate over the node names
for node in "${node_names[@]}"; do
    # Extract the IP address for the current node
    ip=$(jq -r --arg node "$node" '.[$node]' ipaddr.json)
    if [ -z "$ip" ]; then
        echo -e "\033[0;31mERROR: IP address for $node could not be retrieved.\033[0m"
        continue
    fi
    # Copy routing tables and ipaddr.json to each node
    docker cp ./erdos-renyi-generator/routing_tables.json $node:/app/routing_tables.json
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mERROR: Failed to copy routing_tables.json to $node.\033[0m"
        continue
    fi
    docker cp ./ipaddr.json $node:/app/ipaddr.json
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mERROR: Failed to copy ipaddr.json to $node.\033[0m"
        continue
    fi
done

echo ""
echo "Copying complete. Please check the following nodes:"
for node in "${node_names[@]}"; do
    echo "SUCCESSFUL: $node"
done
