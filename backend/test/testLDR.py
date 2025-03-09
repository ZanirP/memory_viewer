import unittest

from ..core.parser import InstructionParser
from ..core.registers import Registers
from ..instructions.LoadAndStore.ldr import LDR_Instruction
from ..core.memory import Memory
from ..instructions.instruction_set import instruction_set

class TestInstructionParser(unittest.TestCase):

    def setUp(self):
        self.memory_db = {
            "Instructions": ["LDR X0, [X1, #4]"],
            "Queue": None,
            "current_instruction": -1,
            "registers": Registers(),
            "memory": Memory()
        }

    def test_parser_ldr_instruction(self):
        parser = InstructionParser(self.memory_db["Instructions"])
        self.memory_db["Queue"] = parser.return_queue()
        instruction = self.memory_db["Queue"].get()
        self.assertEqual(instruction.__class__.__name__, "LDR_Instruction")
        self.assertEqual(instruction.destination, "X0")
        self.assertEqual(instruction.base_reg, "X1")
        self.assertEqual(instruction.offset, 4)

    def test_execute_ldr_instruction(self):
        self.memory_db["registers"].set("X1", 0)
        self.memory_db["memory"].set(4, 42)
        parser = InstructionParser(self.memory_db["Instructions"])
        self.memory_db["Queue"] = parser.return_queue()
        instruction = self.memory_db["Queue"].get()
        instruction.execute(self.memory_db["registers"], self.memory_db["memory"])
        self.assertEqual(self.memory_db["registers"].get("X0"), 42)
        
    def test_revert_ldr_instruction(self):
        self.memory_db["registers"].set("X1", 0)
        self.memory_db["memory"].set(4, 42)
        parser = InstructionParser(self.memory_db["Instructions"])
        self.memory_db["Queue"] = parser.return_queue()
        instruction = self.memory_db["Queue"].get()
        instruction.execute(self.memory_db["registers"], self.memory_db["memory"])
        instruction.revert(self.memory_db["registers"])
        self.assertEqual(self.memory_db["registers"].get("X0"), 0)

if __name__ == '__main__':
    unittest.main()
