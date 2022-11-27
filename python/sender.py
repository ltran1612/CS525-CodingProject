# If we want to be parallel and not just concurrent, we need to use Pool 
import socket
import time
import sys

from Crypto.Cipher import AES
from Crypto import Random

from cbc import *



if __name__ == "__main__": 
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


	while True:	
		try:
			# block size
			block_size = int(input("Enter block size: "))
		except Exception:
			print("")
		
		# set up other parameters
		IV = Random.new().read(block_size) # IV
		key = Random.new().read(32) # key for the encryption
		
		# pick the encryption algorithm
		cipher = AES.new(key, AES.MODE_ECB)
		e_algo = cipher.encrypt
		d_algo = cipher.decrypt

		opt = int(input("""Pick the encryption algorithm from the following list:
		1) AES (default)
		2) ...
		"""))

		if opt == 1:
			cipher = AES.new(key, AES.MODE_ECB)
			e_algo = cipher.encrypt
			d_algo = cipher.decrypt
		else:
			print("Other option not available")
		
		# send these information to the receiver


		# pick message
		original_message = "helllo there my name is long, nice to meet you, hallo, dance, think before you do, be bold, code the future, power, sing, song 123"
		
		# pick cipher mode
		opt = int(input("""Pick the cipher mode from the following list: 
		1) CBC (default)
		2) OFB
		3) CTR
		"""))

		encrypt_mode = None
		if opt == 2:
			pass
		elif opt == 3:
			pass
		else:
			# create a cbc object
			cbc = CBC(IV, block_size, key, e_algo, d_algo)
			cbc.set_message(original_message)

		# set the message size
		block_nums = encrypt_mode.get_size()
		#print(block_nums)

		start_time = time.perf_counter_ns()
		# do stuffs here
		# get the encryption blocks
		# block_to_send = cbc.get_block(0)
		# index = 1
		# while block_to_send != None:
		# 	print("encrypted block: ", block_to_send)
		# 	sock.sendto(block_to_send, (UDP_IP, UDP_PORT))
		# 	block_to_send = cbc.get_block(index)
		# 	index = index + 1
		# send the message size
		sock.sendto(int.to_bytes(block_nums, 4, "little"), (UDP_IP, UDP_PORT))

		with open("sender.csv", "w") as outfile:
			outfile.write(start_time)
	

			
		


