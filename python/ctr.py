from random import random
from encryption_mode import EncryptionMode


class CTR(EncryptionMode):
    # Constructor
    # IV: the initial IV
    # block_size: the number of bytes the block have
    # key: the key to the encryption and decryption algorithm
    # e_algo: the encryption algorithm function
    # d_algo: the decryption algorithm function
    def __init__(self, IV, block_size, key, e_algo, d_algo, algo_block_size):
       super().__init__(IV, block_size, key, e_algo, d_algo, algo_block_size)
       self.IV = IV
       self.IV_num = int.from_bytes(IV, "little")
       self.random_nums = []
    
    def calculate_xor_nums(self):
        for i in range(0, self.blocks_num):
            random_num = int.to_bytes(self.IV_num + i, self.block_size, "little")

            rb = [random_num[i:i + self.algo_block_size] for i in range(0, len(random_num), self.algo_block_size)]
            random_num = bytearray()
            for value in rb:
                temp = self.e_algo(value)
                for value in temp:
                    random_num.append(value)
            self.random_nums.append(bytes(random_num))
    
    def get_random_nums(self):
        return self.random_nums
    
    def set_block_num(self, num):
        self.blocks_num = num
                               
                               
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
        random_num = int.to_bytes(self.IV_num + block_index, self.block_size, "little")
        random_num = self.e_algo(random_num)
        random_num = int.from_bytes(random_num, "little")

        # xor the two numbers and convert it into a bytes object
        c_block = p_block ^ random_num #what to do if the number of bits of number is bigger than block size. 
        c_block = int.to_bytes(c_block, self.block_size, "little")
       
        return self.add_index_to_block(c_block, index)
   
    # decrypt a block
    def decrypt_block(self, block):
        index = int.from_bytes(block[:4], "little")

        random_num = int.to_bytes(self.IV_num + index, self.block_size, "little")
        random_num = self.e_algo(random_num)
        random_num = int.from_bytes(random_num, "little")

        c_block = int.from_bytes(block[4:], "little")
        
        p_block = c_block ^ random_num
        p_block = int.to_bytes(p_block, self.block_size, "little")
        self.result[index] = p_block 
        return p_block