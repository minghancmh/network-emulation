#!/bin/bash

# Calculate min, max, and step values for redundancyFactor
REDUNDANCY_FACTOR_MIN=0.2
REDUNDANCY_FACTOR_MAX=0.9
REDUNDANCY_FACTOR_STEP=0.05

# Calculate min, max, and step values for packetDropRate
PACKET_DROP_RATE_MIN=0.01
PACKET_DROP_RATE_MAX=0.2
PACKET_DROP_RATE_STEP=0.01


# Loop through redundancyFactor from 0 to 1
# for redundancyFactor in $(seq $REDUNDANCY_FACTOR_MIN $REDUNDANCY_FACTOR_STEP $REDUNDANCY_FACTOR_MAX); do
    # Loop through packetDropRate from 0 to 1
    for packetDropRate in $(seq $PACKET_DROP_RATE_MIN $PACKET_DROP_RATE_STEP $PACKET_DROP_RATE_MAX); do
        redundancyFactor=0.6 
        echo "Running with redundancyFactor=$redundancyFactor and packetDropRate=$packetDropRate"
        # Run your command with the current values of redundancyFactor and packetDropRate
        # Example command:
        # ./your_program --redundancyFactor $redundancyFactor --packetDropRate $packetDropRate
        ./doTest.sh $redundancyFactor $packetDropRate
    done
# done
