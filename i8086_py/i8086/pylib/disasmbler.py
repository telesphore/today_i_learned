from collections.abc import Callable
from dataclasses import dataclass

from i8086.pylib import instruction as inst
from i8086.pylib.cpu import Cpu


@dataclass
class Byte1:
    """Make disassembly table driven."""

    b1: int
    disasm: Callable = None
    ops: int = None  # Which opcode table to use when the opdode is in the 2nd byte
    mnem: str = None
    fmt: str = ""


@dataclass
class BitFields:
    d: int = None
    w: int = None
    s: int = None
    mod: int = None
    reg: int = None
    rm: int = None
    op: int = None

    @classmethod
    def dw_fields(cls, byte):
        fields = cls()
        fields.d = (byte & 2) >> 1
        fields.w = byte & 1
        return fields

    @classmethod
    def sw_fields(cls, byte):
        fields1 = cls()
        fields1.s = (byte & 2) >> 1
        fields1.w = byte & 1
        return fields1

    @classmethod
    def mod_reg_rm_fields(cls, byte):
        fields = cls()
        fields.mod = (byte & 0o_300) >> 6
        fields.reg = (byte & 0o_70) >> 3
        fields.rm = byte & 7
        return fields

    @classmethod
    def mod_op_rm_fields(cls, byte):
        fields = cls()
        fields.mod = (byte & 0o_300) >> 6
        fields.op = (byte & 0o_70) >> 3
        fields.rm = byte & 7
        return fields


# ###########################################################################
def literal(cpu: Cpu, size: int) -> int:
    """
    Consume a literal value of the given size and return it.

    Note that cpu.ip is changed.
    """
    val = int.from_bytes(
        cpu.mem[cpu.ip : cpu.ip + size], byteorder="little", signed=True
    )
    cpu.ip += size
    return val


# ###########################################################################
RegRm = inst.EffAddr | inst.Reg


def calc_eff_addr(cpu: Cpu, fields1: BitFields, fields2: BitFields) -> inst.EffAddr:
    match fields2.mod:
        case 0 if fields2.rm == 0b_110:
            size = 1 + fields1.w
            disp = literal(cpu, size)
            eff_addr = inst.EffAddr(disp=disp, size=size)

        case 0:
            eff_addr = inst.EffAddr(ea_reg=fields2.rm, size=0)

        case 1:
            disp = literal(cpu, 1)
            eff_addr = inst.EffAddr(ea_reg=fields2.rm, disp=disp, size=1)

        case 2:
            disp = literal(cpu, 2)
            eff_addr = inst.EffAddr(ea_reg=fields2.rm, disp=disp, size=2)

        case 3:
            eff_addr = inst.Reg(fields2.rm, fields1.w)

    return eff_addr


def swap(fields1: BitFields, src: RegRm, dst: RegRm):
    return (src, dst) if fields1.d == 0 else (dst, src)


def mnemonic(byte1):
    return OPS[byte1].mnem


# ###########################################################################
def mod_reg_rm(cpu: Cpu) -> tuple[inst.Src, inst.Dst]:
    byte1 = cpu.consume_byte()
    byte2 = cpu.consume_byte()
    fields1 = BitFields.dw_fields(byte1)
    fields2 = BitFields.mod_reg_rm_fields(byte2)
    reg = inst.Reg(fields2.reg, fields1.w)
    eff_addr = calc_eff_addr(cpu, fields1, fields2)
    src, dst = swap(fields1, reg, eff_addr)
    return inst.Instr(key=byte1, src=src, dst=dst, mnem=mnemonic(byte1))


def mod_op_rm(cpu: Cpu, ops_group: int, imm_size):
    byte1 = cpu.consume_byte()
    byte2 = cpu.consume_byte()
    fields1 = BitFields.dw_fields(byte1)
    fields2 = BitFields.mod_op_rm_fields(byte2)
    eff_addr = calc_eff_addr(cpu, fields1, fields2)
    imm = inst.Imm(data=literal(cpu, imm_size), size=imm_size)
    mnem = inst.OPS2[ops_group][fields2.op]
    return inst.Instr(key=byte1, dst=eff_addr, imm=imm, mnem=mnem)


def mod_math_op_rm8(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_MATH1, 1)


def mod_math_op_rm16(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_MATH1, 2)


def mod_math_op2_rm(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_MATH2)


def mod_move_op_rm8(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_MOVE, 1)


def mod_move_op_rm16(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_MOVE, 2)


def mod_stack_op_rm(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_STACK)


def mod_shift_op_rm(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_SHIFT)


def mod_other_op_rm(cpu: Cpu):
    return mod_op_rm(cpu, inst.OP_OTHER)


def imm8(cpu: Cpu):
    byte1 = cpu.consume_byte()
    dst = inst.Reg(byte1 & 0o_7, inst.REG8)
    data = literal(cpu, 1)
    imm = inst.Imm(data, 1)
    return inst.Instr(key=byte1, dst=dst, imm=imm, mnem=mnemonic(byte1))


def imm16(cpu: Cpu):
    byte1 = cpu.consume_byte()
    dst = inst.Reg(byte1 & 0o_7, inst.REG16)
    data = literal(cpu, 2)
    imm = inst.Imm(data, 2)
    return inst.Instr(key=byte1, dst=dst, imm=imm, mnem=mnemonic(byte1))


def imm8a(cpu: Cpu):
    byte1 = cpu.consume_byte()
    dst = inst.Reg(inst.AL, inst.REG8)
    data = literal(cpu, 1)
    imm = inst.Imm(data, 1)
    return inst.Instr(key=byte1, dst=dst, imm=imm, mnem=mnemonic(byte1))


def imm16a(cpu: Cpu):
    byte1 = cpu.consume_byte()
    dst = inst.Reg(inst.AX, inst.REG16)
    data = literal(cpu, 2)
    imm = inst.Imm(data, 2)
    return inst.Instr(key=byte1, dst=dst, imm=imm, mnem=mnemonic(byte1))


def disp8(cpu: Cpu):
    byte1 = cpu.consume_byte()
    disp = literal(cpu, 1)
    src = inst.EffAddr(disp=disp, size=1)
    return inst.Instr(key=byte1, src=src, mnem=mnemonic(byte1))


def to_disp8(cpu: Cpu):
    byte1 = cpu.consume_byte()
    dst = inst.Reg(cpu.byte & 0o_7, inst.REG8)
    disp = literal(cpu, 1)
    src = inst.EffAddr(disp=disp, size=1)
    return inst.Instr(key=byte1, src=src, dst=dst, mnem=mnemonic(byte1))


def to_disp16(cpu: Cpu):
    byte1 = cpu.consume_byte()
    dst = inst.Reg(cpu.byte & 0o_7, inst.REG16)
    disp = literal(cpu, 2)
    src = inst.EffAddr(disp=disp, size=2)
    return inst.Instr(key=byte1, src=src, dst=dst, mnem=mnemonic(byte1))


def to_reg(cpu: Cpu):
    byte1 = cpu.consume_byte()
    reg = inst.Reg(byte1 & 0o_3, inst.REG16)
    return inst.Instr(key=byte1, dst=reg, mnem=mnemonic(byte1))


def from_reg(cpu: Cpu):
    byte1 = cpu.consume_byte()
    reg = inst.Reg(byte1 & 0o_3, inst.REG16)
    return inst.Instr(key=byte1, src=reg, mnem=mnemonic(byte1))


def ip8(cpu: Cpu):
    raise NotImplementedError


def mod_0sr_rm(cpu: Cpu):
    raise NotImplementedError


def mod_1xx_rm(cpu: Cpu):
    raise NotImplementedError


def disp16(cpu: Cpu):
    raise NotImplementedError


def addracc(cpu: Cpu):
    byte1 = cpu.consume_byte()
    fields1 = BitFields.dw_fields(byte1)

    if fields1.w == 0:
        reg = inst.Reg(inst.AL, inst.REG8)
    else:
        reg = inst.Reg(inst.AX, inst.REG16)

    disp = literal(cpu, 2)
    eff_addr = inst.EffAddr(disp=disp, size=2)

    src, dst = swap(fields1, eff_addr, reg)
    return inst.Instr(key=byte1, src=src, dst=dst, mnem=mnemonic(byte1))


def literal_2nd(cpu: Cpu):
    raise NotImplementedError


def mod_yyy_rm(cpu: Cpu):
    raise NotImplementedError


def seg(cpu: Cpu):
    raise NotImplementedError


def seg_prefix(cpu: Cpu):
    raise NotImplementedError


def decimal_adjust(cpu: Cpu):
    raise NotImplementedError


def acsii_adjust(cpu: Cpu):
    raise NotImplementedError


OPS = [
    Byte1(0x00, mod_reg_rm, mnem="add", fmt="add reg8/mem8,reg8"),
    Byte1(0x01, mod_reg_rm, mnem="add", fmt="add reg16/mem16,reg16"),
    Byte1(0x02, mod_reg_rm, mnem="add", fmt="add reg8,reg8/mem8"),
    Byte1(0x03, mod_reg_rm, mnem="add", fmt="add reg16,reg16/mem16"),
    Byte1(0x04, imm8a, mnem="add", fmt="add al,immed8"),
    Byte1(0x05, imm16a, mnem="add", fmt="add ax,immed16"),
    Byte1(0x06, seg, mnem="push", fmt="push es"),
    Byte1(0x07, seg, mnem="pop", fmt="pop es"),
    Byte1(0x08, mod_reg_rm, mnem="or", fmt="or reg8/mem8,reg8"),
    Byte1(0x09, mod_reg_rm, mnem="or", fmt="or reg16/mem16,reg16"),
    Byte1(0x0A, mod_reg_rm, mnem="or", fmt="or reg8,reg8/mem8"),
    Byte1(0x0B, mod_reg_rm, mnem="or", fmt="or reg16,reg16/mem16"),
    Byte1(0x0C, imm8a, mnem="or", fmt="or al,immed8"),
    Byte1(0x0D, imm16a, mnem="or", fmt="or ax,immed16"),
    Byte1(0x0E, seg, mnem="push", fmt="push cs"),
    Byte1(0x0F, seg, fmt="(not used)"),
    Byte1(0x10, mod_reg_rm, mnem="adc", fmt="adc reg8/mem8,reg8"),
    Byte1(0x11, mod_reg_rm, mnem="adc", fmt="adc reg16/mem16,reg16"),
    Byte1(0x12, mod_reg_rm, mnem="adc", fmt="adc reg8,reg8/mem8"),
    Byte1(0x13, mod_reg_rm, mnem="adc", fmt="adc reg16,reg16/mem16"),
    Byte1(0x14, imm8a, mnem="adc", fmt="adc al,immed8"),
    Byte1(0x15, imm16a, mnem="adc", fmt="adc ax,immed16"),
    Byte1(0x16, seg, mnem="push", fmt="push ss"),
    Byte1(0x17, seg, mnem="pop", fmt="pop ss"),
    Byte1(0x18, mod_reg_rm, mnem="sbb", fmt="sbb reg8/mem8,reg8"),
    Byte1(0x19, mod_reg_rm, mnem="sbb", fmt="sbb reg16/mem16,reg16"),
    Byte1(0x1A, mod_reg_rm, mnem="sbb", fmt="sbb reg8,reg8/mem8"),
    Byte1(0x1B, mod_reg_rm, mnem="sbb", fmt="sbb reg16,reg16/mem16"),
    Byte1(0x1C, imm8a, mnem="sbb", fmt="sbb al,immed8"),
    Byte1(0x1D, imm16a, mnem="sbb", fmt="sbb ax,immed16"),
    Byte1(0x1E, seg, mnem="push", fmt="push ds"),
    Byte1(0x1F, seg, mnem="pop", fmt="pop ds"),
    Byte1(0x20, mod_reg_rm, mnem="and", fmt="and reg8/mem8,reg8"),
    Byte1(0x21, mod_reg_rm, mnem="and", fmt="and reg16/mem16,reg16"),
    Byte1(0x22, mod_reg_rm, mnem="and", fmt="and reg8,reg8/mem8"),
    Byte1(0x23, mod_reg_rm, mnem="and", fmt="and reg16,reg16/mem16"),
    Byte1(0x24, imm8a, mnem="and", fmt="and al,immed8"),
    Byte1(0x25, imm16a, mnem="and", fmt="and ax,immed16"),
    Byte1(0x26, seg_prefix, mnem="es", fmt="es: (segment override prefix)"),
    Byte1(0x27, seg, mnem="daa", fmt="daa"),
    Byte1(0x28, mod_reg_rm, mnem="sub", fmt="sub reg8/mem8,reg8"),
    Byte1(0x29, mod_reg_rm, mnem="sub", fmt="sub reg16/mem16,reg16"),
    Byte1(0x2A, mod_reg_rm, mnem="sub", fmt="sub reg8,reg8/mem8"),
    Byte1(0x2B, mod_reg_rm, mnem="sub", fmt="sub reg16,reg16/mem16"),
    Byte1(0x2C, imm8a, mnem="sub", fmt="sub al,immed8"),
    Byte1(0x2D, imm16a, mnem="sub", fmt="sub ax,immed16"),
    Byte1(0x2E, seg_prefix, mnem="cs", fmt="cs: (segment override prefix)"),
    Byte1(0x2F, decimal_adjust, mnem="das", fmt="das"),
    Byte1(0x30, mod_reg_rm, mnem="xor", fmt="xor reg8/mem8,reg8"),
    Byte1(0x31, mod_reg_rm, mnem="xor", fmt="xor reg16/mem16,reg16"),
    Byte1(0x32, mod_reg_rm, mnem="xor", fmt="xor reg8,reg8/mem8"),
    Byte1(0x33, mod_reg_rm, mnem="xor", fmt="xor reg16,reg16/mem16"),
    Byte1(0x34, imm8a, mnem="xor", fmt="xor al,immed8"),
    Byte1(0x35, imm16a, mnem="xor", fmt="xor ax,immed16"),
    Byte1(0x36, seg_prefix, mnem="ss", fmt="ss: (segment override prefix)"),
    Byte1(0x37, acsii_adjust, mnem="aaa", fmt="aaa"),
    Byte1(0x38, mod_reg_rm, mnem="cmp", fmt="cmp reg8/mem8,reg8"),
    Byte1(0x39, mod_reg_rm, mnem="cmp", fmt="cmp reg16/mem16,reg16"),
    Byte1(0x3A, mod_reg_rm, mnem="cmp", fmt="cmp reg8,reg8/mem8"),
    Byte1(0x3B, mod_reg_rm, mnem="cmp", fmt="cmp reg16,reg16/mem16"),
    Byte1(0x3C, imm8a, mnem="cmp", fmt="cmp al,immed8"),
    Byte1(0x3D, imm16a, mnem="cmp", fmt="cmp ax,immed16"),
    Byte1(0x3E, seg_prefix, mnem="ds", fmt="ds: (segment override prefix)"),
    Byte1(0x3F, acsii_adjust, mnem="aas", fmt="aas"),
    Byte1(0x40, to_reg, mnem="inc", fmt="inc ax"),
    Byte1(0x41, to_reg, mnem="inc", fmt="inc cx"),
    Byte1(0x42, to_reg, mnem="inc", fmt="inc dx"),
    Byte1(0x43, to_reg, mnem="inc", fmt="inc bx"),
    Byte1(0x44, to_reg, mnem="inc", fmt="inc sp"),
    Byte1(0x45, to_reg, mnem="inc", fmt="inc bp"),
    Byte1(0x46, to_reg, mnem="inc", fmt="inc si"),
    Byte1(0x47, to_reg, mnem="inc", fmt="inc di"),
    Byte1(0x48, to_reg, mnem="dec", fmt="dec ax"),
    Byte1(0x49, to_reg, mnem="dec", fmt="dec cx"),
    Byte1(0x4A, to_reg, mnem="dec", fmt="dec ox"),
    Byte1(0x4B, to_reg, mnem="dec", fmt="dec bx"),
    Byte1(0x4C, to_reg, mnem="dec", fmt="dec sp"),
    Byte1(0x4D, to_reg, mnem="dec", fmt="dec bp"),
    Byte1(0x4E, to_reg, mnem="dec", fmt="dec si"),
    Byte1(0x4F, to_reg, mnem="dec", fmt="dec di"),
    Byte1(0x50, from_reg, mnem="push", fmt="push ax"),
    Byte1(0x51, from_reg, mnem="push", fmt="push cx"),
    Byte1(0x52, from_reg, mnem="push", fmt="push dx"),
    Byte1(0x53, from_reg, mnem="push", fmt="push bx"),
    Byte1(0x54, from_reg, mnem="push", fmt="push sp"),
    Byte1(0x55, from_reg, mnem="push", fmt="push bp"),
    Byte1(0x56, from_reg, mnem="push", fmt="push si"),
    Byte1(0x57, from_reg, mnem="push", fmt="push di"),
    Byte1(0x58, to_reg, mnem="pop", fmt="pop ax"),
    Byte1(0x59, to_reg, mnem="pop", fmt="pop cx"),
    Byte1(0x5A, to_reg, mnem="pop", fmt="pop dx"),
    Byte1(0x5B, to_reg, mnem="pop", fmt="pop bx"),
    Byte1(0x5C, to_reg, mnem="pop", fmt="pop sp"),
    Byte1(0x5D, to_reg, mnem="pop", fmt="pop bp"),
    Byte1(0x5E, to_reg, mnem="pop", fmt="pop si"),
    Byte1(0x5F, to_reg, mnem="pop", fmt="pop di"),
    Byte1(0x60, fmt="(not used)"),
    Byte1(0x61, fmt="(not used)"),
    Byte1(0x62, fmt="(not used)"),
    Byte1(0x63, fmt="(not used)"),
    Byte1(0x64, fmt="(not used)"),
    Byte1(0x65, fmt="(not used)"),
    Byte1(0x66, fmt="(not used)"),
    Byte1(0x67, fmt="(not used)"),
    Byte1(0x68, fmt="(not used)"),
    Byte1(0x69, fmt="(not used)"),
    Byte1(0x6A, fmt="(not used)"),
    Byte1(0x6B, fmt="(not used)"),
    Byte1(0x6C, fmt="(not used)"),
    Byte1(0x6D, fmt="(not used)"),
    Byte1(0x6E, fmt="(not used)"),
    Byte1(0x6F, fmt="(not used)"),
    Byte1(0x70, disp8, mnem="jo", fmt="jo short-label"),
    Byte1(0x71, disp8, mnem="jno", fmt="jno short-label"),
    Byte1(0x72, disp8, mnem="jb", fmt="jb/jnaei short-label jc"),
    Byte1(0x73, disp8, mnem="jnb", fmt="jnb/jaei short-label jnc"),
    Byte1(0x74, disp8, mnem="jz", fmt="je/jz short-label"),
    Byte1(0x75, disp8, mnem="jnz", fmt="jne/jnz short-label"),
    Byte1(0x76, disp8, mnem="jbe", fmt="jbe/jna short-label"),
    Byte1(0x77, disp8, mnem="jnbe", fmt="jnbe/ja short-label"),
    Byte1(0x78, disp8, mnem="js", fmt="js short-label"),
    Byte1(0x79, disp8, mnem="jns", fmt="jns short-label"),
    Byte1(0x7A, disp8, mnem="jp", fmt="jp/jpe short-label"),
    Byte1(0x7B, disp8, mnem="jnp", fmt="jnp/jpo short-label"),
    Byte1(0x7C, disp8, mnem="jl", fmt="jl/jnge short-label"),
    Byte1(0x7D, disp8, mnem="jnl", fmt="jnlljge short-label"),
    Byte1(0x7E, disp8, mnem="jle", fmt="jle/jng short-label"),
    Byte1(0x7F, disp8, mnem="jnle", fmt="jnle/jg short-label"),
    Byte1(0x80, mod_math_op_rm8, fmt="add reg8/mem8,immed8"),
    Byte1(0x81, mod_math_op_rm16, fmt="add reg16/mem16,immed16"),
    Byte1(0x82, mod_math_op_rm8, fmt="add reg8/mem8,immed8"),
    Byte1(0x83, mod_math_op_rm8, fmt="add reg16/mem16,immed8"),
    Byte1(0x84, mod_reg_rm, mnem="test", fmt="test reg8/mem8,reg8"),
    Byte1(0x85, mod_reg_rm, mnem="test", fmt="test reg16/mem16,reg16"),
    Byte1(0x86, mod_reg_rm, mnem="xchg", fmt="xchg reg8,reg8/mem8"),
    Byte1(0x87, mod_reg_rm, mnem="xchg", fmt="xchg reg16,reg16/mem16"),
    Byte1(0x88, mod_reg_rm, mnem="mov", fmt="mov reg8/mem8,reg8"),
    Byte1(0x89, mod_reg_rm, mnem="mov", fmt="mov reg16/mem16,reg16"),
    Byte1(0x8A, mod_reg_rm, mnem="mov", fmt="mov reg8,reg8/mem8"),
    Byte1(0x8B, mod_reg_rm, mnem="mov", fmt="mov reg16,reg16/mem16"),
    Byte1(0x8C, mod_0sr_rm, mnem="mov", fmt="mov reg16/mem16,segreg"),
    Byte1(0x8D, mod_reg_rm, mnem="lea", fmt="lea reg16,mem16"),
    Byte1(0x8E, mod_0sr_rm, mnem="mov", fmt="mov segreg,reg16/mem16"),
    Byte1(0x8F, mod_stack_op_rm, fmt="pop reg16/mem16"),
    Byte1(0x90, mnem="nop", fmt="nop (exchange ax,ax)"),
    Byte1(0x91, mnem="xchg", fmt="xchg ax,cx"),
    Byte1(0x92, mnem="xchg", fmt="xchg ax,dx"),
    Byte1(0x93, mnem="xchg", fmt="xchg ax,bx"),
    Byte1(0x94, mnem="xchg", fmt="xchg ax,sp"),
    Byte1(0x95, mnem="xchg", fmt="xchg ax,bp"),
    Byte1(0x96, mnem="xchg", fmt="xchg ax,si"),
    Byte1(0x97, mnem="xchg", fmt="xchg ax,di"),
    Byte1(0x98, mnem="cbw", fmt="cbw"),
    Byte1(0x99, mnem="cwd", fmt="cwd"),
    Byte1(0x9A, disp16, mnem="call", fmt="call far_proc"),
    Byte1(0x9B, mnem="wait", fmt="wait"),
    Byte1(0x9C, mnem="pushf", fmt="pushf"),
    Byte1(0x9D, mnem="popf", fmt="popf"),
    Byte1(0x9E, mnem="sahf", fmt="sahf"),
    Byte1(0x9F, mnem="lahf", fmt="lahf"),
    Byte1(0xA0, addracc, mnem="mov", fmt="mov al,mem8"),
    Byte1(0xA1, addracc, mnem="mov", fmt="mov ax,mem16"),
    Byte1(0xA2, addracc, mnem="mov", fmt="mov mem8,al"),
    Byte1(0xA3, addracc, mnem="mov", fmt="mov mem16,al"),
    Byte1(0xA4, mnem="movs", fmt="movs dest-str8,src-str8"),
    Byte1(0xA5, mnem="movs", fmt="movs dest-str16,src-str16"),
    Byte1(0xA6, mnem="cmps", fmt="cmps dest-str8,src-str8"),
    Byte1(0xA7, mnem="cmps", fmt="cmps dest-str16,src-str16"),
    Byte1(0xA8, imm8, mnem="test", fmt="test al,immed8"),
    Byte1(0xA9, imm16, mnem="test", fmt="test ax,immed16"),
    Byte1(0xAA, mnem="stos", fmt="stos dest-str8"),
    Byte1(0xAB, mnem="stos", fmt="stos dest-str16"),
    Byte1(0xAC, mnem="lods", fmt="lods src-str8"),
    Byte1(0xAD, mnem="lods", fmt="lods src-str16"),
    Byte1(0xAE, mnem="scas", fmt="scas dest-str8"),
    Byte1(0xAF, mnem="scas", fmt="scas dest-str16"),
    Byte1(0xB0, imm8, mnem="mov", fmt="mov al,immed8"),
    Byte1(0xB1, imm8, mnem="mov", fmt="mov cl,immed8"),
    Byte1(0xB2, imm8, mnem="mov", fmt="mov dl,immed8"),
    Byte1(0xB3, imm8, mnem="mov", fmt="mov bl,immed8"),
    Byte1(0xB4, imm8, mnem="mov", fmt="mov ah,immed8"),
    Byte1(0xB5, imm8, mnem="mov", fmt="mov ch,immed8"),
    Byte1(0xB6, imm8, mnem="mov", fmt="mov dh,immed8"),
    Byte1(0xB7, imm8, mnem="mov", fmt="mov bh,immed8"),
    Byte1(0xB8, imm16, mnem="mov", fmt="mov ax,immed16"),
    Byte1(0xB9, imm16, mnem="mov", fmt="mov cx,immed16"),
    Byte1(0xBA, imm16, mnem="mov", fmt="mov dx,immed16"),
    Byte1(0xBB, imm16, mnem="mov", fmt="mov bx,immed16"),
    Byte1(0xBC, imm16, mnem="mov", fmt="mov sp,immed16"),
    Byte1(0xBD, imm16, mnem="mov", fmt="mov bp,immed16"),
    Byte1(0xBE, imm16, mnem="mov", fmt="mov si,immed16"),
    Byte1(0xBF, imm16, mnem="mov", fmt="mov di,immed16"),
    Byte1(0xC0, fmt="(not used)"),
    Byte1(0xC1, fmt="(not used)"),
    Byte1(0xC2, imm16, mnem="ret", fmt="ret immed16 (intraseg)"),
    Byte1(0xC3, mnem="ret", fmt="ret (intrasegment)"),
    Byte1(0xC4, mod_reg_rm, mnem="les", fmt="les reg16,mem16"),
    Byte1(0xC5, mod_reg_rm, mnem="lds", fmt="lds reg16,mem16"),
    Byte1(0xC6, mod_move_op_rm8, mnem="mov", fmt="mov mem8,immed8"),
    Byte1(0xC7, mod_move_op_rm16, mnem="mov", fmt="mov mem16,immed16"),
    Byte1(0xC8, fmt="(not used)"),
    Byte1(0xC9, fmt="(not used)"),
    Byte1(0xCA, imm16, mnem="ret", fmt="ret immed16 (intersegment)"),
    Byte1(0xCB, mnem="ret", fmt="ret (intersegment)"),
    Byte1(0xCC, mnem="int", fmt="int 3"),
    Byte1(0xCD, imm8, mnem="int", fmt="int immed8"),
    Byte1(0xCE, mnem="into", fmt="into"),
    Byte1(0xCF, mnem="iret", fmt="iret"),
    Byte1(0xD0, mod_shift_op_rm, fmt="rol reg8/mem8,1"),
    Byte1(0xD1, mod_shift_op_rm, fmt="rol reg16/mem16,1"),
    Byte1(0xD2, mod_shift_op_rm, fmt="rol reg8/mem8,cl"),
    Byte1(0xD3, mod_shift_op_rm, fmt="rol reg16/mem16,cl"),
    Byte1(0xD4, literal_2nd, mnem="aam", fmt="aam"),  # literal = 00001010
    Byte1(0xD5, literal_2nd, mnem="aad", fmt="aad"),  # literal = 00001010
    Byte1(0xD6, fmt="(not used)"),
    Byte1(0xD7, mnem="xlat", fmt="xlat source-table"),
    Byte1(0xD8, mod_yyy_rm, fmt="?"),
    Byte1(0xD9, mod_yyy_rm, mnem="esc", fmt="esc opcode,source"),
    Byte1(0xDA, mod_yyy_rm, mnem="esc", fmt="esc opcode,source"),
    Byte1(0xDB, mod_yyy_rm, mnem="esc", fmt="esc opcode,source"),
    Byte1(0xDC, mod_yyy_rm, mnem="esc", fmt="esc opcode,source"),
    Byte1(0xDD, mod_yyy_rm, mnem="esc", fmt="esc opcode,source"),
    Byte1(0xDE, mod_yyy_rm, mnem="esc", fmt="esc opcode,source"),
    Byte1(0xDF, mod_yyy_rm, fmt="?"),
    Byte1(0xE0, disp8, mnem="loopne", fmt="loopne/loopnz short-label"),
    Byte1(0xE1, disp8, mnem="loope", fmt="loope/loopz short-label"),
    Byte1(0xE2, disp8, mnem="loop", fmt="loop short-label"),
    Byte1(0xE3, disp8, mnem="jcxz", fmt="jcxz short~label"),
    Byte1(0xE4, imm8a, mnem="in", fmt="in al,immed8"),
    Byte1(0xE5, imm8a, mnem="in", fmt="in ax,immed8"),
    Byte1(0xE6, imm8a, mnem="out", fmt="out al,immed8"),
    Byte1(0xE7, imm8a, mnem="out", fmt="out ax,immed8"),
    Byte1(0xE8, disp8, mnem="call", fmt="call near-proc"),
    Byte1(0xE9, disp8, mnem="jmp", fmt="jmp near-label"),
    Byte1(0xEA, ip8, mnem="jmp", fmt="jmp far-label"),
    Byte1(0xEB, disp8, mnem="jmp", fmt="jmp short-label"),
    Byte1(0xEC, mnem="in", fmt="in al,dx"),
    Byte1(0xED, mnem="in", fmt="in ax,dx"),
    Byte1(0xEE, mnem="out", fmt="out al,dx"),
    Byte1(0xEF, mnem="out", fmt="out ax,dx"),
    Byte1(0xF0, mnem="lock", fmt="lock (prefix)"),
    Byte1(0xF1, fmt="(not used)"),
    Byte1(0xF2, mnem="repne", fmt="repne/repnz"),
    Byte1(0xF3, mnem="rep", fmt="rep/repe/rerz"),
    Byte1(0xF4, mnem="hlt", fmt="hlt"),
    Byte1(0xF5, mnem="cmc", fmt="cmc"),
    Byte1(0xF6, mod_math_op2_rm, fmt="test reg8/mem8,immed8"),
    Byte1(0xF7, mod_math_op2_rm, fmt="test reg16/mem16,immed16"),
    Byte1(0xF8, mnem="clc", fmt="clc"),
    Byte1(0xF9, mnem="stc", fmt="stc"),
    Byte1(0xFA, mnem="cli", fmt="cli"),
    Byte1(0xFB, mnem="sti", fmt="sti"),
    Byte1(0xFC, mnem="cld", fmt="cld"),
    Byte1(0xFD, mnem="std", fmt="std"),
    Byte1(0xFE, mod_other_op_rm, fmt="inc reg8/mem8"),
    Byte1(0xFF, mod_other_op_rm, fmt="inc mem16"),
]
