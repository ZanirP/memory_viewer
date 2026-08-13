from pydantic import BaseModel
from typing import Dict

class Registers:
    
    def __init__(self):
        self.registers = {f"X{i}": 0 for i in range(31)}
        self.registers["XZR"] = 0
        self.registers["SP"] = 0x7FFFFFFF
        self.registers["PC"] = 0
        
    def get(self, reg):
        if reg not in self.registers:
            raise ValueError(f"Invalid register: {reg}")
        return self.registers[reg]
        
    def set(self, reg, value):
        if reg not in self.registers:
            raise ValueError(f"Invalid register: {reg}")
        if not isinstance(value, int):
            raise ValueError(f"Register values must be integers: {reg}")
        if reg == "XZR":
            return
        self.registers[reg] = value if reg == "PC" else value & 0xFFFFFFFFFFFFFFFF
        
    def __repr__(self):
        return str(self.registers)


class RegistersModel(BaseModel):
    registers: Dict[str, int]
