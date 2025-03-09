from ..instructions import Instruction

class Conditional_Branch_Instruction(Instruction):
    
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label
        
    def execute(self, registers, memory, labels, flags, pc):
        if self.condition(registers, flags):
            return labels[self.label]
        return pc[0] + 1
    
    def revert(self, pc, previous_pc):
        pc[0] = previous_pc