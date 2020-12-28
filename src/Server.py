import socket
def Main(): 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # UDP socket

    #udp_host = socket.gethostname()		        # Host IP
    udp_host = '127.0.0.1'		        # Host IP
    udp_port = 13117			                # specified port to connect

    #print type(sock) ============> 'type' can be used to see type 
                    # of any variable ('sock' here)

    sock.bind((udp_host,udp_port))

    
    print ("host ip:",udp_host," port:",udp_port,"\n")
    while True:
        print ("Waiting for client...")
        data,addr = sock.recvfrom(1024)	        #receive data from client
        print ("Received Messages:",data," from",addr)


if __name__ == '__main__': 
	Main() 