from abc import ABC, abstractmethod


class Instruction(ABC):
    """
    Abstract base class for all ARMv8 instructions.

    This class provides a blueprint for instruction parsing, classification, execution, 
    and reversion. Each specific instruction should implement its own parsing logic 
    and execution behavior.

    Methods:
        __init__(): Parses and classifies the instruction.
        execute(registers, memory): Executes the instruction using provided registers and memory.
        revert(): Reverts the instruction to undo its effects.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the instruction.

        This method is responsible for parsing the instruction and classifying it 
        into the appropriate instruction set. Subclasses should implement the 
        necessary parsing logic.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        self.isReverted = False
        return

    @abstractmethod
    def execute(self, registers, memory):
        """
        Executes the instruction.

        This method modifies the given registers and memory according to the 
        instruction's behavior.

        Args:
            registers (dict): A dictionary representing the CPU registers.
            memory (Memory): An object representing the system memory.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        return

    @abstractmethod
    def revert(self, registers, memory):
        """
        Reverts the instruction execution.

        This method is used to undo the effects of the instruction. 
        It allows for debugging, rollback mechanisms, or speculative execution.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        return
