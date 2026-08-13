from pydantic import BaseModel
from typing import Dict
from .cache import DirectMappedCache

class Memory:
    
    def __init__(self, size=4096, cache_lines=8, cache_block_size=8):
        self.memory = bytearray(size)
        self.cache = DirectMappedCache(cache_lines, cache_block_size)
    
    def load_double_word(self, address):
        ''' Load a 8-byte word from memory '''
        self._validate_double_word_address(address)
        value = self.peek_double_word(address)
        return self.cache.access(address, value, "load")

    def peek_double_word(self, address):
        """Read backing memory without representing a processor memory access."""
        self._validate_double_word_address(address)
        return int.from_bytes(self.memory[address:address+8], "little")
    
    def store_double_word(self, address, value):
        ''' Store a 8-byte word to memory'''
        self._validate_double_word_address(address)
        self.memory[address:address+8] = (value & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")
        self.cache.access(address, value & 0xFFFFFFFFFFFFFFFF, "store")

    def _validate_double_word_address(self, address):
        if not isinstance(address, int):
            raise ValueError("Memory address must be an integer")
        if address % 8 != 0:
            raise ValueError("Unaligned memory")
        if address < 0 or address + 8 > len(self.memory):
            raise ValueError(f"Memory address out of bounds: {address}")
        
    def to_dict(self):
        return {
            address: int.from_bytes(self.memory[address:address+8], "little")
                for address in range(0, len(self.memory), 8) 
                # if self.load_double_word(address) != 0
                }

class MemoryModel(BaseModel):
    memory: Dict[int, int]
