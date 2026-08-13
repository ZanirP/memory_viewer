import pytest
from fastapi import HTTPException

import main
from core.memory import Memory
from core.parser import InstructionParser
from core.registers import Registers


def save(lines, session="test"):
    return main.save_instruction(main.InstructionRequest(instructions=lines), session)


def test_run_all_stops_at_end_of_program():
    save(["MOV X0, #1"])

    result = main.run_all("test")

    assert result["steps"] == 1
    assert main.get_machine("test")["registers"].get("X0") == 1
    assert result["pc"] == 4


def test_run_all_stops_infinite_branch_at_execution_limit(monkeypatch):
    monkeypatch.setattr(main, "MAX_RUN_ALL_STEPS", 5)
    save(["loop: B loop"])

    with pytest.raises(HTTPException, match="Execution limit") as error:
        main.run_all("test")

    assert error.value.status_code == 409


def test_mov_and_load_store_offsets_are_integers():
    parser = InstructionParser([
        "MOV X0, #42",
        "MOV X1, #8",
        "STR X0, [X1, #8]",
        "LDR X2, [X1, #8]",
    ])
    registers = Registers()
    memory = Memory()

    for address in range(0, 16, 4):
        instruction = parser.return_instruction_memory()[address]
        instruction.execute(registers, memory)

    assert registers.get("X0") == 42
    assert registers.get("X2") == 42
    assert memory.load_double_word(16) == 42


@pytest.mark.parametrize("address", [-8, 4096])
def test_memory_rejects_out_of_bounds_double_words(address):
    memory = Memory()

    with pytest.raises(ValueError, match="out of bounds"):
        memory.load_double_word(address)
    with pytest.raises(ValueError, match="out of bounds"):
        memory.store_double_word(address, 1)

    assert len(memory.memory) == 4096


def test_failed_save_preserves_existing_machine_state():
    save(["MOV X0, #7"])
    main.run_next_line("test")

    with pytest.raises(HTTPException) as error:
        save(["B missing"])

    machine = main.get_machine("test")
    assert error.value.status_code == 400
    assert machine["Instructions"] == ["MOV X0, #7"]
    assert machine["registers"].get("X0") == 7


def test_sessions_have_independent_program_and_register_state():
    save(["MOV X0, #1"], "session-a")
    save(["MOV X0, #2"], "session-b")
    main.run_next_line("session-a")

    assert main.get_machine("session-a")["registers"].get("X0") == 1
    assert main.get_machine("session-b")["registers"].get("X0") == 0


def test_branch_response_maps_pc_to_source_line():
    save(["B done", "", "MOV X0, #1", "done: MOV X0, #2"])

    result = main.run_next_line("test")

    assert result["pc"] == 8
    assert result["activeLine"] == 4
