import socket
import select
import time
import scapy.all
import struct
from _thread import *
import threading

print_lock = threading.Lock()
latch = threading.Condition()

def Main():
    HOST = scapy.all.get_if_addr('eth1')                    # Host IP
    PORT = 13000			                                # specified PORT to connect

    tcp_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	#make IP address reusable
    tcp_sock.bind((HOST,PORT))
    tcp_sock.listen()
    print ("Server started, listening on IP address ",HOST)
    while True:
        start_server(PORT,tcp_sock)
        game_mode()


def start_server(PORT,tcp_sock):
    udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP socket
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcast ??

    DEST_PORT = 13117                                               # destenation PORT for broadcast
    BROADCAST_ADDR = '172.1.255.255' #'172.1.255.255'              # broadcast IP
    offer_str = make_offer(PORT)

    nextCastTime = time.time()                                      # When we want to send the next periodic-ping-message out
    start_time=nextCastTime
    
    while (start_time+10>=time.time()):
        secondsUntilNextCast = nextCastTime - time.time()
        if (secondsUntilNextCast < 0):    
            secondsUntilNextCast = 0


                                                                    # select() won't return until 'udp_sock' has some data
                                                                    # ready-for-read, OR until secondsUntilNextPing seconds
                                                                    # have passed, whichever comes first
        ready_to_read_list, _ , _ = select.select([tcp_sock], [], [], secondsUntilNextCast) #using select timeout in order to time 
        if (tcp_sock in ready_to_read_list):                   # There's an a new TCP connection to accept!
            gather_client(tcp_sock)
        
        now = time.time()
        if (now >= nextCastTime):
            # Time to send out the next Cast!
            print ("Sending out scheduled Cast at time ", now)
            udp_sock.sendto(offer_str, (BROADCAST_ADDR, DEST_PORT))
            nextCastTime = now + 1.0   # do it again in another second
    latch.acquire()
    latch.notify_all()
    latch.release()


def make_offer(port):
    offer=struct.pack('IBH',0xfeedbeef,0x2,port)
    print(offer)
    return offer


def gather_client(tcp_sock):
    try:
        # tcp_sock.setblocking(0)
        client_sock,addr=tcp_sock.accept()
        team_name = client_sock.recvfrom(100)
        print(team_name)
        start_new_thread(thread_life, (client_sock,team_name))
        
    except:
        print("no new connections")


def thread_life(c,team_name):
    latch.acquire()
    latch.wait()
    latch.release()
    print('thread \'', team_name , '\' is ready!!')

    while True:
        # data received from client
        data = c.recv(1024)
        if not data:
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

        # connection closed
    c.close()


def sign_up():
    print("not yet implimented")


def game_mode():
    print("not yet implimented")
    init_game_data()


def init_game_data():
    print("not yet implimented")


if __name__ == '__main__':
	Main() 