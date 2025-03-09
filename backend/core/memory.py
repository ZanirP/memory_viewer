from pydantic import BaseModel
from typing import Dict

class Memory:
    
    def __init__(self, size=4096):
        self.memory = bytearray(size)
    
    def load_double_word(self, address):
        ''' Load a 8-byte word from memory '''
        if address % 8 != 0:
            raise ValueError("Unaligned memory")
        return int.from_bytes(self.memory[address:address+8], "little")
    
    def store_double_word(self, address, value):
        ''' Store a 8-byte word to memory'''
        self.memory[address:address+8] = value.to_bytes(8, "little")
        
    def to_dict(self):
        return {
            address: self.load_double_word(address) 
                for address in range(0, len(self.memory), 8) 
                # if self.load_double_word(address) != 0
                }

class MemoryModel(BaseModel):
    memory: Dict[int, int]
