#!/bin/bash

# Clean removes all Docker containers created by Docker Compose.

# Prompt the user for confirmation
echo "This script deletes all Docker containers created by Docker Compose. Do you wish to continue? (y/n)"
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



# Shut down and remove containers created by Docker Compose
docker-compose down

# Remove the docker images
docker rmi network-emulation-router network-emulation-receiver network-emulation-sender


# Optionally, remove other files or perform additional cleanup here

echo "Cleanup completed."
