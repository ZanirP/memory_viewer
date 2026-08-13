import pytest
from fastapi import HTTPException

import main
from core.parser import InstructionParser
from core.registers import Registers


def save(lines, session="remaining"):
    return main.save_instruction(main.InstructionRequest(instructions=lines), session)


def test_unknown_and_malformed_instructions_report_source_line():
    with pytest.raises(ValueError, match=r"Line 2: Unknown opcode: BOGUS"):
        InstructionParser(["MOV X0, #1", "BOGUS X0"])
    with pytest.raises(ValueError, match=r"Line 1: Missing operands for ADD"):
        InstructionParser(["ADD"])


def test_registers_wrap_to_64_bits_and_xzr_is_immutable():
    registers = Registers()
    registers.set("X0", -1)
    registers.set("XZR", 12)

    assert registers.get("X0") == 0xFFFFFFFFFFFFFFFF
    assert registers.get("XZR") == 0


def test_add_and_sub_use_64_bit_register_semantics():
    registers = Registers()
    registers.set("X1", 0xFFFFFFFFFFFFFFFF)
    registers.set("X2", 1)
    instructions = InstructionParser(["ADD X0, X1, X2", "SUB X3, X2, X1"]).return_instruction_memory()

    instructions[0].execute(registers, main.Memory())
    instructions[4].execute(registers, main.Memory())

    assert registers.get("X0") == 0
    assert registers.get("X3") == 2


def test_logical_immediates_accept_decimal_and_hex():
    save(["MOV X1, #15", "EOR X0, X1, #5", "AND X2, X1, #0x3", "ORR X3, X0, #0x10"])
    result = main.run_all("remaining")
    registers = main.get_machine("remaining")["registers"]

    assert result["steps"] == 4
    assert registers.get("X0") == 10
    assert registers.get("X2") == 3
    assert registers.get("X3") == 26


def test_revert_uses_multi_step_execution_history():
    save(["MOV X0, #1", "MOV X1, #2", "ADD X2, X0, X1"])
    main.run_all("remaining")

    first = main.revert("remaining")
    second = main.revert("remaining")
    third = main.revert("remaining")
    registers = main.get_machine("remaining")["registers"]

    assert first["canRevert"] is True
    assert second["canRevert"] is True
    assert third["canRevert"] is False
    assert registers.get("X0") == 0
    assert registers.get("X1") == 0
    assert registers.get("X2") == 0
    assert registers.get("PC") == 0
    with pytest.raises(HTTPException) as error:
        main.revert("remaining")
    assert error.value.status_code == 409


def test_change_metadata_only_marks_written_state():
    save(["MOV X0, #7", "MOV X1, #8", "STR X0, [X1]", "LDR X2, [X1]", "B done", "done: MOV X3, #1"])

    mov = main.run_next_line("remaining")
    main.run_next_line("remaining")
    store = main.run_next_line("remaining")
    load = main.run_next_line("remaining")
    branch = main.run_next_line("remaining")

    assert mov["changedRegister"] == "X0" and mov["changedAddress"] is None
    assert store["changedRegister"] is None and store["changedAddress"] == "8"
    assert load["changedRegister"] == "X2" and load["changedAddress"] is None
    assert branch["changedRegister"] == "PC" and branch["changedAddress"] is None


def test_program_and_reset_contracts_are_synchronized():
    save(["MOV X0, #4"], "program-session")
    main.run_next_line("program-session")
    loaded = main.program("program-session")

    assert loaded["instructions"] == ["MOV X0, #4"]
    assert loaded["pc"] == 4
    assert loaded["canRevert"] is True

    main.reset("program-session")
    cleared = main.program("program-session")
    assert cleared["instructions"] == []
    assert cleared["pc"] == 0
    assert cleared["canRevert"] is False
