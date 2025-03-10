import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from instructions.Other.noParse import No_Instruction
from core.registers import Registers, RegistersModel
from core.memory import Memory, MemoryModel
from core.parser import InstructionParser
from pydantic import BaseModel

app = FastAPI()

class InstructionRequest(BaseModel):
	instructions: List[str]

origins = [
	"http://localhost:3000",
	# put the actual website here
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

memory_db = {
    
    "Instructions": [],
    "Queue": None,
    "current_instruction": None,
    "registers": Registers(),
    "memory": Memory()
}


@app.post(path="/save", response_model=None)
def save_instruction(data: InstructionRequest):
    instructions = data.instructions
    print("DEBUG - Instructions: ", instructions)
    print("DEBUG - Instructions Type: ", type(instructions))
    memory_db["Instructions"] = instructions
    memory_db["current_instruction"] = No_Instruction()
    memory_db["registers"] = Registers()
    memory_db["memory"] = Memory()
    memory_db["Queue"] = InstructionParser(instructions).return_queue()

@app.post(path="/run-next-line", response_model=None)
def run_next_line():
    if memory_db["current_instruction"].isReverted == True:
        memory_db["current_instruction"].execute(memory_db["registers"], memory_db["memory"])
        return {"message": "Instruction Executed"}
    else:
        memory_db["current_instruction"] =  memory_db["Queue"].get()
        memory_db["current_instruction"].execute(memory_db["registers"], memory_db["memory"])
        return {"message": "Instruction Executed"}

@app.post(path="/revert", response_model=None)
def revert():
    memory_db["current_instruction"].revert(memory_db["registers"], memory_db["memory"])

@app.post(path="/reset", response_model=None)
def reset():
	memory_db["Instructions"] = []
	memory_db["current_instruction"] = None
	memory_db["registers"] = Registers()
	memory_db["memory"] = Memory()
	memory_db["Queue"] = None

@app.post(path="/run-all", response_model=None)
def run_all():
    while memory_db["Queue"].empty() == False:
        memory_db["current_instruction"] = memory_db["Queue"].get()
        memory_db["current_instruction"].execute(memory_db["registers"], memory_db["memory"])

@app.get(path="/registers", response_model=RegistersModel)
def registers():
	return RegistersModel(registers=memory_db["registers"].registers)

@app.get(path="/memory", response_model=MemoryModel)
def memory():
	return MemoryModel(memory=memory_db["memory"].to_dict())



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)