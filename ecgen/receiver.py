import pickle
import time
import zfec
from utils import Packet
from typing import List
import zlib
import socket
import json
from packetizer import Packetizer
from colorama import Fore
import sys
from const import LEN_DATA_TO_RECV, PORT, LOG_FILE_PATH


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
        self.decodedUUIDs = []
        self.numSuccessfullyDecodedMsgs = 0 
        self.timeout = 5
        self.currentMessageID = None
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
    
    def log_num_decoded_msgs(self):
        print(f"{Fore.RED}[RECEIVER]:LOGGING{self.numSuccessfullyDecodedMsgs} {Fore.RESET}")
        with open(LOG_FILE_PATH, "a") as f:
            f.write(f"Num successfully decoded msgs: {self.numSuccessfullyDecodedMsgs}*\n")

    def recv(self):
        # This function should append the packet to the buffer of the receiver
        # This function should verify that it is the correct destination by checking the packet header
        # It should also verify the udphdr checksum and ignore the packet if the verify_checksum fails
        # Once it passes all these tests, append it to the buffer of the receiver
        with open("ipaddr.json", "r") as f:
            ipaddr = json.loads(f.read())
        recv_eightip = ipaddr["network-emulation-receiver-8"] # TODO: shouldn't hardcode this
        try:
            self.myip = self.get_myip()
            self.myport = PORT
            print(f"[RECEIVER]: Listening on {self.myip}:{self.myport}...")
            # Create a UDP socket for unicast reception
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.myip, self.myport))
            sock.settimeout(30) # TODO: set to 120

            while True: 
                try: 
                    data, addr = sock.recvfrom(LEN_DATA_TO_RECV)
                    packet = pickle.loads(data)
                    self.setSenderM(packet.senderM)
                    self.setSenderK(packet.senderK)
                    print(f'Received packet from {addr}: {packet}')
                    if self.currentMessageID == None:
                        self.currentMessageID = packet.msgID
                    elif self.currentMessageID != packet.msgID:
                        # if the incoming message id (packet.msgID) is different from the current message id, then reset the buffer and decoded packets
                        # otherwise if we have a buffer of 2 different types of msgID, we confused the decoder and the decoder will block 
                        self.currentMessageID = packet.msgID
                        self.buffer = []
                        self.decodedPackets = []
                    packetMsgID = packet.msgID

                    if packetMsgID not in self.decodedUUIDs:
                        self.buffer.append(packet) 
                    if len(self.buffer) != 0:
                        try:
                            self.decode()
                            outmsg = self.postProcess()
                            print(f"[RECEIVER]: SUCCESSFULLY Decoded message: {outmsg}")
                            self.decodedUUIDs.append(packetMsgID)
                            self.numSuccessfullyDecodedMsgs += 1
                            print(f"{Fore.GREEN}[RECEIVER]: Num successfully decoded messages: {self.numSuccessfullyDecodedMsgs} {Fore.RESET}")
                        except:
                            print(f"[RECEIVER]: Cannot decode message, not enough packet, will try again...")
                    sock.settimeout(self.timeout)
                except socket.timeout:
                    if self.myip == recv_eightip:
                        print(f"[RECEIVER]: Timeout occurred, no messages received. Exiting...")
                        self.log_num_decoded_msgs()
                        break
        except socket.timeout:
            print(f"[RECEIVER]: Timeout occurred, no messages received for 2 minutes. Exiting...")
            if self.myip == recv_eightip:
                print("self.myip", self.myip)
                print("recv_eightip", recv_eightip)
                self.log_num_decoded_msgs()
            sys.exit(1)
        

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
        # print("decoder km: ", (k, self.senderM))
        print(f'[RECEIVER]: spawming the zfec decoder')
        self.decoder = zfec.Decoder(k, self.senderM) 
        blocksReceived = []
        blockNums = []
        self.buffer = sorted(self.buffer, key=lambda pkt:pkt.packetNumber)
        for pkt in self.buffer:
            blocksReceived.append(pkt.packetData)
            blockNums.append(pkt.packetNumber)

        print(f"[RECEIVER]: passing into the zfec decoder")
        decoded = self.decoder.decode(blocksReceived, blockNums)
        print(f"[RECEIVER]: decoded={decoded}")

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
                



    
