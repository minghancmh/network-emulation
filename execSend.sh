#!/bin/bash

redundancy_factor=$1

echo "[execSend.sh] Redundancy factor: $redundancy_factor"

docker exec -it network-emulation-sender-1 /bin/bash -c "\
    source /opt/conda/etc/profile.d/conda.sh; \
    conda activate netsim; \
    ./send.sh $redundancy_factor\
    "

echo "Command executed successfully inside docker. "