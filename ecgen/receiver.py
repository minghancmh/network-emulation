import pickle
import zfec
from utils import Packet
from typing import List
import zlib
import socket
import struct
import select
import argparse
from packetizer import Packetizer
from const import LEN_DATA_TO_RECV, PORT


class Receiver:
    def __init__(self, routerIP: str) :
        print(f"[RECEIVER]: Initializing receiver...")
        self.buffer: List[Packet] = [] # A list of packets that the receiver has received
        self.decoder = None # Note that the decoder needs to be instantiated every decode call because k,m are dependent on the packets received
        self.senderM = None # m value in the encoder of the sender
        self.myip = self.get_myip() # IP of the receiver node
        self.myport = None # Port of the receiver node
        self.minPackets = None # k value in the encoder of the sender. The receiver must receive at least k packets, or decoding will fail.
        self.decodedPackets = None # The decoded packets to be passed to post process.
        self.packetizer = Packetizer()
        self.routerIp = routerIP
        self.displayReceiverAttributes()


    def setSenderK(self, k):
        self.minPackets = k

    def setSenderM(self, m):
        self.senderM = m

    def get_myip(self):
        # Create a UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server (Google DNS)
        myip = s.getsockname()[0]  # Get the local IP address assigned by Docker
        s.close()
        return myip

    def recv(self):
        # This function should append the packet to the buffer of the receiver
        # This function should verify that it is the correct destination by checking the packet header
        # It should also verify the udphdr checksum and ignore the packet if the verify_checksum fails
        # Once it passes all these tests, append it to the buffer of the receiver
        self.myip = self.get_myip()
        self.myport = PORT
        print(f"[RECEIVER]: Listening on {self.myip}:{self.myport}...")
        # Create a UDP socket for unicast reception
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.myip, self.myport))
        # sock.setblocking(0)
        while True: 
            data, addr = sock.recvfrom(LEN_DATA_TO_RECV)
            packet = pickle.loads(data)
            self.setSenderM(packet.senderM)
            self.setSenderK(packet.senderK)
            print(f'Received packet from {addr}: {packet}')
            self.buffer.append(packet)
            # if (len(self.buffer) >= self.minPackets):
            try:
                self.decode()
                outmsg = self.postProcess()
                print(f"[RECEIVER]: SUCCESSFULLY Decoded message: {outmsg}")
            except:
                print(f"[RECEIVER]: Don't have enough packets to decode message, will try again...")

    def send(destination_ip, packet: Packet):
        # Create a UDP socket
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Send the message to the destination IP address and port
            sender_socket.sendto(pickle.dumps(packet), (destination_ip, packet.udpheader.destinationPort))
            print("Message sent successfully.")
        finally:
            # Close the socket
            sender_socket.close()

    def subscribe(self):
        self.send(self.routerIp, "subscribe " + self.myip)
        

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
        print(f"[RECEIVER]: decoding...")
        if len(self.buffer) < self.minPackets:
            raise Exception(f"[RECEIVER]: DECODING FAIL. Received {len(self.buffer)} packets at the receiver. Need at least {self.minPackets} packets.")
        assert self.senderM != None, "SenderM not set. Please set the senderM value."
        # Note that the value of m here should be the same as the value of m as the sender
        # k: len of the buffer
        k = len(self.buffer)
        print("decoder km: ", (k, self.senderM))
        self.decoder = zfec.Decoder(k, self.senderM) 
        blocksReceived = []
        blockNums = []

        self.buffer = sorted(self.buffer, key=lambda pkt:pkt.packetNumber)
        for pkt in self.buffer:
            blocksReceived.append(pkt.packetData)
            blockNums.append(pkt.packetNumber)


        decoded = self.decoder.decode(blocksReceived, blockNums)
        # print(decoded)

        self.buffer: List[Packet] = [] # clear the buffer
        self.decoder = None # clear the decoder 

        self.decodedPackets = decoded[:self.minPackets]

        return decoded

    
    def postProcess(self):
        # this function assumes that decode has already been called. This is just to derive the original text file.
        assert self.decodedPackets != None
        return self.packetizer.postProcess(self.decodedPackets)
    

    def displayReceiverAttributes(self):
        print(f"""\n=====RECEIVER ATTRIBUTES=====\
        \n myip: {self.myip}\
        \n myport: {self.myport}\
        \n minPackets: {self.minPackets}\
        \n senderM: {self.senderM}\
        \n routerIp: {self.routerIp}\
        \n=============================\n
      """)
                



    
