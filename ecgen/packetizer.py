from const import PADDING_BYTE
class Packetizer:
    """
    The Packetizer class is reponsible for breaking down an input stream into chunks, and padding them to maxBlockSize.
    It is also responsible for converting each of these chunks into a bytestring for processing downstream.
    utf-8 encoding is used for str->byte conversion.
    """

    def __init__(self, maxBlockSize=64):
        self.maxBlockSize = maxBlockSize

    def addHeader(self):
        pass

    def parse(self, input_stream):
        packets = []
        for i in range(len(input_stream) // self.maxBlockSize + 1):
            packet = self.pad(input_stream[i*self.maxBlockSize: (i+1)*self.maxBlockSize])
            packets.append(bytes(packet, "utf-8"))

        return packets
    
    def pad(self, packet):
        assert len(packet) <= self.maxBlockSize
        return packet + PADDING_BYTE * (self.maxBlockSize - len(packet))
    
    def postProcess(self, decodedPackets):
        ret = ""
        for packet in decodedPackets:
            packet_str = packet.decode("utf-8").strip(PADDING_BYTE)
            ret += packet_str
        return ret


    

