import main
from core.memory import Memory
from core.registers import Registers
from instructions.LoadAndStore.ldr import LDR_Instruction
from instructions.LoadAndStore.str import STR_Instruction


def test_first_access_misses_and_repeated_access_hits():
    memory = Memory()

    memory.load_double_word(0)
    assert memory.cache.misses == 1
    assert memory.cache.last_access["result"] == "MISS"

    memory.load_double_word(0)
    assert memory.cache.hits == 1
    assert memory.cache.last_access["result"] == "HIT"


def test_conflicting_address_replaces_direct_mapped_line():
    memory = Memory(cache_lines=2, cache_block_size=8)
    memory.load_double_word(0)
    memory.load_double_word(16)

    line = memory.cache.lines[0]
    assert line["blockAddress"] == 16
    assert line["tag"] == 1
    assert memory.cache.misses == 2


def test_loads_and_stores_update_cache_data_and_statistics():
    registers = Registers()
    memory = Memory()
    registers.set("X0", 42)
    registers.set("X1", 8)

    STR_Instruction("X0", "X1").execute(registers, memory)
    assert memory.cache.last_access["operation"] == "store"
    assert memory.cache.lines[1]["data"] == 42

    LDR_Instruction("X2", "X1").execute(registers, memory)
    assert registers.get("X2") == 42
    assert memory.cache.last_access["result"] == "HIT"
    assert memory.cache.accesses == 2


def test_simulator_reset_clears_cache():
    session = "cache-reset-test"
    main.save_instruction(main.InstructionRequest(instructions=["LDR X0, [X1]"]), session)
    main.run_next_line(session)
    assert main.get_machine(session)["memory"].cache.accesses == 1

    main.reset(session)
    state = main.get_machine(session)["memory"].cache.to_dict()
    assert state["statistics"] == {"accesses": 0, "hits": 0, "misses": 0, "hitRate": 0.0}
    assert all(not line["valid"] for line in state["lines"])
