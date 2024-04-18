# https://github.com/tahoe-lafs/zfec
import zfec
import math
from packetizer import Packetizer
from collections import deque
from utils import Packet
from const import LEN_DATA_PACKET
import socket


class Sender:
    def __init__(self, redundancy_factor: float, input: str, senderIP: str, destinationIP: str, sourcePort: int, destinationPort: int):
        """
        redundancy_factor: A scalar factor which determines how many extra packets are going to be generated
            For example, if the input packetizes into 256 blocks, and k is set to 0.1, then floor(0.1*256) = 25 extra packets will be generated
        input: This is the input string that is to be sent across the network
        """
        print("[SENDER]: Initializing sender...")
        self.redundancy_factor = redundancy_factor
        self.input = input 
        self.senderIP = senderIP
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.sourceIP = self.senderIP
        self.destinationIP = destinationIP

        self.packetizer = Packetizer(LEN_DATA_PACKET)
        self.packets = self.packetizer.parse(self.input)

        k = len(self.packets)
        m = k + math.floor(self.redundancy_factor * k)
        self.k = k
        self.m = m
        self.encoder = zfec.Encoder(k, m)
        self.packetQueue: deque[Packet] = deque([])

    def getkm(self):
        return (self.k,self.m)

    def encode(self):
        print(f"[SENDER]: encoding...")
        dataPackets = self.encoder.encode(self.packets)
        for i in range(len(dataPackets)):
            packet = Packet(dataPackets[i], i, self.sourcePort, self.destinationPort, LEN_DATA_PACKET, self.sourceIP, self.destinationIP)
            self.packetQueue.append(packet)




    def printAllPacketsInQueue(self):
        # WARNING: This function is incredibly inefficient and should not be used. It is to be used only for debugging purposes.
        newQueue: deque[Packet] = deque([])
        while self.packetQueue:
            pkt = self.packetQueue.popleft()
            pkt.printPacket()
            newQueue.append(pkt)
        self.packetQueue = newQueue


    def send(self, packet:Packet):
        # input sending logic to other nodes here
        # feel free to add class attributes such as next nodes IP_addrs
        print(f"[SENDER]: sender sending packet...")
        packet.printPacket()
        pass

    def displaySenderAttributes(self):
        print(f"""\n=====SENDER ATTRIBUTES=====\
      \nredundancy_factor: {self.redundancy_factor}\
      \nsenderIP: {self.senderIP}\
      \ndestinationIP: {self.destinationIP}\
      \nsourcePort: {self.sourcePort}\
      \ndestinationPort: {self.destinationPort}
      """)

    


