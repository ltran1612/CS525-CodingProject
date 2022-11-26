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
       self.last_block = IV

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
        last_block = int.from_bytes(self.last_block, "little")

        # xor the two numbers and convert it into a bytes object
        c_block = p_block ^ last_block #what to do if the number of bits of number is bigger than block size. 
        c_block = int.to_bytes(c_block, self.block_size, "little")

        # run the encryption algorithm on the bytes object
        c_block = self.e_algo(c_block)

        # set last block to this block
        self.last_block = c_block
       
        return self.add_index_to_block(c_block, block_index)

   
    # decrypt a block
    def decrypt_block(self, block):
        c_block = block[4:]
        p_block = int.from_bytes(self.d_algo(c_block), "little") ^ int.from_bytes(self.last_block, "little")
        self.last_block = c_block
        result = int.to_bytes(p_block, self.block_size, "little")
        return result