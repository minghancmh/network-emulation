import zlib
from utils import Packet
from collections import deque
import random

class Router:
    def __init__(self, probabilityDropRate):
        self.routerQueue = deque([]) 
        self.probabilityDropRate = probabilityDropRate
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
    
    def random_drop(self) -> bool:
        # This function determines whether the router should drop this packet.
        # This is key for simulating packet loss.
        rand = random.random()
        if rand < self.probabilityDropRate:
            return True
        return False


    
    def recv(self):
        # use verify_checkSum to verify the udphdr checksum of the packet
        # if it doesnt checkout, do not forward the packet (ie don't enqueue it)
        pass

    def send(self):
        if self.random_drop():
            # packet has been dropped, do not forward
            return
        # send the packet 
        pass
    

