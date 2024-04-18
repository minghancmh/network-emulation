import argparse
import ipaddress
from sender import Sender
from utils import Packet

parser = argparse.ArgumentParser(
    prog="Sender",
    description="This program sends a payload to a certain ip address",
)

parser.add_argument('--inputText', help=".txt file for input payload")
parser.add_argument('--receiverIP', help="IPv4 address for the receiver node.")
parser.add_argument('--redundancyFactor', help=" A scalar factor which determines how many extra packets are going to be generated")
parser.add_argument('--senderIP', help="IPv4 address of the sending node (ie this node)")




args = parser.parse_args()
assert args.inputText != None, "Please provide an input file."
assert args.receiverIP != None, "Please provide a receiver IP."
assert args.redundancyFactor != None, "Please provide a redundancy factr."
assert args.senderIP != None, "Please provide a senderIP."


inputTextFilePath : str = args.inputText
receiverIP: ipaddress.IPv4Address = ipaddress.ip_address(args.receiverIP)
redundancyFactor: float = float(args.redundancyFactor)
senderIP: ipaddress.IPv4Address = ipaddress.ip_address(args.senderIP)



print(f"""
      \n=====ARGUMENTS RECEIVED=====\
      \ninputTextFile: {inputTextFilePath}\
      \nreceiverIP: {receiverIP}\
      \nsenderIP: {senderIP}\
      \nredundancyFactor: {redundancyFactor}\n
      """)

with open(inputTextFilePath, 'r') as f:
    inputToSend = f.read()


sender = Sender(redundancyFactor, inputToSend, senderIP, receiverIP, 8080, 8080)
sender.displaySenderAttributes()
sender.encode()
# sender.printAllPacketsInQueue()
packetToSend: Packet = Packet(sender.packets[0], 1, sender.sourcePort, sender.destinationPort, len(sender.packets[0]), sender.sourceIP, sender.destinationIP)
sender.send(packetToSend)





