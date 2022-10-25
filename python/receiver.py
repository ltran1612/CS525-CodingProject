# If we want to be parallel and not just concurrent, we need to use Pool 
import socket

if __name__ == "__main__": 
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print("received message: %s" % data)