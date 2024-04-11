class Packetizer:

    def __init__(self, maxBlockSize=64):
        self.maxBlockSize = maxBlockSize

    def addHeader(self):
        pass

    def parse(self, bytestream):
        packets = []
        for i in range(len(bytestream) // self.maxBlockSize + 1):
            packets.append(bytestream[i*self.maxBlockSize: (i+1)*self.maxBlockSize])

        return packets

    

if __name__ == "__main__":
    packetizer = Packetizer(16)

    charstream = "aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbccccccccccccccccdddddddd"

    bytestream = charstream.encode('utf-8')

    packets = packetizer.parse(bytestream)

    print(packets)