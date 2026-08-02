import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

if os.getenv("ENV", "development") == "development":
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["http://localhost:3000"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)


memory_db = {
    
    "Instructions": [],
    "Instruction_Memory": None,
    "current_instruction": None,
    "registers": Registers(),
    "memory": Memory()
}


@app.post(path="/save", response_model=None)
def save_instruction(data: InstructionRequest):
    instructions = data.instructions
    print("DEBUG - Instructions: ", instructions)
    memory_db["Instructions"] = instructions
    memory_db["current_instruction"] = No_Instruction()
    memory_db["registers"] = Registers()
    memory_db["memory"] = Memory()
    memory_db["registers"].set("PC", 0)
    memory_db["Instruction_Memory"] = InstructionParser(instructions).return_instruction_memory()
    print("DEBUG - Instruction Memory: ", memory_db["Instruction_Memory"])

@app.post(path="/run-next-line", response_model=None)
def run_next_line():
    instruction = memory_db["current_instruction"]
    if instruction.isReverted == True:
        instruction.execute(memory_db["registers"], memory_db["memory"])
        memory_db["registers"]["PC"] += 4 # TODO: fix this when branching is implemented
        
    else:
        instruction =  memory_db["Instruction_Memory"].get(memory_db["registers"]["PC"], No_Instruction())
        memory_db["current_instruction"] = instruction
        instruction.execute(memory_db["registers"], memory_db["memory"])
        memory_db["registers"]["PC"] += 4 # TODO: fix this when branching is implemented

    changed_reg = getattr(instruction, 'destination', None)
    changed_mem = getattr(instruction, 'target_address', None)
    
    return {
        "message": "Executed next instruction",
        "changedRegister": changed_reg,
        "changedAddress": str(changed_mem) if changed_mem is not None else None
    }
    
    
        

@app.post(path="/revert", response_model=None)
def revert():
    instruction = memory_db["current_instruction"]
    pc = memory_db["registers"].get("PC")

    try:
        instruction.revert(memory_db["registers"], memory_db["memory"])
    except TypeError:
        instruction.revert(memory_db["registers"])

    memory_db["registers"].set("PC", max(0, pc - 4))  # TODO: fix this when branching is implemented
    
    changed_reg = getattr(instruction, 'destination', None)
    changed_mem = getattr(instruction, 'target_address', None)
    
    return {
        "message": "Reverted last instruction",
        "changedRegister": changed_reg,
        "changedAddress": str( changed_mem) if changed_mem is not None else None
    }

@app.post(path="/reset", response_model=None)
def reset():
	memory_db["Instructions"] = []
	memory_db["current_instruction"] = None
	memory_db["registers"] = Registers()
	memory_db["memory"] = Memory()
	memory_db["Instruction_Memory"] = None

@app.post(path="/run-all", response_model=None)
def run_all():
    memory_db["registers"]["PC"] = 0
    while memory_db["Instruction_Memory"] and len(memory_db["Instruction_Memory"]) > 0:
        memory_db["current_instruction"] = memory_db["Instruction_Memory"].get(
            memory_db["registers"]["PC"], No_Instruction())
        memory_db["current_instruction"].execute(memory_db["registers"], memory_db["memory"])
        memory_db["registers"]["PC"] += 4 # TODO: fix this when branching is implemented

@app.get(path="/registers", response_model=RegistersModel)
def registers():
	return RegistersModel(registers=memory_db["registers"].registers)

@app.get(path="/memory", response_model=MemoryModel)
def memory():
	return MemoryModel(memory=memory_db["memory"].to_dict())


FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Don't try to serve index.html if the request was meant for an API endpoint
    if full_path.startswith("api/") or full_path in ["registers", "memory", "save", "run-next-line", "revert"]:
        raise HTTPException(status_code=404, detail="API route not found")
        
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Run 'npm run build' inside /frontend first."}

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)