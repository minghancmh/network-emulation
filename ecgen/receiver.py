import zfec
from utils import Packet
from typing import List
import zlib
from packetizer import Packetizer

class Receiver:
    def __init__(self, senderK:int, senderM: int, receiverNodeIP: str):
        print(f"[RECEIVER]: Initializing receiver...")
        self.buffer: List[Packet] = [] # A list of packets that the receiver has received
        self.decoder = None # Note that the decoder needs to be instantiated every decode call because k,m are dependent on the packets received
        self.senderM = senderM # m value in the encoder of the sender
        self.myip = receiverNodeIP # IP of the receiver node
        self.minPackets = senderK # k value in the encoder of the sender. The receiver must receive at least k packets, or decoding will fail.
        self.decodedPackets = None
        self.packetizer = Packetizer()

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
        print(f"[RECEIVER]: decoding...")
        if len(self.buffer) < self.minPackets:
            raise Exception(f"[RECEIVER]: DECODING FAIL. Received {len(self.buffer)} packets at the receiver. Need at least {self.minPackets} packets.")
        # Note that the value of m here should be the same as the value of m as the sender
        # k: len of the buffer
        k = len(self.buffer)
        self.decoder = zfec.Decoder(k, self.senderM)
        blocksReceived = []
        blockNums = []

        self.buffer = sorted(self.buffer, key=lambda pkt:pkt.packetNumber)
        for pkt in self.buffer:
            blocksReceived.append(pkt.packetData)
            blockNums.append(pkt.packetNumber)


        decoded = self.decoder.decode(blocksReceived, blockNums)

        self.buffer: List[Packet] = [] # clear the buffer
        self.decoder = None # clear the decoder 

        self.decodedPackets = decoded[:self.minPackets]

        return decoded
    
    def postProcess(self):
        # this function assumes that decode has already been called. This is just to derive the original text file.
        assert self.decodedPackets != None
        return self.packetizer.postProcess(self.decodedPackets)



    
