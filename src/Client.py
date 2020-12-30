import select
import socket
import sys
import time
import scapy.all
import struct
import fcntl, os
import getch

GAME_DURATION=10

def Main():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  	# UDP socket
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	#make IP address reusable

	udp_host = '172.17.0.1'#scapy.all.get_if_addr('eth1')				# The server's hostname or IP address
	udp_port = 13117			        					# specified port to connect

	print ("UDP host IP:", udp_host)
	print ("UDP host Port:", udp_port)

	# sock.sendto(msg.encode(),(udp_host,udp_port))		# Sending message to UDP server

	sock.bind(("",udp_port))

	def verify_message(data):
		try:
			magic_cookie, message_type, port = struct.unpack('IBH', data)
			if((magic_cookie==0xfeedbeef) and (message_type==2)):
				return port
			else:
				return None
		except:
			return None


	while True:
		print ("Waiting for server...")
		data,addr = sock.recvfrom(1024)				#receive data from client
		(host,_)=addr
		port=verify_message(data)
		print("server: ",addr[0]," ,",port)
		if(port):
			make_tcp_connection(host,port)


def make_tcp_connection(host,port):
	team_name = "Maccabi Kushilamam City\n"
	try:
		tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# tcp_sock.settimeout(10.0)
		tcp_sock.connect((host, port))					# connect to server on local computer
	except:
		#print("failed while connecting to server")
		return False
	try:
		# message you send to server
		tcp_sock.send(team_name.encode('ascii'))
	except:
		# print("failed while sending team name")
		return False
	try:
		# tcp_sock.settimeout(10.0)
		data = tcp_sock.recv(4096)
		if(data):
			print(str(data.decode('ascii')))
			game_mode(tcp_sock)

			# print("Server disconnected, listening for offer requests...")
		else:
			# print("got empty message from server after sending team name")
			return False
	except:
		# print("failed after sending team name")
		return False
	try:
		tcp_sock.close()
		return True
	except:
		print("failed in properly closing the connection to server")
		return False


def game_mode(tcp_sock):
	sys.stdin.flush()
	end_game_time= time.time()+GAME_DURATION
	while True:
		try:
			to_read, _, _ = select.select([sys.stdin], [], [], (end_game_time - time.time()))
			if (to_read):
				x=getch.getch()
			#print("you typed in\ " + x)
			tcp_sock.send(x.encode())
		except:
			break
	try:
		summary_msg=tcp_sock.recv(1024)
		if(summary_msg):
			print(summary_msg.decode())
	except:
		print("getting summary message failed")


if __name__ == '__main__':
	Main()
