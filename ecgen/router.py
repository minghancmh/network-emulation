import pickle
import zlib
from const import LEN_DATA_TO_RECV, NUM_ROUTERS, PORT
from utils import Packet
from collections import deque
import random
import socket
from threading import Thread, Lock
import json 
import time


class Router:
    def __init__(self, probabilityDropRate):
        time.sleep(15)
        self.routerQueue = deque([]) 
        self.probabilityDropRate = probabilityDropRate
        self.myip = self.get_myip()
        self.queueLock = Lock()
        with open("routing_tables.json" ,'r') as f:
            routingTableStr = f.read()
        self.routingTable = json.loads(routingTableStr)
        with open("ipaddr.json", 'r') as f:
            ipaddrStr = f.read()
        self.ipAddr = json.loads(ipaddrStr)
        self.myRouterNumber = self.get_myRouterNumber()
        recvThread = Thread(target=self.recv)
        sendThread = Thread(target=self.send)
        recvThread.start()
        sendThread.start()
        print("router finish init")


    def get_myRouterNumber(self):
        for rec_no, rec_ip in self.ipAddr.items():
            if rec_ip == self.myip:
                return int(rec_no[-1])
        return -1


    def get_myip(self):
        # Create a UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server (Google DNS)
        myip = s.getsockname()[0]  # Get the local IP address assigned by Docker
        s.close()
        return myip

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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.myip, PORT))
        # sock.setblocking(0)
        while True: 
            print("[Router]: receiving...")
            data, addr = sock.recvfrom(LEN_DATA_TO_RECV)
            packet = pickle.loads(data)
            if not self.verify_checkSum(packet):
                # packet has been corrupted, do not forward
                print("packet corrupted")
                continue
            self.routerQueue.append(packet)
            print(self.routerQueue)
            time.sleep(1)
            


    def send(self):
        while True:
            print("[Router]: sending...")
            print(f"[Router.send]: Length of router queue = {len(self.routerQueue)}")
            if len(self.routerQueue) > 0:
                print("[Router.send]: lenQueue > 1")
                packet = self.routerQueue.popleft()
                print(f"packet to send: {packet}")
                if self.random_drop():
                    # packet has been dropped, do not forward
                    continue
                # forward the packet
                destIP = packet.iphdr.destIP
                receiverName = None
                for rec_no, rec_ip in self.ipAddr.items():
                    if rec_ip == destIP:
                        receiverName = rec_no
                        break

                receiverNo = int(receiverName[-1]) 

                receiverRouter = receiverNo % NUM_ROUTERS + 1

                if receiverRouter == self.myRouterNumber:
                    # send to receiver
                    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    try:
                        print(f"[Router.send]: sending to {destIP}: {packet}")
                        # Send the message to the destination IP address and port
                        sender_socket.sendto(pickle.dumps(packet), (destIP, packet.udpheader.destinationPort))
                        print("Message sent successfully.")
                    finally:
                        # Close the socket
                        sender_socket.close()
                else:
                    myRouterName = "node" + str(self.myRouterNumber) if self.myRouterNumber != 1 else "node"
                    receiverRouterName = "node" + str(receiverRouter) if receiverRouter != 1 else "node"

                    # send to next router
                    nextRouter = self.routingTable[myRouterName][receiverRouterName]["next_hop"]
                    nextRouterNumber = int(nextRouter[-1]) if nextRouter != "node" else 1
                    nextRouterIP = self.ipAddr["network-emulation-router-"+str(nextRouterNumber)]
                    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    try:
                        # Send the message to the destination IP address and port
                        sender_socket.sendto(pickle.dumps(packet), (nextRouterIP, packet.udpheader.destinationPort))
                        print("Message sent successfully.")
                    finally:
                        # Close the socket
                        sender_socket.close()
            time.sleep(1) # TODO: remove


    def displayRouterAttributes(self):
        print(f"""\n=====ROUTER ATTRIBUTES=====\
        \nrouterIP: {self.myip}\
        \nprobabilityDropRate: {self.probabilityDropRate}\
        \n=============================\n
      """)
    

