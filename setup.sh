#!/bin/bash

# Make sure we have permissions for all the files
chmod +x ./topology-generator/gen.sh
chmod +x ./clean.sh
chmod +x ./applyRoutingInfo.sh
chmod +x ./getip.sh

TOPO_CONFIG_FILE="./topology-generator/config"

# Path to your docker-compose file 
DOCKER_COMPOSE_FILE="docker-compose.yaml"


replicas=$(yq e '.services.router.deploy.replicas' "$DOCKER_COMPOSE_FILE")

# Extract the "routers" value using jq
routers=$(jq -r '.routers' "$TOPO_CONFIG_FILE")
echo "Num routers generated in topology generator: $routers"
echo "Num replicas in docker-compose.yaml: $replicas"

if [ -z "$routers" ]; then
    echo -e "\033[0;31mERROR: Are you sure you have installed jq?\033[0m"
    exit 1
fi 

if [ -z "$replicas" ]; then
    echo -e "\033[0;31mERROR: Are you sure you have installed yq?\033[0m"
    exit 1
fi

# Check if the "routers" value is equal to the number of worker nodes in kind.
if [ ! $routers -eq $replicas ]; then
    echo -e "\033[0;31mERROR: worker_count in docker-compose does not match the number of routers in topology-generator\033[0m"
    exit 1
fi


docker-compose up -d
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to start docker-compose.\033[0m"
    exit 1
fi

# Generate the topology information
echo "Generating topology information."
cd topology-generator && ./gen.sh
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to generate topology information.\033[0m"
    exit 1
fi
cd ..

./getip.sh
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to execute getip.sh.\033[0m"
    exit 1
fi

echo "Applying the routing info to each node."
./applyRoutingInfo.sh
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to apply routing information.\033[0m"
    exit 1
fi

echo "Nodes created."