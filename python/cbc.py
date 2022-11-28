from encryption_mode import EncryptionMode

class CBC(EncryptionMode):
    # Constructor
    # IV: the initial IV
    # block_size: the number of bytes the block have
    # key: the key to the encryption and decryption algorithm
    # e_algo: the encryption algorithm function
    # d_algo: the decryption algorithm function
    def __init__(self, IV, block_size, key, e_algo, d_algo):
       super().__init__(IV, block_size, key, e_algo, d_algo)
       self.cipher_blocks = {0: IV}

    # get a block from the disk 
    def get_block(self, block_index):
        if block_index >= self.blocks_num:
            return None

        # set and increment the index
        index = block_index

        # get the next block and convert it into int
        p_block = self.blocks[index]
        p_block = int.from_bytes(p_block, "little")

        # get the last block and convert it into int
        last_block = int.from_bytes(self.cipher_blocks[index], "little")

        # xor the two numbers and convert it into a bytes object
        c_block = p_block ^ last_block #what to do if the number of bits of number is bigger than block size. 
        c_block = int.to_bytes(c_block, self.block_size, "little")

        # run the encryption algorithm on the bytes object
        c_block = self.e_algo(c_block)

        # add a new cipher text block
        self.cipher_blocks[index + 1] = c_block
       
        return self.add_index_to_block(c_block, block_index)
   
    def add_cipher_block(self, block):
        index = int.from_bytes(block[:4], "little")
        self.cipher_blocks[index+1] = block[4:]

    # decrypt a block
    def decrypt_block(self, block):
        index = int.from_bytes(block[:4], "little") 
        c_block = block[4:]
        
        while not index in self.cipher_blocks :
            pass

        last_block = self.cipher_blocks[index]

        p_block = int.from_bytes(self.d_algo(c_block), "little") ^ int.from_bytes(last_block, "little")
        result = int.to_bytes(p_block, self.block_size, "little")
        #print("decrypted block", result)
        self.result[index] = result
        return result