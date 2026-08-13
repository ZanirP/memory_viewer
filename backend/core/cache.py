from copy import deepcopy


class DirectMappedCache:
    """Small write-through, write-allocate cache for simulator data accesses."""

    def __init__(self, line_count=8, block_size=8):
        if line_count <= 0 or block_size <= 0:
            raise ValueError("Cache dimensions must be positive")
        self.line_count = line_count
        self.block_size = block_size
        self.reset()

    def reset(self):
        self.lines = [
            {"index": index, "valid": False, "tag": None, "blockAddress": None, "data": None}
            for index in range(self.line_count)
        ]
        self.accesses = 0
        self.hits = 0
        self.misses = 0
        self.last_access = None

    def access(self, address, value, operation):
        block_address = address - (address % self.block_size)
        block_number = block_address // self.block_size
        index = block_number % self.line_count
        tag = block_number // self.line_count
        line = self.lines[index]
        hit = line["valid"] and line["tag"] == tag

        self.accesses += 1
        if hit:
            self.hits += 1
        else:
            self.misses += 1

        # Stores are write-through and both loads and stores allocate on a miss.
        if not hit or operation == "store":
            line.update(valid=True, tag=tag, blockAddress=block_address, data=value)

        self.last_access = {
            "address": address,
            "blockAddress": block_address,
            "lineIndex": index,
            "operation": operation,
            "result": "HIT" if hit else "MISS",
        }
        return line["data"]

    def snapshot(self):
        return deepcopy({
            "lines": self.lines,
            "accesses": self.accesses,
            "hits": self.hits,
            "misses": self.misses,
            "last_access": self.last_access,
        })

    def restore(self, state):
        restored = deepcopy(state)
        self.lines = restored["lines"]
        self.accesses = restored["accesses"]
        self.hits = restored["hits"]
        self.misses = restored["misses"]
        self.last_access = restored["last_access"]

    def to_dict(self):
        hit_rate = self.hits / self.accesses if self.accesses else 0.0
        return {
            "configuration": {"mapping": "direct", "lineCount": self.line_count, "blockSize": self.block_size},
            "lines": deepcopy(self.lines),
            "statistics": {
                "accesses": self.accesses,
                "hits": self.hits,
                "misses": self.misses,
                "hitRate": hit_rate,
            },
            "lastAccess": deepcopy(self.last_access),
        }
