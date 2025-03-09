# This file contains the implementation of the branch instruction
from ..instructions import Instruction
class Branch_Instruction(Instruction):
    
    def __init__(self, label):
        self.label = label
        
    def execute(self, registers, memory, labels, pc):
        if self.label in labels:
            pc[0] = labels[self.label]
        else:
            raise ValueError(f"Undefined label: {self.label}")
        
    
    def revert(self, pc, previous_pc):
        pc[0] = previous_pc
        
    