import zlib
from const import TTL
class udphdr:
    def __init__(self, sourcePort, destinationPort, udpLength, checkSum):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.udpLength = udpLength
        self.checkSum = checkSum

class iphdr:
    def __init__(self, sourceIP, destIP):
        self.sourceIP = sourceIP
        self.destIP = destIP
        self.TTL = TTL


class Packet:
    """
    This is more of a "struct" class created to abstract away packet logic.
    Each packet is assigned a packetNumber, which is required by the zfec decoder.
    """
    def __init__(self, packetData: bytes, packetNumber: int, sourcePort: int, destinationPort: int, udpLength: int, sourceIP:str, destIP:str):
        """
        packetData: data of the packet in bytes
        packetNumber: number of the packet
        sourcePort: sending port
        destinationPort: final destinationPort
        udpLength: length of the packetData
        """
        self.packetData = packetData
        self.packetNumber = packetNumber
        checkSum = self.get_checksum(self.packetData + bytes(packetNumber) + bytes(sourcePort) + bytes(destinationPort) + bytes(udpLength)) # Generate a checksum across the packetData, packetNumber, source/destination ports, and udplength
        self.udpheader = udphdr(sourcePort, destinationPort, udpLength, checkSum)
        self.iphdr = iphdr(sourceIP, destIP)

    def get_checksum(self, data):
        return zlib.crc32(data)

    def printPacket(self):
        print(f"===== PACKET {self.packetNumber} ===== \n IPHEADER(srcIP: {self.iphdr.sourceIP} \t destIP: {self.iphdr.destIP}) \n UDPHEADER (srcPort: {self.udpheader.sourcePort} \t destPort: {self.udpheader.destinationPort} \t udpLen: {self.udpheader.udpLength} \t checkSum: {self.udpheader.checkSum}) \n BODY: {self.packetData}\n")
