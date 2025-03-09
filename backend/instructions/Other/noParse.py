from ..instructions import Instruction


class No_Instruction(Instruction):
    
	def __init__(self):
		print("NO INSTRUCTION FOUND")
	
	def execute(self, registers, memory):
		pass
	
	def revert(self, registers):
		pass