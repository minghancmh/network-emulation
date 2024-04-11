#!/bin/bash

# Make sure we have permissions for all the files
chmod +x ./topology-generator/gen.sh
chmod +x ./clean.sh
chmod +x ./applyRoutingTable.sh
chmod +x ./getip.sh

TOPO_CONFIG_FILE="./topology-generator/config"

# Path to your Kind configuration file
KIND_CONFIG_FILE="./kind-config.yaml"


# Count the number of worker nodes
worker_count=$(grep -c "role: worker" "$KIND_CONFIG_FILE")


# Extract the "routers" value using jq
routers=$(jq -r '.routers' "$TOPO_CONFIG_FILE")
echo "Num routers generated in topology generator: $routers"
echo "Num workers in kind-config.yaml: $worker_count"

# Check if the "routers" value is equal to the number of worker nodes in kind.
if [ ! $routers -eq $worker_count ]; then
    echo "ERROR: worker_count in kind_config does not match the number of routers in topology-generator"
    exit 1
fi


# Generates the docker image
docker build -t custom-kindest-node .


# Create the kind cluster
kind create cluster --name=test-cluster --config=kind-config.yaml

# Generate the topology information
echo "Generating topology information."
cd topology-generator && ./gen.sh
cd ..

./getip.sh

echo "Applying the routing info to each node."
./applyRoutingInfo.sh

echo "Kind cluster created."
