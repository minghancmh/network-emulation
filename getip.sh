#!/bin/bash

# This executable outputs an ipaddr.json file for use by applyRoutingTable.sh. This file gets the IP of all containers managed by Docker Compose and puts them in a 
# JSON file with key=name, value=ip.

# Generate nodes.txt file from Docker Compose container information
docker-compose ps -q | xargs docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{.Name}}' | awk '{print $1,$2}' > nodes.txt
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to generate nodes.txt from Docker container information.\033[0m"
    exit 1
fi

# Run the parser on it to get the IP addresses
python3 ./nodes-parser.py -n nodes.txt
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to parse nodes.txt into ipaddr.json.\033[0m"
    exit 1
fi

# Remove temporary files
rm -f nodes.txt
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to remove temporary file nodes.txt.\033[0m"
    exit 1
fi

echo "Look in ipaddr.json to get container IPs"
