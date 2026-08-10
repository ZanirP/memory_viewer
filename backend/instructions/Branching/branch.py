# This file contains the implementation of the branch instruction
from ..instructions import Instruction
class Branch_Instruction(Instruction):
    
    def __init__(self, label):
        self.label = label
        self.target_address = None
        self.previous_pc = None
        self.isReverted = False
        self.updates_pc = True
        
    def execute(self, registers, memory):
        if self.target_address is None:
            raise ValueError(f"Undefined label: {self.label}")
        self.previous_pc = registers.get("PC")
        registers.set("PC", self.target_address)
        self.isReverted = False
        
    def revert(self, registers, memory):
        if self.previous_pc is not None:
            registers.set("PC", self.previous_pc)
            self.previous_pc = None
            self.isReverted = True
    
