import os
from threading import RLock
from typing import List

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.memory import Memory, MemoryModel
from core.parser import InstructionParser
from core.registers import Registers, RegistersModel


app = FastAPI()
MAX_RUN_ALL_STEPS = 10_000


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


def new_machine():
    return {
        "Instructions": [],
        "Instruction_Memory": {},
        "Address_To_Line": {},
        "current_instruction": None,
        "history": [],
        "registers": Registers(),
        "memory": Memory(),
        "lock": RLock(),
    }


sessions = {}
# Kept as a compatibility alias for existing direct callers and tests.
memory_db = new_machine()
sessions["default"] = memory_db


def get_machine(session_id):
    key = session_id if isinstance(session_id, str) and session_id else "default"
    if key not in sessions:
        sessions[key] = new_machine()
    return sessions[key]


def current_position(machine):
    pc = machine["registers"].get("PC")
    return pc, machine["Address_To_Line"].get(pc)


def execute_one(machine):
    pc = machine["registers"].get("PC")
    instruction = machine["Instruction_Memory"].get(pc)
    if instruction is None:
        return None

    register_snapshot = machine["registers"].registers.copy()
    memory_snapshot = machine["memory"].memory[:]
    cache_snapshot = machine["memory"].cache.snapshot()
    machine["current_instruction"] = instruction
    instruction.execute(machine["registers"], machine["memory"])
    if not getattr(instruction, "updates_pc", False):
        machine["registers"].set("PC", pc + 4)
    changed_register = "PC" if getattr(instruction, "updates_pc", False) else getattr(instruction, "destination", None)
    changed_address = getattr(instruction, "target_address", None) if getattr(instruction, "writes_memory", False) else None
    machine["history"].append({
        "instruction": instruction,
        "registers": register_snapshot,
        "memory": memory_snapshot,
        "cache": cache_snapshot,
        "changedRegister": changed_register,
        "changedAddress": changed_address,
    })
    return instruction


@app.post("/save")
def save_instruction(data: InstructionRequest, x_session_id: str = Header(default="default")):
    try:
        parser = InstructionParser(data.instructions)
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    machine = get_machine(x_session_id)
    with machine["lock"]:
        machine["Instructions"] = list(data.instructions)
        machine["Instruction_Memory"] = parser.return_instruction_memory()
        machine["Address_To_Line"] = parser.return_address_to_line()
        machine["current_instruction"] = None
        machine["history"] = []
        machine["registers"] = Registers()
        machine["memory"] = Memory()
    return {"message": "Instructions saved", "pc": 0, "activeLine": current_position(machine)[1]}


@app.post("/run-next-line")
def run_next_line(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        if not machine["Instruction_Memory"]:
            raise HTTPException(status_code=409, detail="No program has been saved")
        try:
            instruction = execute_one(machine)
        except (TypeError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        if instruction is None:
            pc, active_line = current_position(machine)
            return {
                "message": "Program complete", "executed": False, "complete": True,
                "pc": pc, "activeLine": active_line, "canRevert": bool(machine["history"]),
            }

        pc, active_line = current_position(machine)
        history_entry = machine["history"][-1]
        return {
            "message": "Executed next instruction",
            "executed": True,
            "complete": active_line is None,
            "pc": pc,
            "activeLine": active_line,
            "canRevert": True,
            "changedRegister": history_entry["changedRegister"],
            "changedAddress": str(history_entry["changedAddress"]) if history_entry["changedAddress"] is not None else None,
        }


@app.post("/revert")
def revert(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        if not machine["history"]:
            raise HTTPException(status_code=409, detail="No instruction is available to revert")
        history_entry = machine["history"].pop()
        machine["registers"].registers = history_entry["registers"]
        machine["memory"].memory = history_entry["memory"]
        machine["memory"].cache.restore(history_entry["cache"])
        machine["current_instruction"] = machine["history"][-1]["instruction"] if machine["history"] else None
        reverted_pc, active_line = current_position(machine)
        return {
            "message": "Reverted last instruction",
            "pc": reverted_pc,
            "activeLine": active_line,
            "canRevert": bool(machine["history"]),
            "changedRegister": history_entry["changedRegister"],
            "changedAddress": str(history_entry["changedAddress"]) if history_entry["changedAddress"] is not None else None,
        }


@app.post("/reset")
def reset(x_session_id: str = Header(default="default")):
    key = x_session_id if isinstance(x_session_id, str) and x_session_id else "default"
    sessions[key] = new_machine()
    if key == "default":
        global memory_db
        memory_db = sessions[key]
    return {"message": "Simulator reset", "pc": 0, "activeLine": None}


@app.post("/run-all")
def run_all(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        if not machine["Instruction_Memory"]:
            raise HTTPException(status_code=409, detail="No program has been saved")
        steps = 0
        try:
            while machine["registers"].get("PC") in machine["Instruction_Memory"]:
                if steps >= MAX_RUN_ALL_STEPS:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Execution limit of {MAX_RUN_ALL_STEPS} instructions exceeded",
                    )
                execute_one(machine)
                steps += 1
        except (TypeError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        pc, active_line = current_position(machine)
        return {
            "message": "Program complete", "complete": True, "steps": steps, "pc": pc,
            "activeLine": active_line, "canRevert": bool(machine["history"]),
        }


@app.get("/program")
def program(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        pc, active_line = current_position(machine)
        return {
            "instructions": machine["Instructions"],
            "pc": pc,
            "activeLine": active_line,
            "canRevert": bool(machine["history"]),
        }


@app.get("/registers", response_model=RegistersModel)
def registers(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        return RegistersModel(registers=machine["registers"].registers)


@app.get("/memory", response_model=MemoryModel)
def memory(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        return MemoryModel(memory=machine["memory"].to_dict())


@app.get("/cache")
def cache(x_session_id: str = Header(default="default")):
    machine = get_machine(x_session_id)
    with machine["lock"]:
        return machine["memory"].cache.to_dict()


FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
FRONTEND_ASSETS = os.path.join(FRONTEND_DIST, "assets")
if os.path.isdir(FRONTEND_ASSETS):
    app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS), name="assets")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    api_paths = {"registers", "memory", "cache", "program", "save", "run-next-line", "revert", "reset", "run-all"}
    if full_path.startswith("api/") or full_path in api_paths:
        raise HTTPException(status_code=404, detail="API route not found")
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Run 'npm run build' inside /frontend first."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
