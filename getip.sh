#!/bin/bash

# This executable outputs an ipaddr.json file for use by applyRoutingTable.sh. This file gets the IP of all containers managed by Docker Compose and puts them in a 
# JSON file with key=name, value=ip.

# Generate nodes.txt file from Docker Compose container information
docker-compose ps -q | xargs docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{.Name}}' | awk '{print $1,$2}' > nodes.txt

# Run the parser on it to get the IP addresses
python3 ./nodes-parser.py -n nodes.txt

# Remove temporary files
rm -f nodes.txt

echo "Look in ipaddr.json to get container IPs"
