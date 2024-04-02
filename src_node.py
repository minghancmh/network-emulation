
import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Specify the multicast group address and port
multicast_group = ('224.3.29.71', 10000)

# Set the time-to-live (TTL) for multicast packets
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# Generate multicast packets and send them
message = 'This is a multicast message'

sock.sendto(message.encode('utf-8'), multicast_group)