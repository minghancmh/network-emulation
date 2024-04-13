from sender import Sender
from router import Router
from receiver import Receiver
import random

# This file abstracts away the sending and receiving logic. 
# It is a demo to show how encoding / packetloss, and decoding are simulated.


with open("sampleInput.txt", "r") as f:
    inputToSend = f.read()
sender = Sender(0.2, inputToSend, "1.1.1.1", "2.2.2.2", 11111, 22222) # 0.2 is the redundancy factor. Very it and see results!
k,m = sender.getkm()

sender.encode()
packets = list(sender.packetQueue)

# drop some packets
drop_rate = 0.1 # this is the probability that a packet gets dropped. Vary it and see results!
packetsReceived = []
for pkt in packets:
    rand = random.random()
    if rand < drop_rate:
        continue
    packetsReceived.append(pkt)



print(f"Started with {len(packets)} packets, received {len(packetsReceived)} packets at the receiver. {len(packets) - len(packetsReceived)} packets were dropped.")

receiver = Receiver(k,m, "2.2.2.2")

receiver.buffer = packetsReceived

decodedPackets = receiver.decode()



ret_str = receiver.postProcess()





