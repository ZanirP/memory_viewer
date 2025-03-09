# keeping track of what's been created, plus will be useful later on
from .ALU.add import ADD_Instruction
from .ALU.and_file import AND_Instruction
from .ALU.eor import EOR_Instruction
from .ALU.LSL import LSL_Instruction
from .ALU.LSR import LSR_Instruction
from .ALU.mul import MUL_Instruction
from .ALU.orr import ORR_Instruction
from .ALU.sub import SUB_Instruction
from .LoadAndStore.ldr import LDR_Instruction
from .LoadAndStore.str import STR_Instruction
from .Other.noParse import No_Instruction


instruction_set = {
    # ALU operations
	"ADD" : ADD_Instruction,
	"AND" : AND_Instruction,
	"EOR" : EOR_Instruction,
	"LSL" : LSL_Instruction,
	"LSR" : LSR_Instruction,
	"MUL" : MUL_Instruction,
	"ORR" : ORR_Instruction,
    "SUB" : SUB_Instruction,
    
    # Load and Store operations
    "LDR" : LDR_Instruction,
    "STR" : STR_Instruction,
    
    # Branching operations
    
    
    
    "Other" : No_Instruction
    
}

instruction_format = {
	ADD_Instruction: "Rd,Rn,Rm",
	AND_Instruction: "Rd,Rn,Rm",
	EOR_Instruction: "Rd,Rn,Rm",
	LSL_Instruction: "Rd,Rn,Rm",
	LSR_Instruction: "Rd,Rn,Rm",
	MUL_Instruction: "Rd,Rn,Rm",
	ORR_Instruction: "Rd,Rn,Rm",
	SUB_Instruction: "Rd,Rn,Rm",
 
    LDR_Instruction: "Rd, [Rn, #offset]",
	STR_Instruction: "Rd, [Rn, #offset]",
	
	
	No_Instruction: "No instruction"
}