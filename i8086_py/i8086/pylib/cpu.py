from i8086.pylib.instruction import REG, REG16


class Cpu:
    def __init__(self, data, end):
        self.data: list[int] = data
        self.end: int = end

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

        self.mem: list[int] = [None] * 65536

    @property
    def byte(self):
        return self.data[self.ip]

    def consume_byte(self):
        byte = self.byte
        self.ip += 1
        return byte

    def display(self):
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
        for i, byte in enumerate(self.mem):
            if byte is not None:
                print(f"{i:04d} {byte:04x} ({byte})")
