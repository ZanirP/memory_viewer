import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from instructions.instructions import Instruction
from core.registers import Registers, RegistersModel
from core.memory import Memory, MemoryModel
from core.parser import InstructionParser

app = FastAPI()
origins = [
	"http://localhost:3000"
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
    "current_instruction": -1,
    "registers": Registers(),
    "memory": Memory()
}


@app.post(path="/save")
def save_instruction(instructions: List[Instruction]):
    # TODO: Implement this function
    memory_db["Instructions"] = instructions
    memory_db["Queue"] = InstructionParser(instructions).return_queue()
    return {"message": "Save functionality not completed yet"}

@app.post(path="/run-next-line")
def run_next_line():
	memory_db["current_instruction"] += 1
	memory_db["Queue"].get().execute(memory_db["registers"], memory_db["memory"])
	return {"message": "Ran next line"}

@app.post(path="/revert")
def revert():
    # TODO: Implement this function
	return {"message": "Revert functionality not implemented yet"}

@app.post(path="/reset")
def reset():
    # TODO: Implement this function
	return {"message": "Reset functionality not implemented yet"}

@app.post(path="/run-all")
def run_all():
    # TODO: Implement this function
	return {"message": "Run all functionality not implemented yet"}

@app.get(path="/registers", response_model=RegistersModel)
def registers():
	return RegistersModel(registers=memory_db["registers"].registers)

@app.get(path="/memory", response_model=MemoryModel)
def memory():
	return MemoryModel(memory=memory_db["memory"].to_dict())



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)