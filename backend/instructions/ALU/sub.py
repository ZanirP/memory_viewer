from ..instructions import Instruction

class SUB_Instruction(Instruction):
    
    def __init__(self, destination, reg1, reg2):
        self.destination = destination
        self.reg1 = reg1
        self.reg2 = reg2
        self.previous_value = None
        self.isReverted = False
        
    
    def execute(self, registers, memory):
        self.previous_value = registers.get(self.destination)
        registers.set(self.destination, registers.get(self.reg1) - registers.get(self.reg2))
        self.isReverted = False
        
    def revert(self, registers, memory):
        if self.previous_value is not None:
            registers.set(self.destination, self.previous_value)
            self.previous_value = None
            self.isReverted - True