# If we want to be parallel and not just concurrent, we need to use Pool 
import socket
import time
import sys

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA

from cbc import *
from ofb import *
from ctr import *

if __name__ == "__main__": 
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.setblocking(False)

	block_size = None
	try:
		# block size
		block_size = int(input("Enter block size:\n"))
	except Exception:
		print("End of input reading")
		exit(0)
	
	# default algorithm is AES
	# set up other parameters
	IV = Random.new().read(block_size) # IV
	key = Random.new().read(32) # key for the encryption
	# pick the encryption algorithm
	cipher = AES.new(key, AES.MODE_ECB)
	e_algo = cipher.encrypt
	d_algo = cipher.decrypt
	
	
	opt = None
	try:
		opt = int(input(
"""Pick the encryption algorithm from the following list:
	1) AES (default)
"""))
	except Exception:
		print("")
		exit(0)
	algo_code = opt
	if algo_code == 2: # meant for RSA, but we got into some problems with the RSA of pycryptodome.
		print("Invalid input")
		exit(1)
		key = RSA.generate(2048)
		keys = (key, key.public_key())

		with open("private.pem", "wb") as f:
			f.write(keys[0].export_key())
		
		with open("public.pem", "wb") as f:
			f.write(keys[1].export_key())

		cipher = PKCS1_OAEP.new(keys[1])
		e_algo = cipher.encrypt
		cipher = PKCS1_OAEP.new(keys[0])
		d_algo = cipher.decrypt
		key = b'0'
	else: # AES
		key = Random.new().read(32)
		cipher = AES.new(key, AES.MODE_ECB)
		e_algo = cipher.encrypt
		d_algo = cipher.decrypt

		if block_size != 16:
			print("The AES used in this experiment does not support other block sizes other than 16")
		
	# test message is in test_message.txt
	message_path = "test_message.txt"
	
	original_message = ""
	with open(message_path) as f:
		original_message = "\n".join(f.readlines())
	
	# pick cipher mode
	try:
		opt = int(input(
"""Pick the cipher mode from the following list: 
	1) CBC (default)
	2) OFB
	3) CTR
"""))
	except Exception:
		print("")
		exit(0)
	
	# create the objects for each encryption mode
	encrypt_code = opt
	encrypt_mode = None
	if encrypt_code == 2: #OFB
		encrypt_mode = OFB(IV, block_size, key, e_algo, d_algo)
	elif encrypt_code == 3: #CTR
		encrypt_mode = CTR(IV, block_size, key, e_algo, d_algo)
	else: # CBC
		encrypt_mode = CBC(IV, block_size, key, e_algo, d_algo)
		
	# set the message
	encrypt_mode.set_message(original_message)
	# set the message size
	block_nums = encrypt_mode.get_size()

	# send these information to the receiver
	# send block size
	message = bytearray()
	for value in int.to_bytes(0, 8, "little"):
		message.append(value)
	for value in int.to_bytes(block_size, 8, "little"):
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))

	# send IV
	message = bytearray()
	for value in int.to_bytes(1, 8, "little"):
		message.append(value)
	for value in IV:
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))

	# send key
	message = bytearray()
	for value in int.to_bytes(2, 8, "little"):
		message.append(value)
	for value in key:
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))

	# send algorithm option
	message = bytearray()
	for value in int.to_bytes(3, 8, "little"):
		message.append(value)
	for value in int.to_bytes(algo_code, 8, "little"):
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))

	# send cipher mode
	message = bytearray()
	for value in int.to_bytes(5, 8, "little"):
		message.append(value)
	for value in int.to_bytes(encrypt_code, 8, "little"):
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))
	
	# send blocks number
	message = bytearray()
	for value in int.to_bytes(6, 8, "little"):
		message.append(value)
	for value in int.to_bytes(block_nums, 8, "little"):
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))

	# send mesage pat
	message = bytearray()
	for value in int.to_bytes(7, 8, "little"):
		message.append(value)
	for value in bytes(message_path, "utf-8"):
		message.append(value)
	sock.sendto(message, (UDP_IP, UDP_PORT))

	# wait for the report from the receiver that the receiver has finished setting up.
	sock.setblocking(True)
	value, addr = sock.recvfrom(1024)
	value = int.from_bytes(value, "little")
	if value == 1: # set up successful
		print("set up successful")
		sock.setblocking(False)
	else:
		print("set up failed")
		exit(1)

	# special cases for OFB
	if encrypt_code == 2: # OFB
		encrypt_mode.calculate_xor_nums()
		
	# start sending the cipher blocks
	start_time = time.perf_counter_ns()
	if encrypt_code == 2: # OFB
		for i in range(block_nums):
			block = encrypt_mode.get_block(i)
			sock.sendto(block, (UDP_IP, UDP_PORT))
	elif encrypt_code == 3: # CTR
		for i in range(block_nums):
			block = encrypt_mode.get_block(i)
			sock.sendto(block, (UDP_IP, UDP_PORT))
	else: # CBC
		for i in range(block_nums):
			block = encrypt_mode.get_block(i)
			sock.sendto(block, (UDP_IP, UDP_PORT))
	
	# write the start time
	with open("sender.csv", "a") as outfile:
		outfile.write(str(start_time) + "\n")


			
		


