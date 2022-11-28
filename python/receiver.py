# If we want to be parallel and not just concurrent, we need to use Pool 
import socket
import time
import threading

from termios import CKILL
from Crypto.Cipher import AES
from Crypto import Random

from cbc import *

def handler(x):
	print(x, flush=True)

if __name__ == "__main__": 
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))

	#initialization
	set_up = False
	key = None
	block_size = None
	block_nums = None
	IV = None
	algo_code = None
	encrypt_code = None

	# start initializating
	message_size = 3000000
	while not set_up:
		data, addr = sock.recvfrom(message_size) # buffer size is 1024 bytes
		val_code = int.from_bytes(data[:8], "little")
		value = data[8:]
		if val_code == 0: # block size
			block_size = int.from_bytes(value, "little")
		elif val_code == 1: # IV
			IV = value
		elif val_code == 2: # key
			key = value
		elif val_code == 3: # algorithm
			algo_code = int.from_bytes(value, "little")
			# set the algorithm here
		elif val_code == 5: # encryption mode
			encrypt_code = int.from_bytes(value, "little")
		elif val_code == 6: # blocks num
			block_nums = int.from_bytes(value, "little")
		else:
			print("ERROR: Invalid set up step")
			exit(1)
		set_up = key != None and block_size != None and IV != None and algo_code != None and encrypt_code != None and block_nums != None
	
	cipher = None
	e_algo = None
	d_algo = None
	if algo_code == 1:
		cipher = AES.new(key, AES.MODE_ECB)
		e_algo = cipher.encrypt
		d_algo = cipher.decrypt 
	
	encrypt_mode = None
	if encrypt_code == 2:
		pass
	elif encrypt_code == 3:
		pass
	else:
		# create a cbc object
		encrypt_mode = CBC(IV, block_size, key, e_algo, d_algo)
	
	print("set up done")

	
	result = []

	end_time = time.perf_counter_ns()
	if encrypt_code == 2:
		pass
	elif encrypt_code == 3:
		pass
	else:
		threads = []
		# create a cbc object
		for i in range(block_nums):
			block, addr = sock.recvfrom(encrypt_mode.get_total_size(block_size))
			print("cipher blocks", block)
			encrypt_mode.add_cipher_block(block)
			
			try:
				x = threading.Thread(target=encrypt_mode.decrypt_block, args=(block,))
				x.start()
				threads.append(x)
			except Exception:
				print("error starting a process")
		
		for thread in threads:
			thread.join()
		print(encrypt_mode.get_decrypted_message())
	#print(data)
	with open("receiver.csv", "w") as outfile:
		outfile.write(str(end_time))
	

