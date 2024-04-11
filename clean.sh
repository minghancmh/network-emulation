#!/bin/bash

# Clean removes the entire kind environment and all of its dependencies. 

# Prompt the user for confirmation
echo "This script deletes the entire kind environment and its dependencies. Do you wish to continue? (y/n)"
read -r response

# Check the user's response
case "$response" in
    [yY][eE][sS]|[yY]) 
        echo "Proceeding..."
        ;;
    [nN][oO]|[nN]) 
        echo "Aborting..."
        exit 1
        ;;
    *)
        echo "Invalid input..."
        exit 1
        ;;
esac

# Remove files starting with 'output'
rm -f ./topology-generator/output*

# Remove routing_tables.json file
rm -f ./topology-generator/routing_tables.json

# Delete the kind cluster
kind delete cluster --name test-cluster

# Remove ipaddr.json
rm -f ./ipaddr.json

echo "Cleanup completed."


