class EncryptionMode:
     # Constructor
    # IV: the initial IV
    # block_size: the number of bytes the block have
    # key: the key to the encryption and decryption algorithm
    # e_algo: the encryption algorithm function
    # d_algo: the decryption algorithm function
    def __init__(self, IV, block_size, key, e_algo, d_algo):
        self.numbering_size = 4
        self.blocks = []
        self.blocks_num = 0
        self.block_size = block_size
        self.key = key
        self.e_algo = e_algo
        self.d_algo = d_algo
        self.usable_block_size = self.block_size - self.numbering_size

    def get_size(self):
        return self.blocks_num

    # Parse the message in to blocks
    def set_message(self, message):
        string_byte = bytes(message, "utf-8")
        
        temp = [string_byte[i:i + self.usable_block_size] for i in range(0, len(string_byte), self.usable_block_size)]
        blocks = temp
        block_of_0 = int.from_bytes(bytes(self.usable_block_size), "little")
        for block in blocks:
            num_b = int.from_bytes(block, "little")
            block = num_b | block_of_0
            block = int.to_bytes(block, self.usable_block_size, "little")
            print("message block", block)
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