import socket
import select
import time
import scapy.all
import struct
from _thread import *
import threading

print_lock = threading.Lock()

def Main():
    HOST = '172.17.0.1' #scapy.all.get_if_addr('eth1')        # Host IP
    print(HOST)
    PORT = 13000			                                # specified PORT to connect

    tcp_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((HOST,PORT))
    tcp_sock.listen()
    print ("Server started, listening on IP address ",HOST)
    while True:
        start_server(PORT,tcp_sock)

def start_server(PORT,tcp_sock):
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP socket
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcast ??



    DEST_PORT = 13117                                               # destenation PORT for broadcast
    BROADCAST_ADDR = '172.17.255.255' #'172.1.255.255'              # broadcast IP
    offer_str = make_offer(PORT)

    nextCastTime = time.time()                                      # When we want to send the next periodic-ping-message out
    start_time=nextCastTime
    # for now using 'select()' for multiplex the two tasks, consider changing to two threads
    while (start_time+10>=time.time()):
        secondsUntilNextCast = nextCastTime - time.time()
        if (secondsUntilNextCast < 0):    
            secondsUntilNextCast = 0

                                                                    # select() won't return until 'udp_sock' has some data
                                                                    # ready-for-read, OR until secondsUntilNextPing seconds
                                                                    # have passed, whichever comes first
        inReady, _ , _ = select.select([udp_sock], [], [], secondsUntilNextCast)
        print(len(inReady))
        # if (tcp_sock in inReady):
        #     # There's an incoming TCP packet ready to receive!

        now = time.time()
        if (now >= nextCastTime):
            # Time to send out the next Cast!
            print ("Sending out scheduled Cast at time ", now)
            udp_sock.sendto(offer_str, (BROADCAST_ADDR, DEST_PORT))
            gather_client(tcp_sock)
            nextCastTime = now + 1.0   # do it again in another second


def threaded(c):
    while True:
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

        # connection closed
    c.close()

def make_offer(port):
    offer=struct.pack('IBh',0xfeedbeef,0x2,port)
    print(offer)
    return offer


def gather_client(tcp_sock):
    try:
        tcp_sock.setblocking(0)
        c,addr=client_sock,addr=tcp_sock.accept()
        start_new_thread(threaded, (c,))
        print(client_sock.recvfrom(100))
    except:
        print("test print error")


if __name__ == '__main__':
	Main() 