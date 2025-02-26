from dataclasses import dataclass

# Opcodes can spill into the 2nd Byte1 (bits 5-3). These are tables to handle this.
OPS2 = [
    " add or adc sbb and sub xor cmp ".split(),
    " test ? not neg mul imul div idiv ".split(),
    " mov ? ? ? ? ? ? ? ".split(),
    " pop ? ? ? ? ? ? ? ".split(),
    " rol ror rcl rcr sal shr ? sar ".split(),
    " inc dec call call jmp jmp push ? ".split(),
]
OP_MATH1 = 0
OP_MATH2 = 1
OP_MOVE = 2
OP_STACK = 3
OP_SHIFT = 4
OP_OTHER = 5


# Registers in the reg field
# Yea, the whole c follows a thing is odd to me too
REG = [
    " al cl dl bl ah ch dh bh ".split(),
    " ax cx dx bx sp bp si di ".split(),
    ["bx + si", "bx + di", "bp + si", "bp + di", "si", "di", "bp", "bx"],
    " es cs ss ds ? ? ? ? ".split(),
]

REG8 = 0
REG16 = 1
REG_EA = 2
REG_SEG = 3

AL = 0
AX = 0


@dataclass
class Reg:
    reg: int = None
    type_: int = None

    def format(self):
        return REG[self.type_][self.reg]

    def to_mnemonic(self):
        return REG[self.type_][self.reg]


@dataclass
class Mem:
    ea_reg: int = None
    disp: int = None
    size: int = None

    def format(self):
        addr = REG[REG_EA][self.ea_reg] if self.ea_reg is not None else ""
        if self.disp:
            addr += " " if addr else ""
            addr += f"+ {self.disp}"
        addr = addr.replace("[ -", "[-")
        addr = addr.removeprefix("+ ")
        addr = f"[{addr}]"
        addr = addr.replace("+ -", "- ")
        return addr


@dataclass
class Imm:
    data: int
    size: int

    def format(self):
        return str(self.data)


Dst = Reg | Mem
Src = Reg | Mem


@dataclass
class Instr:
    key: int  # Useful for debugging
    mnem: str = None
    dst: Dst = None
    src: Src = None
    imm: Imm = None

    def debug(self):
        print(hex(self.key), self)

    def format(self):
        # self.debug()
        out = ""

        if self.dst:
            out += self.dst.format()

        if self.src:
            out += ", " if out else ""
            out += self.src.format()

        if self.imm:
            out += ", " if out else ""
            if isinstance(self.dst, Mem):
                out += "byte " if self.imm.size == 1 else "word "
            out += self.imm.format()

        return f"{self.mnem} {out}".strip()
