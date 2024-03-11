#!bin/bash
# this file is to be loaded into worker nodes

#ip of the node that you are trying to communicate with
IP=172.19.0.3

#port num
#set by nc -u -l -k 55255 on the listener
PORT=55255

MESSAGE="insert payload here"

for i in {1..10000}; do
    echo "$MESSAGE" | nc $IP $PORT -u -q 0
done