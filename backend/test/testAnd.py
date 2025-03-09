import unittest

from ..core.parser import InstructionParser
from ..core.registers import Registers
from ..instructions.ALU.and_file import AND_Instruction
from ..core.memory import Memory
from ..instructions.instruction_set import instruction_set

class TestInstructionParser(unittest.TestCase):

    def setUp(self):
        self.memory_db = {
            "Instructions": ["AND X0, X1, X2"],
            "Queue": None,
            "current_instruction": -1,
            "registers": Registers(),
            "memory": Memory()
        }

    def test_parser_and_instruction(self):
        parser = InstructionParser(self.memory_db["Instructions"])
        self.memory_db["Queue"] = parser.return_queue()
        instruction = self.memory_db["Queue"].get()
        self.assertEqual(instruction.__class__.__name__, "AND_Instruction")
        self.assertEqual(instruction.destination, "X0")
        self.assertEqual(instruction.reg1, "X1")
        self.assertEqual(instruction.reg2_or_immediate, "X2")

    def test_execute_and_instruction(self):
        self.memory_db["registers"].set("X1", 5)
        self.memory_db["registers"].set("X2", 3)
        parser = InstructionParser(self.memory_db["Instructions"])
        self.memory_db["Queue"] = parser.return_queue()
        instruction = self.memory_db["Queue"].get()
        instruction.execute(self.memory_db["registers"], self.memory_db["memory"])
        self.assertEqual(self.memory_db["registers"].get("X0"), 1)
        
    def test_revert_and_instruction(self):
        self.memory_db["registers"].set("X1", 5)
        self.memory_db["registers"].set("X2", 3)
        parser = InstructionParser(self.memory_db["Instructions"])
        self.memory_db["Queue"] = parser.return_queue()
        instruction = self.memory_db["Queue"].get()
        instruction.execute(self.memory_db["registers"], self.memory_db["memory"])
        instruction.revert(self.memory_db["registers"])
        self.assertEqual(self.memory_db["registers"].get("X0"), 0)

if __name__ == '__main__':
    unittest.main()
