from queue import Queue
from instructions.instruction_set import instruction_set



class InstructionParser:
    
    def __init__(self, instructions):
        self.instructions = instructions
        self.queue = Queue()
        
        for instruction in instructions:
            self.queue.put(self.parse(instruction))
            
        
        
        
		
    def classify_instruction(self, instruction):
        instruction = instruction.strip().split(maxsplit=1)
        opcode = instruction[0]
        operands = instruction[1] if len(instruction) > 1 else None
        
        if opcode in instruction_set:
            # fit operands to expected format
            # we could just strip the "," and "[, ]" chracters and then split
            operands = operands.strip().replace(",", " ").replace("[", " ").replace("]", " ").replace("#", "").split()
            return opcode, operands
        else:
            return "Other", []
        
    def parse(self, instruction):
        opcode, operands = self.classify_instruction(instruction)
        return instruction_set[opcode](*operands)
    
    def return_queue(self):
        return self.queue
        
        
        