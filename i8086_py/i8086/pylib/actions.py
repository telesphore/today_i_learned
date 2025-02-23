from i8086.pylib.cpu import Cpu
from i8086.pylib.instruction import Instr


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


def add(cpu: Cpu, instr: Instr):
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


def cmp(cpu: Cpu, instr: Instr):
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


def je(cpu: Cpu, instr: Instr):
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


def jne(cpu: Cpu, instr: Instr):
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


def mov(cpu: Cpu, instr: Instr):
    cpu.reg[instr.dst.type_][instr.dst.reg]


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


def sub(cpu: Cpu, instr: Instr):
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
