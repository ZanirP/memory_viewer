import pytest

from core.memory import Memory
from core.parser import InstructionParser
from core.registers import Registers
from instructions.Branching.branch import Branch_Instruction


def test_parser_records_labels_without_using_instruction_space():
    parser = InstructionParser([
        "start:",
        "ADD X0, X1, X2",
        "end: SUB X3, X4, X5",
    ])

    assert parser.return_labels() == {"start": 0, "end": 4}
    assert list(parser.return_instruction_memory()) == [0, 4]


def test_parser_resolves_forward_branch_label():
    parser = InstructionParser([
        "B done",
        "ADD X0, X1, X2",
        "done: SUB X3, X4, X5",
    ])

    branch = parser.return_instruction_memory()[0]
    assert isinstance(branch, Branch_Instruction)
    assert branch.label == "done"
    assert branch.target_address == 8


def test_branch_updates_and_reverts_pc():
    registers = Registers()
    branch = InstructionParser(["B target", "target: MOV X0, #1"]).return_instruction_memory()[0]

    branch.execute(registers, Memory())
    assert registers.get("PC") == 4

    branch.revert(registers, Memory())
    assert registers.get("PC") == 0


def test_parser_rejects_undefined_branch_label():
    with pytest.raises(ValueError, match="Undefined label: missing"):
        InstructionParser(["B missing"])
