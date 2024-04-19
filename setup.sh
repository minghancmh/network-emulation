#!/bin/bash

# Make sure we have permissions for all the files
chmod +x ./topology-generator/gen.sh
chmod +x ./clean.sh
chmod +x ./applyRoutingInfo.sh
chmod +x ./getip.sh

TOPO_CONFIG_FILE="./topology-generator/config"

# Path to your docker-compose file 
DOCKER_COMPOSE_FILE="docker-compose.yaml"


replicas=$(yq e '.services.node.deploy.replicas' "$DOCKER_COMPOSE_FILE")


# Extract the "routers" value using jq
routers=$(jq -r '.routers' "$TOPO_CONFIG_FILE")
echo "Num routers generated in topology generator: $routers"
echo "Num replicas in docker-compose.yaml: $replicas"

# Check if the "routers" value is equal to the number of worker nodes in kind.
if [ ! $routers -eq $replicas ]; then
    echo "ERROR: worker_count in kind_config does not match the number of routers in topology-generator"
    exit 1
fi


# Builds docker image and spins up containers
docker-compose up -d


# Generate the topology information
echo "Generating topology information."
cd topology-generator && ./gen.sh
cd ..

./getip.sh

echo "Applying the routing info to each node."
./applyRoutingInfo.sh

echo "Nodes created."