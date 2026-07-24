from ..instructions import Instruction

class MOV_Instruction(Instruction):
	
	def __init__(self, destination, immediate):
		self.destination = destination
		self.immediate = immediate
		self.previous_value = None
		self.isReverted = False
		
	def execute(self, registers, memory):
		self.isReverted = False
		self.previous_value = registers.get(self.destination)
		registers.set(self.destination, self.immediate)
		
	def revert(self, registers, memory):
		if self.previous_value is not None:
			registers.set(self.destination, self.previous_value)
			self.previous_value = None
			self.isReverted = True