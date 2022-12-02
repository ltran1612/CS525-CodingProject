class EncryptionMode:
     # Constructor
    # IV: the initial IV
    # block_size: the number of bytes the block have
    # key: the key to the encryption and decryption algorithm
    # e_algo: the encryption algorithm function
    # d_algo: the decryption algorithm function
    def __init__(self, IV, block_size, key, e_algo, d_algo, algo_block_size):
        if block_size % algo_block_size != 0:
            print("Block size must be a multiple of algo_block_size")
            return
        self.numbering_size = 4
        self.blocks = []
        self.blocks_num = 0
        self.block_size = block_size
        self.key = key
        self.e_algo = e_algo
        self.d_algo = d_algo
        self.result = {}
        self.algo_block_size = algo_block_size
        self.total_block_size = self.get_total_size(self.block_size)
        
    def get_size(self):
        return self.blocks_num
    
    def get_total_size(self, block_size):
        return self.numbering_size + block_size

    def get_decrypted_message(self):
        i = 0
        p_blocks = []
        while i in self.result:
            p_blocks.append(self.result[i].decode("utf-8"))
            i = i + 1
        
        return "".join(p_blocks)


    # Parse the message in to blocks
    def set_message(self, message):
        string_byte = bytes(message, "utf-8")
        
        temp = [string_byte[i:i + self.block_size] for i in range(0, len(string_byte), self.block_size)]
        blocks = temp
        block_of_0 = int.from_bytes(bytes(self.block_size), "little")
        for block in blocks:
            num_b = int.from_bytes(block, "little")
            block = num_b | block_of_0
            block = int.to_bytes(block, self.block_size, "little")
            #print("message block", block)
            self.blocks.append(block)
        
        self.blocks_num = len(self.blocks)

    def add_index_to_block(self, block, block_index):
        index = block_index
      
        final_block = bytearray()

        my_index = int.to_bytes(index, self.numbering_size, "little")

        for value in my_index:
            final_block.append(value)
        
        for value in block:
            final_block.append(value)
        
        final_block = bytes(final_block)
        return final_block