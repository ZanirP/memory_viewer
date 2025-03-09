from pydantic import BaseModel
from typing import Dict

class Registers:
    
    def __init__(self):
        self.registers = {f"X{i}": 0 for i in range(31)}
        self.registers["XZR"] = 0
        self.registers["SP"] = 0x7FFFFFFF
        self.registers["PC"] = 0
        
    def get(self, reg):
        return self.registers.get(reg, None)
        
    def set(self, reg, value):
        if reg in self.registers:
            self.registers[reg] = value
        else:
            raise ValueError(f"Invalid Registers: {reg}")
        
    def __repr__(self):
        return str(self.registers)


class RegistersModel(BaseModel):
    registers: Dict[str, int]