from dataclasses import dataclass, field

from i8086.pylib.instruction import Instr


@dataclass
class Exe:
    data: list[int]
    end: int
    idx: int = 0
    instr: list[Instr] = field(default_factory=list)

    @property
    def byte(self):
        return self.data[self.idx]

    def consume_byte(self):
        byte = self.byte
        self.idx += 1
        return byte

    def append(self, instr):
        self.instr.append(instr)
