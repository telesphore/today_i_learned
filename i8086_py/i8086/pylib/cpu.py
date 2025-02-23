import i8086.pylib.instruction as inst


class Cpu:
    def __init__(self):
        self.reg: list[int] = [
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg 8
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg16
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg_ea
            [0, 0, 0, 0, 0, 0, 0, 0],  # reg_seg
        ]

    def output(self):
        for reg in range(8):
            print(f"{inst.REG[inst.REG16][reg]} = {self.reg[inst.REG16][reg]}")
