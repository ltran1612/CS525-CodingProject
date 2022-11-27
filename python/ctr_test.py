from Crypto.Cipher import AES
from Crypto import Random

from ctr import *

if __name__ == "__main__": 
	# set up
	block_size = 16
	IV = Random.new().read(block_size)
	key = Random.new().read(32)
	cipher = AES.new(key, AES.MODE_ECB)
	e_algo = cipher.encrypt
	d_algo = cipher.decrypt

	original_message = "helllo there my name is long, nice to meet you, hallo, dance, think before you do, be bold, code the future, power, sing, song 123"

	# create a ctr object
	ctr = CTR(IV, block_size, key, e_algo, d_algo)
	ctr.set_message(original_message)

	# get the encryption blocks
	block_to_send = ctr.get_block(0)
	blocks = []
	index = 1
	while block_to_send != None:
		blocks.append(block_to_send)
		print("encrypted block: ", block_to_send)
		#sock.sendto(block_to_send, (UDP_IP, UDP_PORT))
		block_to_send = ctr.get_block(index)
		index = index + 1

	# decrypt the blocks
	ctr = CTR(IV, block_size, key, e_algo, d_algo)
	plain_texts = []
	for block in blocks:
		plain_block = ctr.decrypt_block(block)
		print("decrypted block",plain_block)
		message = plain_block.decode("utf-8")
		plain_texts.append(message)
	
	print(original_message)
	decrypted_message = "".join(plain_texts)
	print(decrypted_message)
	len1 = len(original_message)
	decrypted_message = decrypted_message[:len1]
	print("same?", original_message == decrypted_message)
		


