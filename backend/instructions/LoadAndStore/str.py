from ..instructions import Instruction

class STR_Instruction(Instruction):
    
    def __init__(self, reg, base, offset=0):
        self.reg = reg
        self.base = base
        self.offset = offset
        self.previous_value = None
        self.isReverted = False
        self.destination = None
        self.target_address = None
        
    
    def execute(self, registers, memory):
        value = registers.get(self.base)
        address = value + self.offset
        self.target_address = address
        
        if value is None or not isinstance(value, int):
            raise ValueError("Invalid base register ", self.base)
        if address % 8 != 0:
            raise ValueError("Unaligned memory access")        
        
        self.previous_value = memory.load_double_word(address)
        value_store = registers.get(self.reg)
        if value_store is None or not isinstance(value_store, int):
            raise ValueError("Invalid source register ", value_store)
        memory.store_double_word(address, value_store)
        self.isReverted = False
        
    def revert(self, registers, memory):
        
        if self.previous_value is not None:
            address = registers.get(self.base) + self.offset
            memory.store_double_word(address, self.previous_value)
            self.previous_value = None
            self.isReverted = True
