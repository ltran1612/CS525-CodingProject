# If we want to be parallel and not just concurrent, we need to use Pool or multiprocessing; that is multiple child processes instead of threads. 
# However, with multiple processes, we cannot pass our class and the encryption/decryption algorithm to the child processes because they contain pointers that cannot be serialized. 
import socket
import time
import threading
from multiprocessing import Pool

from termios import CKILL
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA

from cbc import *
from ofb import *
from ctr import *

def handler(x):
	print(x, flush=True)

def decrypt_block_ofb_multiprocess(block, random_nums, block_size):
	index = int.from_bytes(block[:4], "little")

	random_num = random_nums[index]
	random_num = int.from_bytes(random_num, "little")

	c_block = int.from_bytes(block[4:], "little")
	
	p_block = c_block ^ random_num
	p_block = int.to_bytes(p_block, block_size, "little")
	p_block = p_block.decode("utf-8")

	return p_block, index

def decrypt_block_ctr_multiprocess(block, random_nums, block_size):
	index = int.from_bytes(block[:4], "little")

	random_num = random_nums[index]
	random_num = int.from_bytes(random_num, "little")

	c_block = int.from_bytes(block[4:], "little")
	
	p_block = c_block ^ random_num
	p_block = int.to_bytes(p_block, block_size, "little")
	p_block = p_block.decode("utf-8")

	return p_block, index

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
	message_path = ""

	sender_address = ""
	# start initializating
	message_size = 3000000
	while not set_up:
		data, sender_address = sock.recvfrom(message_size) # buffer size is 1024 bytes
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
		elif val_code == 5: # encryption mode
			encrypt_code = int.from_bytes(value, "little")
		elif val_code == 6: # blocks num
			block_nums = int.from_bytes(value, "little")
		elif val_code == 7: # original message path
			message_path = value.decode("utf-8")
		else:
			print("ERROR: Invalid set up step")
			exit(1)
		set_up = key != None and block_size != None and IV != None and algo_code != None and encrypt_code != None and block_nums != None and message_path != ""
	
	cipher = None
	e_algo = None
	d_algo = None
	algo_block_size = None
	if algo_code == 1:
		cipher = AES.new(key, AES.MODE_ECB)
		e_algo = cipher.encrypt
		d_algo = cipher.decrypt
		algo_block_size = 16
	else: # meant for RSA, but we was not able to do it in RSA
		print("Invalid input")
		exit(1)
		public_key = None
		private_key = None
		with open("public.pem") as f:
			public_key = RSA.import_key(f.read())
		with open("private.pem") as f:
			private_key = RSA.import_key(f.read())
		cipher = PKCS1_OAEP.new(public_key)
		e_algo = cipher.encrypt
		cipher = PKCS1_OAEP.new(private_key)
		d_algo = cipher.decrypt
	
	encrypt_mode = None
	if encrypt_code == 2:
		print("OFB")
		encrypt_mode = OFB(IV, block_size, key, e_algo, d_algo, algo_block_size)
	elif encrypt_code == 3:
		print("CTR")
		encrypt_mode = CTR(IV, block_size, key, e_algo, d_algo, algo_block_size)
	else:
		print("CBC")
		# create a cbc object
		encrypt_mode = CBC(IV, block_size, key, e_algo, d_algo, algo_block_size)
	
	random_nums = None
	if encrypt_code == 2 or encrypt_code == 3: #OFB
		encrypt_mode.set_block_num(block_nums)
		encrypt_mode.calculate_xor_nums()
		random_nums = encrypt_mode.get_random_nums()
	print("set up done")
	print(block_nums)
	# set up done
	# report back to the sender
	# tell them to start sending data
	sock.sendto(int.to_bytes(1, 1, "little"), sender_address)

	# waiting for data
	decrypted_message = ""
	if encrypt_code == 2: #OFB
		results = [None] * block_nums

		pool = Pool()
		for i in range(block_nums):
			block, addr = sock.recvfrom(encrypt_mode.get_total_size(block_size))
			
			try:
				x = pool.apply_async(decrypt_block_ofb_multiprocess, (block, random_nums, block_size)) 
				results[i] = x
			except Exception:
				print("error starting a process")
		
		# close the pool
		pool.close()
		# wait for the threads to finish
		pool.join()
		plaintexts = [None] * block_nums

		# we're done
		# organize the plaintexts blocks
		for i in range(block_nums):
			plaintext, index = results[i].get()
			plaintexts[index] = plaintext
		decrypted_message = "".join(plaintexts)
	elif encrypt_code == 3: # CTR
		results = [None] * block_nums

		pool = Pool()
		for i in range(block_nums):
			block, addr = sock.recvfrom(encrypt_mode.get_total_size(block_size))
			#print(i)
			try:
				x = pool.apply_async(decrypt_block_ctr_multiprocess, (block, random_nums, block_size)) 
				results[i] = x
			except Exception:
				print("error starting a process")
		
		# close the pool
		pool.close()
		#print("waiting")
		# join the pool
		pool.join()
		
		plaintexts = [None] * block_nums

		# organizing values
		for i in range(block_nums):
			plaintext, index = results[i].get()
			plaintexts[index] = plaintext
		decrypted_message = "".join(plaintexts)
	else: # CBC
		threads = []
		# create a cbc object
		for i in range(block_nums):
			block, addr = sock.recvfrom(encrypt_mode.get_total_size(block_size))
			encrypt_mode.add_cipher_block(block)
			
			try:
				x = threading.Thread(target=encrypt_mode.decrypt_block, args=(block,))
				x.start()
				threads.append(x)
			except Exception:
				print("error starting a process")
		# wait for threads to finish
		#print("waiting for")
		for thread in threads:
			thread.join()
		
		# get the message
		decrypted_message = encrypt_mode.get_decrypted_message()

	end_time = time.perf_counter_ns()
	original_message = ""
	with open(message_path) as f:
			original_message = "\n".join(f.readlines())
	#print("Decrypted message: ", decrypted_message)
	#print("Original message: ", original_message)

	# we crop this to remove the paddings
	print("Are they the same (noted, the decrypted string is cropped to the length of the original message to remove paddings)?", decrypted_message[:len(original_message)] == original_message)

	# write the end time.
	with open("receiver.csv", "a") as outfile:
		outfile.write(str(end_time) + "\n")

	

