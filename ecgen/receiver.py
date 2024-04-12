import zfec
from utils import Packet
from typing import List
import zlib

class Receiver:
    def __init__(self, SENDER_M: int, receiverNodeIP: str):
        self.buffer: List[Packet] = [] # A list of packets that the receiver has received
        self.decoder = None # Note that the decoder needs to be instantiated every decode call because k,m are dependent on the packets received
        self.SENDER_M = SENDER_M # m value in the encoder of the sender
        self.myip = receiverNodeIP # IP of the receiver node

    def recv(self):
        # This function should append the packet to the buffer of the receiver
        # This function should verify that it is the correct destination by checking the packet header
        # It should also verify the udphdr checksum and ignore the packet if the verify_checksum fails
        # Once it passes all these tests, append it to the buffer of the receiver
        pass

    def verify_checkSum(self, packet: Packet):
        hdr = packet.udpheader
        srcPort = hdr.sourcePort
        destPort = hdr.destinationPort
        udplen = hdr.udpLength
        packetData = packet.packetData
        packetNum = packet.packetNumber
        packetChecksum = hdr.checkSum
        currChecksum = zlib.crc32(packetData + bytes(srcPort) + bytes(destPort) + bytes(udplen) + bytes(packetNum))
        return packetChecksum == currChecksum

    def decode(self):
        # Note that the value of m here should be the same as the value of m as the sender
        # k: len of the buffer
        k = len(self.buffer)
        self.decoder = zfec.Decoder(k, self.SENDER_M)
        blocksReceived = [None] * k
        blockNums = []

        self.buffer = sorted(self.buffer, key=lambda pkt:pkt.packetNumber)
        for pkt in self.buffer:
            blocksReceived.append(pkt.packetData)
            blockNums.append(pkt.packetNumber)

        self.buffer: List[Packet] = [] # clear the buffer
        self.decoder = None # clear the decoder 

        return self.decoder.decode(blocksReceived, blockNums)

        
        # sort out the buffer interms of the index of the packets




    

# enc = zfec.Encoder(4, 10)
# dec = zfec.Decoder(5, 10)

# out = enc.encode([b"hello", b"how00", b"are00", b"you00"])
# print("encoded:", out)

# # corrupt 2 blocks
# blockNums = [i for i in range(len(out))]

# for i in range(5):
#     rand_num = random.randint(0,5)
#     out[rand_num] = None
#     blockNums.remove(rand_num)


# blocksReceived = []
# for i in range(len(out)):
#     if out[i] != None:
#         blocksReceived.append(out[i])


# print("blocks received:", blocksReceived)

# recovered = dec.decode(blocksReceived, blockNums)

# print("recovered:", recovered)
