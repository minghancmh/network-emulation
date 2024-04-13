import unittest
from sender import Sender
from router import Router
from receiver import Receiver
import random
# This file abstracts away the sending and receiving logic. It is a demo to show how encoding / packetloss, and decoding are simulated.

class TestECGen(unittest.TestCase):

    def testSimpleSendReceiveNoDrop(self):
        with open("sampleInput.txt", "r") as f:
            inputToSend = f.read()
        sender = Sender(0.2, inputToSend, "1.1.1.1", "2.2.2.2", 11111, 22222)
        k,m = sender.getkm()

        sender.encode()
        packets = list(sender.packetQueue)

        # drop some packets
        drop_rate = 0
        packetsReceived = []
        for pkt in packets:
            rand = random.random()
            if rand < drop_rate:
                continue
            packetsReceived.append(pkt)

        print(f"Started with {len(packets)} packets, received {len(packetsReceived)} packets at the receiver. {len(packets) - len(packetsReceived)} packets were dropped.")

        receiver = Receiver(k,m, "2.2.2.2")

        receiver.buffer = packetsReceived
        receiver.decode()
        ret_str = receiver.postProcess()

        self.assertEqual(ret_str, inputToSend)

    def testSimpleSendReceiveDeterministicDrop(self):
        with open("sampleInput.txt", "r") as f:
            inputToSend = f.read()
        sender = Sender(0.2, inputToSend, "1.1.1.1", "2.2.2.2", 11111, 22222)
        k,m = sender.getkm()

        sender.encode()
        packets = list(sender.packetQueue)

        # drop some packets
        drop_rate = 0
        packetsReceived = []
        # for pkt in packets:
        #     rand = random.random()
        #     if rand < drop_rate:
        #         continue
        #     packetsReceived.append(pkt)
        packetsReceived = packets[2::]

        print(f"Started with {len(packets)} packets, received {len(packetsReceived)} packets at the receiver. {len(packets) - len(packetsReceived)} packets were dropped.")

        receiver = Receiver(k,m, "2.2.2.2")

        receiver.buffer = packetsReceived
        receiver.decode()
        ret_str = receiver.postProcess()

        self.assertEqual(ret_str, inputToSend)

    def testSimpleSendReceiveDeterministicDrop2(self):
        with open("sampleInput.txt", "r") as f:
            inputToSend = f.read()
        sender = Sender(0.2, inputToSend, "1.1.1.1", "2.2.2.2", 11111, 22222)
        k,m = sender.getkm()

        sender.encode()
        packets = list(sender.packetQueue)
        lenpackets = len(packets)

        # drop some packets
        drop_rate = 0
        packetsReceived = []
        for _ in range(k):
            rand_i = random.randint(0, len(packets)-1)
            packetsReceived.append(packets[rand_i])
            del packets[rand_i]

        print(f"Started with {lenpackets} packets, received {len(packetsReceived)} packets at the receiver. {lenpackets - len(packetsReceived)} packets were dropped.")

        receiver = Receiver(k,m, "2.2.2.2")

        receiver.buffer = packetsReceived
        receiver.decode()
        ret_str = receiver.postProcess()

        self.assertEqual(ret_str, inputToSend)



if __name__ == '__main__':
    unittest.main()