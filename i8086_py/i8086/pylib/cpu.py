import array
from pathlib import Path

from i8086.pylib.instruction import REG, REG16


class Cpu:
    def __init__(self, prog):
        self.end: int = len(prog)

        self.reg: list[list[int]] = [
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg8
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg16
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg_ea
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg_seg
        ]

        self.ip: int = 0

        self.zf: int = 0
        self.sf: int = 0
        self.pf: int = 0

        self.mem: list[int] = [0] * 65536
        self.mem[0 : self.end] = prog

    @property
    def byte(self):
        return self.mem[self.ip]

    def consume_byte(self):
        byte = self.byte
        self.ip += 1
        return byte

    def display(self, start=0, end=None):
        for reg in range(8):
            val = self.reg[REG16][reg]
            hx = f"0x{val:04x}".replace("-", "")
            print(f"{REG[REG16][reg]} = {hx} ({val})")
        hx = f"0x{self.ip:04x}"
        print(f"ip = {hx} ({self.ip})")
        print()
        print(f"zf = {self.zf}")
        print(f"sf = {self.sf}")
        print(f"pf = {self.pf}")
        print()
        print("memory")
        end = end if end else start + 16
        for i, byte in enumerate(self.mem[start:end]):
            print(f"{i:04d} {byte:04x} ({byte})")

    def dump(self, path: Path):
        bytes_ = array.array("B", [b & 0xFF for b in self.mem])
        with path.open("wb") as f:
            bytes_.tofile(f)
