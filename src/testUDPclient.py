
import socket
import scapy.all
import struct
import fcntl, os

def Main():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP socket
	# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #enable broadcast ??
	# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #enable broadcast ??

	udp_host = scapy.all.get_if_addr('eth1')               # The server's hostname or IP address
	udp_port = 13117			        # specified port to connect

	msg = "Hello Python! from sharon & gil"
	print ("UDP host IP:", udp_host)
	print ("UDP host Port:", udp_port)

	# sock.sendto(msg.encode(),(udp_host,udp_port))		# Sending message to UDP server

	sock.bind(("",udp_port))

	def verify_message(data):
		magic_cookie, message_type, port = struct.unpack('IBh', data)
		if(magic_cookie==0xfeedbeef and type==2):
			return port
		else:
			return None



	while True:
		print ("Waiting for server...")
		data,addr = sock.recvfrom(1024)#receive data from client
		port=verify_message(data)
		if(port):
			make_tcp_connection(addr,port)


def make_tcp_connection(host,port):
	team_name = "Maccabi Kushilamam City\n"
	try:
		tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_sock.settimeout(10.0)
		# connect to server on local computer
		tcp_sock.connect((host, port))
		#make tcp-socket non blocking
		#tcp_sock.setblocking(0)
		#fcntl.fcntl(tcp_sock, fcntl.F_SETFL, os.O_NONBLOCK)
		# message you send to server
		tcp_sock.send(team_name.encode('ascii'))
	except:
		print("failed while connecting to server or while sending team name")
		return False
	try:
		tcp_sock.settimeout(10.0)
		data = tcp_sock.recv(4096)
		if(data):
			print(str(data.decode('ascii')))
			game_mode(tcp_sock)
			print("Server disconnected, listening for offer requests...")
			return True
		else:
			print("got empty message from server after sending team name")
			return False
	except:
		print("failed after sending team name")
		return False

#TODO:close the connection after game mode
def game_mode(tcp_sock):
	while True:
		str = input()
		try:
			tcp_sock.send(str.encode())
		except:
			break


if __name__ == '__main__':
	Main()
