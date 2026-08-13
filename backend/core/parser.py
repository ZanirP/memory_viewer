from instructions.instruction_set import instruction_set



class InstructionParser:
    
    def __init__(self, instructions):
        if isinstance(instructions, str):
            instructions = instructions.splitlines()
            
        self.instructions = instructions
        self.instruction_memory = {}
        self.address_to_line = {}
        self.labels = {}
        self.current_address = 0

        for line_number, instruction in enumerate(instructions, start=1):
            cleaned = instruction.strip()
            if not cleaned or cleaned.startswith("#") or cleaned.startswith("//"):
                continue

            if ":" in cleaned:
                label, cleaned = cleaned.split(":", 1)
                label = label.strip()
                if not label:
                    raise ValueError("Label cannot be empty")
                if label in self.labels:
                    raise ValueError(f"Duplicate label: {label}")
                self.labels[label] = self.current_address
                cleaned = cleaned.strip()

            if cleaned:
                self.current_address += 4

        self.current_address = 0
        for line_number, instruction in enumerate(instructions, start=1):
            cleaned = instruction.strip()
            
            if not cleaned or cleaned.startswith("#") or cleaned.startswith("//"):
                continue

            if ":" in cleaned:
                _, cleaned = cleaned.split(":", 1)
                cleaned = cleaned.strip()
                if not cleaned:
                    continue
            
            try:
                parsed_instruction = self.parse(cleaned)
            except (TypeError, ValueError) as error:
                raise ValueError(f"Line {line_number}: {error}") from error
            if parsed_instruction.__class__.__name__ == "Branch_Instruction":
                if parsed_instruction.label not in self.labels:
                    raise ValueError(f"Undefined label: {parsed_instruction.label}")
                parsed_instruction.target_address = self.labels[parsed_instruction.label]
            self.instruction_memory[self.current_address] = parsed_instruction
            self.address_to_line[self.current_address] = line_number
            self.current_address += 4      
        
        
        
		
    def classify_instruction(self, instruction):
        instruction = instruction.strip().split(maxsplit=1)
        opcode = instruction[0].upper()
        operands = instruction[1] if len(instruction) > 1 else None
        
        if opcode in instruction_set:
            # fit operands to expected format
            # we could just strip the "," and "[, ]" chracters and then split
            if operands is None:
                raise ValueError(f"Missing operands for {opcode}")
            operands = operands.strip().replace(",", " ").replace("[", " ").replace("]", " ").replace("#", "").split()
            return opcode, operands
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        
    def parse(self, instruction):
        opcode, operands = self.classify_instruction(instruction)
        return instruction_set[opcode](*operands)
    
    def return_instruction_memory(self):
        return self.instruction_memory

    def return_labels(self):
        return self.labels

    def return_address_to_line(self):
        return self.address_to_line
        
        
