from ..instructions import Instruction

class EOR_Instruction(Instruction):
    
    def __init__(self, destination, reg1, reg2_or_immediate):
        
        self.destination = destination
        self.reg1 = reg1
        self.reg2_or_immediate = reg2_or_immediate
        self.is_immiedate = reg2_or_immediate.startswith("X") == False
        self.previous_value = None
        
    def execute(self, registers, memory):
        
        self.previous_value = registers.get(self.destination)
        
        if self.is_immiedate:
            result = registers.get(self.reg1) ^ int(self.reg2_or_immediate[1:])
        else:
            result = registers.get(self.reg1) ^ registers.get(self.reg2_or_immediate)
            
        registers.set(self.destination, result & 0xFFFFFFFFFFFFFFFF)
        
    def revert(self, registers):
        
        if self.previous_value is not None:
            registers.set(self.destination, self.previous_value)
            self.previous_value = None