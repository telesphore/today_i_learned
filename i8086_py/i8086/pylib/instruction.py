from collections.abc import Callable
from dataclasses import dataclass
from enum import EnumInt

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
    reg: int
    type_: int

    def to_mnemonic(self):
        return REG[self.type_][self.reg]


@dataclass
class EffAddr:
    ea_reg: int = None
    disp: int = None
    size: int = None


@dataclass
class Imm:
    data: int
    size: int


Dst = Reg | EffAddr
Src = Reg | EffAddr | Imm


@dataclass
class Instr:
    mnem: str = None
    act: Callable = None
    dst: Dst = None
    src: Src = None


def aaa():
    pass


def aad():
    pass


def aam():
    pass


def aas():
    pass


def adc():
    pass


def add():
    pass


def and_():
    pass


def call():
    pass


def cbw():
    pass


def clc():
    pass


def cld():
    pass


def cli():
    pass


def cmc():
    pass


def cmp():
    pass


def cmps():
    pass


def cs():
    pass


def cwd():
    pass


def daa():
    pass


def das():
    pass


def dec():
    pass


def div():
    pass


def ds():
    pass


def es():
    pass


def esc():
    pass


def hlt():
    pass


def idiv():
    pass


def imul():
    pass


def in_():
    pass


def inc():
    pass


def int_():
    pass


def into():
    pass


def iret():
    pass


def jb():
    pass


def jbe():
    pass


def jcxz():
    pass


def je():
    pass


def jl():
    pass


def jle():
    pass


def jmp():
    pass


def jnb():
    pass


def jnbe():
    pass


def jne():
    pass


def jnl():
    pass


def jnle():
    pass


def jno():
    pass


def jnp():
    pass


def jns():
    pass


def jo():
    pass


def jp():
    pass


def js():
    pass


def lahf():
    pass


def lds():
    pass


def lea():
    pass


def les():
    pass


def lock():
    pass


def lods():
    pass


def loop():
    pass


def loope():
    pass


def loopne():
    pass


def mov():
    pass


def movs():
    pass


def mul():
    pass


def neg():
    pass


def nop():
    pass


def not_():
    pass


def or_():
    pass


def out():
    pass


def pop():
    pass


def popf():
    pass


def push():
    pass


def pushf():
    pass


def rcl():
    pass


def rcr():
    pass


def rep():
    pass


def repne():
    pass


def ret():
    pass


def rol():
    pass


def ror():
    pass


def sahf():
    pass


def sal():
    pass


def sar():
    pass


def sbb():
    pass


def scas():
    pass


def shr():
    pass


def ss():
    pass


def stc():
    pass


def std():
    pass


def sti():
    pass


def stos():
    pass


def sub():
    pass


def test():
    pass


def wait():
    pass


def xchg():
    pass


def xlat():
    pass


def xor():
    pass


INSTR = {
    "aaa": Instr("aaa", act=aaa),
    "aad": Instr("aad", act=aad),
    "aam": Instr("aam", act=aam),
    "aas": Instr("aas", act=aas),
    "adc": Instr("adc", act=adc),
    "add": Instr("add", act=add),
    "and": Instr("and", act=and_),
    "call": Instr("call", act=call),
    "cbw": Instr("cbw", act=cbw),
    "clc": Instr("clc", act=clc),
    "cld": Instr("cld", act=cld),
    "cli": Instr("cli", act=cli),
    "cmc": Instr("cmc", act=cmc),
    "cmp": Instr("cmp", act=cmp),
    "cmps": Instr("cmps", act=cmps),
    "cs": Instr("cs", act=cs),
    "cwd": Instr("cwd", act=cwd),
    "daa": Instr("daa", act=daa),
    "das": Instr("das", act=das),
    "dec": Instr("dec", act=dec),
    "div": Instr("div", act=div),
    "ds": Instr("ds", act=ds),
    "es": Instr("es", act=es),
    "esc": Instr("esc", act=esc),
    "hlt": Instr("hlt", act=hlt),
    "idiv": Instr("idiv", act=idiv),
    "imul": Instr("imul", act=imul),
    "in": Instr("in", act=in_),
    "inc": Instr("inc", act=inc),
    "int": Instr("int", act=int_),
    "into": Instr("into", act=into),
    "iret": Instr("iret", act=iret),
    "jb": Instr("jb", act=jb),
    "jbe": Instr("jbe", act=jbe),
    "jcxz": Instr("jcxz", act=jcxz),
    "je": Instr("je", act=je),
    "jle": Instr("jle", act=jle),
    "jl": Instr("jl", act=jl),
    "jmp": Instr("jmp", act=jmp),
    "jnb": Instr("jnb", act=jnb),
    "jnbe": Instr("jnbe", act=jnbe),
    "jne": Instr("jne", act=jne),
    "jnle": Instr("jnle", act=jnle),
    "jnl": Instr("jnl", act=jnl),
    "jno": Instr("jno", act=jno),
    "jnp": Instr("jnp", act=jnp),
    "jns": Instr("jns", act=jns),
    "jo": Instr("jo", act=jo),
    "jp": Instr("jp", act=jp),
    "js": Instr("js", act=js),
    "lahf": Instr("lahf", act=lahf),
    "lds": Instr("lds", act=lds),
    "lea": Instr("lea", act=lea),
    "les": Instr("les", act=les),
    "lock": Instr("lock", act=lock),
    "lods": Instr("lods", act=lods),
    "loop": Instr("loop", act=loop),
    "loope": Instr("loope", act=loope),
    "loopne": Instr("loopne", act=loopne),
    "mov": Instr("mov", act=mov),
    "movs": Instr("movs", act=movs),
    "mul": Instr("mul", act=mul),
    "neg": Instr("neg", act=neg),
    "nop": Instr("nop", act=nop),
    "not": Instr("not", act=not_),
    "or": Instr("or", act=or_),
    "out": Instr("out", act=out),
    "pop": Instr("pop", act=pop),
    "popf": Instr("popf", act=popf),
    "push": Instr("push", act=push),
    "pushf": Instr("pushf", act=pushf),
    "rcl": Instr("rcl", act=rcl),
    "rcr": Instr("rcr", act=rcr),
    "rep": Instr("rep", act=rep),
    "repne": Instr("repne", act=repne),
    "ret": Instr("ret", act=ret),
    "rol": Instr("rol", act=rol),
    "ror": Instr("ror", act=ror),
    "sahf": Instr("sahf", act=sahf),
    "sal": Instr("sal", act=sal),
    "sar": Instr("sar", act=sar),
    "sbb": Instr("sbb", act=sbb),
    "scas": Instr("scas", act=scas),
    "shr": Instr("shr", act=shr),
    "ss": Instr("ss", act=ss),
    "stc": Instr("stc", act=stc),
    "std": Instr("std", act=std),
    "sti": Instr("sti", act=sti),
    "stos": Instr("stos", act=stos),
    "sub": Instr("sub", act=sub),
    "test": Instr("test", act=test),
    "wait": Instr("wait", act=wait),
    "xchg": Instr("xchg", act=xchg),
    "xlat": Instr("xlat", act=xlat),
    "xor": Instr("xor", act=xor),
}
