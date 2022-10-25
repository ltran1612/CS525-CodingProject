# If we want to be parallel and not just concurrent, we need to use Pool 
import socket
from termios import CKILL
from Crypto.Cipher import AES
from Crypto import Random

from cbc import *

if __name__ == "__main__": 
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))

	# initialization
	set_up = False
	key = None
	block_size = None
	IV = None
	e_algo = ""
	d_algo = ""
	while not set_up:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		value, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		if data == "key":
			key = value
		elif data == "block_size":
			block_size = int(value)
		elif data == "IV":
			IV = int(value)
		else:
			print("ERROR: Invalid set up step")
			exit(1)
		set_up = key != None and block_size != None and IV != None
