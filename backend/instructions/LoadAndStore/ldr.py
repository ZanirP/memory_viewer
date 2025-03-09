from ..instructions import Instruction

class LDR_Instruction(Instruction):
    
    def __init__(self, destination, base, offset=0):
        self.destination = destination
        self.base = base
        self.offset = offset
        self.previous_value = None
        
    
    def execute(self, registers, memory):
        address = registers.get(self.base) + self.offset
        
        if address % 8 != 0:
            raise ValueError("Unaligned memory access")
        
        self.previous_value = registers.get(self.destination)        
        loaded_value = memory.load_double_word(address)
        registers.set(self.destination, loaded_value)
                
    def revert(self, registers):
        if self.previous_value is not None:
            registers.set(self.destination, self.previous_value)
            self.previous_value = None
