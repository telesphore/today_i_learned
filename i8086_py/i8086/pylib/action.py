from dataclasses import dataclass

from i8086.pylib.cpu import Cpu
from i8086.pylib.instruction import AX, REG16, Instr, Mem, Reg

BX = 3
BP = 5
SI = 6
DI = 7


# ###########################################################################
def src_val(cpu: Cpu, instr: Instr) -> int:
    if isinstance(instr.src, Reg):
        val = cpu.reg[instr.src.type_][instr.src.reg]

    elif isinstance(instr.src, Mem):
        off = eff_addr(cpu, instr.src)

        if instr.src.size == 1:
            val = cpu.mem[off] & 0xFF
        else:
            byte1 = cpu.mem[off] & 0xFF
            byte2 = cpu.mem[off + 1] & 0xFF
            val = (byte2 << 8) | byte1

    elif instr.imm:
        val = instr.imm.data

    return val & 0xFFFF


def eff_addr(cpu: Cpu, arg: Mem) -> int:
    off = 0

    if arg.ea_reg is not None:
        match arg.ea_reg:
            case 0:
                off += cpu.reg[REG16][BX] + cpu.reg[REG16][SI]
            case 1:
                off += cpu.reg[REG16][BX] + cpu.reg[REG16][DI]
            case 2:
                off += cpu.reg[REG16][BP] + cpu.reg[REG16][SI]
            case 3:
                off += cpu.reg[REG16][BP] + cpu.reg[REG16][DI]
            case 4:
                off += cpu.reg[REG16][SI]
            case 5:
                off += cpu.reg[REG16][DI]
            case 6:
                off += cpu.reg[REG16][BP]
            case 7:
                off += cpu.reg[REG16][BX]
    off += arg.disp if arg.disp is not None else 0

    return off


def dst_val(cpu: Cpu, instr: Instr) -> int:
    if isinstance(instr.dst, Reg):
        val = cpu.reg[instr.dst.type_][instr.dst.reg]

    elif isinstance(instr.dst, Mem):
        off = eff_addr(cpu, instr.dst)
        val = cpu.mem[off]

    return val & 0xFFFF


def set_dst(cpu: Cpu, instr: Instr, val: int, *, flags: bool = True):
    if flags:
        set_flags(cpu, val)

    if isinstance(instr.dst, Reg):
        cpu.reg[instr.dst.type_][instr.dst.reg] = val & 0xFFFF

    elif isinstance(instr.dst, Mem):
        off = eff_addr(cpu, instr.dst)
        if instr.dst.size == 1:
            cpu.mem[off] = val
        else:
            cpu.mem[off] = val & 0x_00_FF
            cpu.mem[off + 1] = (val & 0x_FF_00) >> 8


def set_flags(cpu: Cpu, val: int):
    cpu.zf = int(val == 0)
    cpu.sf = 1 if val & 0b_1000_0000_0000_0000 else 0
    cpu.pf = 1 if bin(val & 0x_FF).count("1") % 2 == 0 else 0


# ###########################################################################
EA_CYCLES = [
    # [6, 6, 6, 6, 6, 6, 6, 6],  # Displacement only
    [12, 12, 11, 11, 9, 9, 9, 9],  # Displacement and register
    [8, 8, 7, 7, 5, 5, 5, 5],  # Register only
]


def eff_addr_cycles(arg: Mem) -> int:
    tics = 0

    if arg.disp and not arg.ea_reg:
        tics = 6

    elif arg.disp and arg.ea_reg:
        tics = EA_CYCLES[0][arg.ea_reg]

    elif not arg.disp and arg.ea_reg:
        tics = EA_CYCLES[1][arg.ea_reg]

    return tics


@dataclass
class Cycles:
    reg_reg: int = None
    reg_mem: int = None
    mem_reg: int = None
    reg_imm: int = None
    mem_imm: int = None
    acc_imm: int = None
    acc_mem: int = None
    mem_acc: int = None


def calc_cycles(instr: Instr, cycles: Cycles):
    tics = 0

    if isinstance(instr.dst, Reg) and instr.dst.reg == AX and instr.imm:
        tics = cycles.acc_imm

    elif isinstance(instr.dst, Reg) and instr.dst == AX and isinstance(instr.src, Mem):
        tics = cycles.acc_mem + eff_addr_cycles(instr.src)

    elif isinstance(instr.dst, Mem) and isinstance(instr.src, Reg) and instr.src == AX:
        tics = cycles.mem_acc + eff_addr_cycles(instr.dst)

    elif isinstance(instr.dst, Reg) and isinstance(instr.src, Reg):
        tics = cycles.reg_reg

    elif isinstance(instr.dst, Reg) and isinstance(instr.src, Mem):
        tics = cycles.reg_mem + eff_addr_cycles(instr.src)

    elif isinstance(instr.dst, Mem) and isinstance(instr.src, Reg):
        tics = cycles.mem_reg + eff_addr_cycles(instr.dst)

    elif isinstance(instr.dst, Reg) and instr.imm:
        tics = cycles.reg_imm

    elif isinstance(instr.dst, Mem) and instr.imm:
        tics = cycles.mem_imm + eff_addr_cycles(instr.dst)

    return tics


# ###########################################################################
def add(cpu: Cpu, instr: Instr):
    src = src_val(cpu, instr)
    dst = dst_val(cpu, instr)
    dst += src
    set_dst(cpu, instr, dst)
    cycles = Cycles(reg_reg=3, reg_mem=9, mem_reg=16, reg_imm=4, mem_imm=17, acc_imm=4)
    print(f"\tadd cycles = {calc_cycles(instr, cycles)}")


def cmp(cpu: Cpu, instr: Instr):
    src = src_val(cpu, instr)
    dst = dst_val(cpu, instr)
    dst -= src
    set_flags(cpu, dst)
    cycles = Cycles(reg_reg=3, reg_mem=9, mem_reg=9, reg_imm=4, mem_imm=10, acc_imm=4)
    print(f"\t\tcmp cycles = {calc_cycles(instr, cycles)}")


def je(cpu: Cpu, instr: Instr):
    if cpu.zf:
        cpu.ip += instr.src.disp


def jne(cpu: Cpu, instr: Instr):
    if not cpu.zf:
        cpu.ip += instr.src.disp


def jnz(cpu: Cpu, instr: Instr):
    if not cpu.zf:
        cpu.ip += instr.src.disp


def jz(cpu: Cpu, instr: Instr):
    if cpu.zf:
        cpu.ip += instr.src.disp


def mov(cpu: Cpu, instr: Instr):
    val = src_val(cpu, instr)
    set_dst(cpu, instr, val, flags=False)
    cycles = Cycles(
        mem_acc=10, acc_mem=10, reg_reg=2, reg_mem=8, mem_reg=9, reg_imm=4, mem_imm=10
    )
    print(f"\t\tmov cycles = {calc_cycles(instr, cycles)}")


def sub(cpu: Cpu, instr: Instr):
    src = src_val(cpu, instr)
    dst = dst_val(cpu, instr)
    dst -= src
    set_dst(cpu, instr, dst)
    cycles = Cycles(reg_reg=3, reg_mem=9, mem_reg=16, reg_imm=4, mem_imm=17, acc_imm=4)
    print(f"\t\tsub cycles = {calc_cycles(instr, cycles)}")


# ###########################################################################
def aaa(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def aad(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def aam(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def aas(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def adc(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def and_(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def call(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cbw(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def clc(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cld(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cli(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cmc(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cmps(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cs(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def cwd(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def daa(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def das(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def dec(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def div(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def ds(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def es(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def esc(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def hlt(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def idiv(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def imul(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def in_(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def inc(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def int_(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def into(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def iret(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jb(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jbe(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jcxz(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jl(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jle(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jmp(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jnb(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jnbe(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jnl(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jnle(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jno(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jnp(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jns(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jo(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def jp(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def js(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def lahf(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def lds(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def lea(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def les(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def lock(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def lods(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def loop(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def loope(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def loopne(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def movs(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def mul(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def neg(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def nop(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def not_(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def or_(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def out(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def pop(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def popf(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def push(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def pushf(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def rcl(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def rcr(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def rep(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def repne(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def ret(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def rol(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def ror(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def sahf(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def sal(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def sar(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def sbb(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def scas(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def shr(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def ss(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def stc(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def std(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def sti(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def stos(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def test(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def wait(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def xchg(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def xlat(cpu: Cpu, instr: Instr):
    raise NotImplementedError


def xor(cpu: Cpu, instr: Instr):
    raise NotImplementedError


ACTION = {
    "aaa": aaa,
    "aad": aad,
    "aam": aam,
    "aas": aas,
    "adc": adc,
    "add": add,
    "and": and_,
    "call": call,
    "cbw": cbw,
    "clc": clc,
    "cld": cld,
    "cli": cli,
    "cmc": cmc,
    "cmp": cmp,
    "cmps": cmps,
    "cs": cs,
    "cwd": cwd,
    "daa": daa,
    "das": das,
    "dec": dec,
    "div": div,
    "ds": ds,
    "es": es,
    "esc": esc,
    "hlt": hlt,
    "idiv": idiv,
    "imul": imul,
    "in": in_,
    "inc": inc,
    "int": int_,
    "into": into,
    "iret": iret,
    "jb": jb,
    "jbe": jbe,
    "jcxz": jcxz,
    "je": je,
    "jle": jle,
    "jl": jl,
    "jmp": jmp,
    "jnb": jnb,
    "jnbe": jnbe,
    "jne": jne,
    "jnle": jnle,
    "jnl": jnl,
    "jnz": jne,
    "jno": jno,
    "jnp": jnp,
    "jns": jns,
    "jo": jo,
    "jp": jp,
    "js": js,
    "jz": je,
    "lahf": lahf,
    "lds": lds,
    "lea": lea,
    "les": les,
    "lock": lock,
    "lods": lods,
    "loop": loop,
    "loope": loope,
    "loopne": loopne,
    "mov": mov,
    "movs": movs,
    "mul": mul,
    "neg": neg,
    "nop": nop,
    "not": not_,
    "or": or_,
    "out": out,
    "pop": pop,
    "popf": popf,
    "push": push,
    "pushf": pushf,
    "rcl": rcl,
    "rcr": rcr,
    "rep": rep,
    "repne": repne,
    "ret": ret,
    "rol": rol,
    "ror": ror,
    "sahf": sahf,
    "sal": sal,
    "sar": sar,
    "sbb": sbb,
    "scas": scas,
    "shr": shr,
    "ss": ss,
    "stc": stc,
    "std": std,
    "sti": sti,
    "stos": stos,
    "sub": sub,
    "test": test,
    "wait": wait,
    "xchg": xchg,
    "xlat": xlat,
    "xor": xor,
}
