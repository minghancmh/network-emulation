#!/bin/bash


redundancy_factor=$1
packet_drop_rate=$2
VAR_NAME=PACKET_DROP_RATE

# Check if the variable exists in the .env file
if grep -q "^${VAR_NAME}=" ecgen/const.py; then
    # Variable exists, replace its value
    sed -i '' "s/^${VAR_NAME}=.*/${VAR_NAME}=${packet_drop_rate}/" ecgen/const.py
else
    # Variable does not exist, add it
    echo "${VAR_NAME}=${packet_drop_rate}" >> ecgen/const.py
fi

if [ -z "$redundancy_factor" ]; then
    echo "Please provide the redundancy factor as an argument."
    exit 1
fi

if [ -z "$packet_drop_rate" ]; then
    echo "Please provide the packet drop rate as an argument."
    exit 1
fi

./setup.sh

sleep 5

./execSend.sh $redundancy_factor

sleep 30

echo "y" | ./clean.sh

echo "Test completed successfully. Environment clean."

