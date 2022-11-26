from random import random


class OFB:
    # Constructor
    # IV: the initial IV
    # block_size: the number of bytes the block have
    # key: the key to the encryption and decryption algorithm
    # e_algo: the encryption algorithm function
    # d_algo: the decryption algorithm function
    def __init__(self, IV, block_size, key, e_algo, d_algo):
        super.__init__()
        self.random_nums = [IV]
    
    def calculate_xor_nums(self):
        for i in range(1, self.blocks_num):
            num = self.random_nums[i-1]
            num = self.e_algo(num)
            self.random_nums.append(num)
                               
    # get a block from the disk 
    def get_block(self, block_index):
        if block_index >= self.blocks_num:
            return None

        # set and increment the index
        index = block_index

        # get the next block and convert it into int
        p_block = self.blocks[index]
        p_block = int.from_bytes(p_block, "little")

        # encrypt the last random number    
        random_num = self.random_nums[index]
        random_num = int.from_bytes(random_num, "little")

        # xor the two numbers and convert it into a bytes object
        c_block = p_block ^ random_num #what to do if the number of bits of number is bigger than block size. 
        c_block = int.to_bytes(c_block, self.block_size, "little")
       
        return c_block
        
   
    # decrypt a block
    def decrypt_block(self, block):
        index = self.block_index
        self.block_index = index + 1

        random_num = self.random_nums[index]
        random_num = int.from_bytes(random_num, "little")

        c_block = int.from_bytes(block, "little")
        
        p_block = c_block ^ random_num

        return int.to_bytes(p_block, self.block_size, "little")