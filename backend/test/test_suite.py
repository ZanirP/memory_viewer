"""Compatibility smoke tests for the current parser API.

The original suite imported obsolete queue- and byte-memory-based tests. Current
behavior is covered by the pytest regression modules in this directory.
"""

from core.parser import InstructionParser


def test_parser_exposes_instruction_memory():
    parser = InstructionParser(["MOV X0, #1"])

    assert list(parser.return_instruction_memory()) == [0]
