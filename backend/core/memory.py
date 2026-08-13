from pydantic import BaseModel
from typing import Dict

class Memory:
    
    def __init__(self, size=4096):
        self.memory = bytearray(size)
    
    def load_double_word(self, address):
        ''' Load a 8-byte word from memory '''
        self._validate_double_word_address(address)
        return int.from_bytes(self.memory[address:address+8], "little")
    
    def store_double_word(self, address, value):
        ''' Store a 8-byte word to memory'''
        self._validate_double_word_address(address)
        self.memory[address:address+8] = (value & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")

    def _validate_double_word_address(self, address):
        if not isinstance(address, int):
            raise ValueError("Memory address must be an integer")
        if address % 8 != 0:
            raise ValueError("Unaligned memory")
        if address < 0 or address + 8 > len(self.memory):
            raise ValueError(f"Memory address out of bounds: {address}")
        
    def to_dict(self):
        return {
            address: self.load_double_word(address) 
                for address in range(0, len(self.memory), 8) 
                # if self.load_double_word(address) != 0
                }

class MemoryModel(BaseModel):
    memory: Dict[int, int]
