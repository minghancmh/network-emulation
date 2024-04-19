#!/bin/bash
# The dest_ip here MUST be the next hop of the sender, NOT THE FINAL DESTINATION IP

# Initialize conda
conda init
conda activate netsim

# Function to display script usage
usage() {
    echo "Usage: $0 [-m <message_file>] [-h]" 1>&2
    echo "Options:" 1>&2
    echo "  -m <message_file>: Specify the message file." 1>&2
    echo "  -h: Display this help message." 1>&2
    exit 1
}

# Default message file
msg_file="sampleInput.txt"

# Parse command-line options
while getopts ":m:h" opt; do
    case ${opt} in
        m )
            msg_file=$OPTARG
            ;;
        h )
            usage
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            usage
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
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
dest=$(echo "$json_data" | jq -r '.["network-emulation-receiver-8"]')

echo "Destination IP: $dest"

python3 -u node.py --nodeType sender --bgrip $bgrip --msg $msg_file --dest_ip $dest
