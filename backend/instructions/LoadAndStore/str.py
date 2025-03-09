from ..instructions import Instruction

class STR_Instruction(Instruction):
    
    def __init__(self, reg, base, offset=0):
        self.reg = reg
        self.base = base
        self.offset = offset
        self.previous_value = None
        
    
    def execute(self, registers, memory):
        value = registers.get(self.base)
        
        if base is None or not isinstance(base, int):
            raise ValueError("Invalid base register")
        
        address = value + self.offset
        
        self.previous_value = memory.load_double_word(address)
        
        value_store = registers.get(self.reg)
        memory.store_double_word(address, value_store)
        
    def revert(self, registers, memory):
        
        if self.previous_value is not None:
            address = registers.get(self.base) + self.offset
            memory.store_double_word(address, self.previous_value)
            self.previous_value = None
