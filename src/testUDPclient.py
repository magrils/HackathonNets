
import socket
import scapy.all
import struct


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP socket
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #enable broadcast ??
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcast ??

udp_host = scapy.all.get_if_addr('eth1')               # The server's hostname or IP address
udp_port = 13117			        # specified port to connect

msg = "Hello Python! from sharon & gil"
print ("UDP host IP:", udp_host)
print ("UDP host Port:", udp_port)

# sock.sendto(msg.encode(),(udp_host,udp_port))		# Sending message to UDP server

sock.bind(('172.1.255.255',udp_port))

while True:
	print ("Waiting for server...")
	message,addr = sock.recvfrom(1024)	        #receive data from client
	print ("Received Messages:",message," from",addr)
