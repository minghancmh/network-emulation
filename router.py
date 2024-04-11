import socket
import struct

# Define the multicast group and port
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the time-to-live for messages to 1
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Bind the socket to a specific interface and port
sock.bind(server_address)

# Join the multicast group
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive and process incoming messages
while True:
    data, address = sock.recvfrom(1024)
    # Process the received data
    # ...

# Close the socket
sock.close()
