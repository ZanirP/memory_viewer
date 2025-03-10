from ..instructions import Instruction

class LSL_Instruction(Instruction):
    
    def __init__(self, destination, reg, shift_amount):
        
        self.destination = destination
        self.reg = reg
        self.shift_amount = int(shift_amount)
        self.previous_value = None
        self.isReverted = False
        
    def execute(self, registers, memory):
        
        self.previous_value = registers.get(self.destination)
        result = registers.get(self.reg) << self.shift_amount
        registers.set(self.destination, result & 0xFFFFFFFFFFFFFFFF)
        self.isReverted = False
        
    def revert(self, registers, memory):
        
        if self.previous_value is not None:
            registers.set(self.destination, self.previous_value)
            self.previous_value = None
            self.isReverted = True

