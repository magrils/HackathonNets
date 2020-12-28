import socket
import select
import time
import scapy.all
import struct

def Main(): 
    start_server()

def start_server():
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP socket
    # udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #enable broadcast ??
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcast ??
    
    
    #udp_host = socket.gethostname()		    
    HOST = scapy.all.get_if_addr('eth1')		                                # Host IP
    PORT = 13000			                                # specified PORT to connect
    DEST_PORT = 13117                                       # destenation PORT for broadcast
    BROADCAST_ADDR = '172.17.255.255' #'172.1.255.255'            # broadcast IP
    offer_str = make_offer(PORT)
    
    # udp_sock.bind((HOST,PORT))
    print ("Server started, listening on IP address ",HOST)
    
    # When we want to send the next periodic-ping-message out
    nextCastTime = time.time()
 
    # for now using 'select()' for multiplex the two tasks, consider changing to two threads
    while True:
        secondsUntilNextCast = nextCastTime - time.time()
        if (secondsUntilNextCast < 0):    
            secondsUntilNextCast = 0

        # select() won't return until 'udp_sock' has some data
        # ready-for-read, OR until secondsUntilNextPing seconds 
        # have passed, whichever comes first
        inReady, _ , _ = select.select([udp_sock], [], [], secondsUntilNextCast)

        if (udp_sock in inReady):
            # There's an incoming UDP packet ready to receive!
            print(udp_sock.recvfrom(100))
            gather_client()

        now = time.time()
        if (now >= nextCastTime):
            # Time to send out the next Cast!
            print ("Sending out scheduled Cast at time ", now)
            udp_sock.sendto(offer_str, (BROADCAST_ADDR, DEST_PORT))
            nextCastTime = now + 1.0   # do it again in another second

def make_offer(port):
    offer=struct.pack('IBh',0xfeedbeef,0x2,port)
    print(offer)
    return offer


def gather_client():
    print("method gather_client not yet inplemented")

if __name__ == '__main__': 
	Main() 