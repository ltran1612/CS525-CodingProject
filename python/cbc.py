class CBC:
    # Constructor
    # IV: the initial IV
    # block_size: the number of bytes the block have
    # key: the key to the encryption and decryption algorithm
    # e_algo: the encryption algorithm function
    # d_algo: the decryption algorithm function
    def __init__(self, IV, block_size, key, e_algo, d_algo):
        self.blocks = []
        self.blocks_num = 0
        self.last_block = IV
        self.block_size = block_size
        self.key = key
        self.e_algo = e_algo
        self.d_algo = d_algo
        self.block_index = 0

    # Parse the message in to blocks
    def set_message(self, message):
        string_byte = bytes(message, "utf-8")
        block_of_0 = int.from_bytes(bytes(self.block_size), "little")
        temp = [string_byte[i:i + self.block_size] for i in range(0, len(string_byte), self.block_size)]
        blocks = temp

        # add padding, if needed
        for b in blocks:
            num = int.from_bytes(b, "little")
            block = num | block_of_0
            block = int.to_bytes(block, self.block_size, "little")
            self.blocks.append(block)
        print(len(self.blocks))
        self.blocks_num = len(self.blocks)
                               
    # get a block from the disk 
    def cbc_get_block(self):
        if self.block_index >= self.blocks_num:
            return None

        # set and increment the index
        index = self.block_index
        self.block_index = self.block_index + 1

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
       
        return c_block
        
   
    # decrypt a block
    def cbc_decrypt_block(self, block):
        index = self.block_index
        index = index + 1
        c_block = block
        p_block = int.from_bytes(self.d_algo(c_block), "little") ^ int.from_bytes(self.last_block, "little")
        self.last_block = c_block

        return int.to_bytes(p_block, self.block_size, "little")