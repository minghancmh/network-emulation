# https://github.com/tahoe-lafs/zfec
import pickle
import uuid
import zfec
import math
from packetizer import Packetizer
from collections import deque
from utils import Packet
from const import LEN_DATA_PACKET
import socket
from const import PORT, LOG_FILE_PATH
import sys


class Sender:
    def __init__(self, redundancy_factor: float, senderIP: str, destinationIP: str, sourcePort: int, destinationPort: int ):
        """
        redundancy_factor: A scalar factor which determines how many extra packets are going to be generated
            For example, if the input packetizes into 256 blocks, and k is set to 0.1, then floor(0.1*256) = 25 extra packets will be generated
        input: This is the input string that is to be sent across the network
        """
        print("[SENDER]: Initializing sender...")
        self.redundancy_factor = redundancy_factor
        self.input = None 
        self.senderIP = self.get_myip()
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.sourceIP = self.senderIP
        self.destinationIP = destinationIP
        self.packetizer = Packetizer(LEN_DATA_PACKET)
        self.packets = None
        self.borderGatewayRouterIP = None
        self.k = 0 
        self.m = 0 
        self.encoder = None 
        self.packetQueue: deque[Packet] = deque([])
        self.displaySenderAttributes()

    def get_myip(self):
        # Create a UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server (Google DNS)
        myip = s.getsockname()[0]  # Get the local IP address assigned by Docker
        s.close()
        return myip
    
    def setMessage(self, msg: str): 
        self.input = msg
        self.packets = self.packetizer.parse(self.input)
        k = len(self.packets)
        m = k + math.floor(self.redundancy_factor * k)
        self.k = k 
        self.m = m
        self.encoder = zfec.Encoder(k, m)
        return uuid.uuid4()


    def getkm(self):
        return (self.k,self.m)

    def encode(self, msgID: uuid):
        print(f"[SENDER]: encoding...")
        dataPackets = self.encoder.encode(self.packets)
        for i in range(len(dataPackets)):
            packet = Packet(dataPackets[i], i, self.sourcePort, self.destinationPort, LEN_DATA_PACKET, self.sourceIP, self.destinationIP, senderK=self.k, senderM=self.m, msgID=msgID)
            self.packetQueue.append(packet)

    

    def printAllPacketsInQueue(self):
        # WARNING: This function is incredibly inefficient and should not be used. It is to be used only for debugging purposes.
        newQueue: deque[Packet] = deque([])
        while self.packetQueue:
            pkt = self.packetQueue.popleft()
            pkt.printPacket()
            newQueue.append(pkt)
        self.packetQueue = newQueue


    def send(self, destination_ip, msgID: uuid): 
        # Create a UDP socket
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert len(self.packets) != 0, "No packets to send."
        if (len(self.packetQueue) == 0):
            self.encode(msgID)

        while self.packetQueue:
            packet = self.packetQueue.popleft()
            packet.printPacket()
            # Send the message to the destination IP address and port
            sender_socket.sendto(pickle.dumps(packet), (destination_ip, PORT))
            print("Message sent successfully.")
        sender_socket.close()


    def displaySenderAttributes(self):
        print(f"""\n=====SENDER ATTRIBUTES=====\
      \nredundancy_factor: {self.redundancy_factor}\
      \nsenderIP: {self.senderIP}\
      \ndestinationIP: {self.destinationIP}\
      \nsourcePort: {self.sourcePort}\
      \ndestinationPort: {self.destinationPort}\
        \n=============================\n

      """)

    


