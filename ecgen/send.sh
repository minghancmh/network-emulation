#!/bin/bash
# The dest_ip here MUST be the next hop of the sender, NOT THE FINAL DESTINATION IP

conda init
conda activate netsim
echo "sending..."


# Read JSON data from file
json_data=$(cat ipaddr.json)

# Parse the JSON data and extract the IP address of router-1
# change the names according to the names of the docker containers
bgrip=$(echo "$json_data" | jq -r '.["network-emulation-router-1"]')
dest=$(echo "$json_data" | jq -r '.["network-emulation-receiver-14"]')

echo $dest


python3 -u node.py --nodeType sender --bgrip $bgrip --msg sampleInput.txt --dest_ip $dest
