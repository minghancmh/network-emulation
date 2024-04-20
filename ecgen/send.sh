#!/bin/bash
# The dest_ip here MUST be the next hop of the sender, NOT THE FINAL DESTINATION IP

redundancy_factor=$1
echo "[send.sh]Redundancy factor: $redundancy_factor"
if [ -z "$redundancy_factor" ]; then
    echo "Please provide the redundancy factor as an argument."
    exit 1
fi
# Function to display script usage
usage() {
    echo "Usage: $0 [-h]" 1>&2
    echo "Options:" 1>&2
    echo "  -h: Display this help message." 1>&2
    exit 1
}

# Default message file
msg_file_prefix="./textfiles/sampleText"

# Parse command-line options
while getopts ":h" opt; do
    case ${opt} in
        h )
            usage
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            usage
            ;;
    esac
done
shift $((OPTIND -1))

echo "sending..."

# Read JSON data from file
json_data=$(cat ipaddr.json)

# Parse the JSON data and extract the IP address of router-1
# change the names according to the names of the docker containers
bgrip=$(echo "$json_data" | jq -r '.["network-emulation-router-1"]')
dest=$(echo "$json_data" | jq -r '.["network-emulation-receiver-8"]') #TODO: Shouldnt hardcode this

echo "Destination IP: $dest"
echo "bgrip: $bgrip"

# Loop through message files from sampleText1 to sampleText1000
for ((i=1; i<=200; i++)); do
    msg_file="${msg_file_prefix}${i}.txt"
    echo "Sending $msg_file..."
    python3 -u send.py --bgrip "$bgrip" --msg "$msg_file" --dest_ip "$dest" --redundancy_factor "$redundancy_factor"


done
