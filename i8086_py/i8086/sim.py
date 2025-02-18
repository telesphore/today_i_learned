#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

REG = [
    " al cl dl bl ah ch dh bh ".split(),
    " ax cx dx bx sp bp si di ".split(),
]

EA_REG = ["bx + si", "bx + di", "bp + si", "bp + di", "si", "di", "bp", "bx"]

TEST = """
    mov add sub cmp
    ja jb jbe jcxz je jg jl jle jnb jne jnl jno jnp jns jnz jo jp js jz
    loop loopnz loopz
    """.split()

MATH = " add ? adc sbb ? sub ? cmp ".split()


def main(args):
    with args.asm.open() as f:
        code = f.readlines()
    code = [ln.strip() for ln in code if ln.split() and ln.split()[0] in TEST]

    with args.bin.open("rb") as f:
        data = f.read()
    end = len(data)

    disasm = []

    i = 0
    while i < end:
        # for k in range(i, i + 2):
        #     print(f"{data[k]:08b}")
        match data[i]:
            case b if (b >> 2) == 0b_100010:
                asm, i = reg_rm("mov", data, i)
            case b if (b >> 1) == 0b_1100011:
                asm, i = mov_imm_rm("mov", data, i)
            case b if (b >> 4) == 0b_1011:
                asm, i = imm_reg("mov", data, i)
            case b if (b >> 1) == 0b_1010000:
                asm, i = mem_acc("mov", data, i, d=0)
            case b if (b >> 1) == 0b_1010001:
                asm, i = mem_acc("mov", data, i, d=1)

            case b if (b >> 2) == 0b_100000:
                asm, i = math_imm_rm(data, i)

            case b if (b >> 2) == 0b_000000:
                asm, i = reg_rm("add", data, i)
            case b if (b >> 1) == 0b_0000010:
                asm, i = imm_acc("add", data, i)

            case b if (b >> 2) == 0b_001010:
                asm, i = reg_rm("sub", data, i)
            case b if (b >> 1) == 0b_0010110:
                asm, i = imm_acc("sub", data, i)

            case b if (b >> 2) == 0b_001110:
                asm, i = reg_rm("cmp", data, i)
            case b if (b >> 1) == 0b_0011110:
                asm, i = imm_acc("cmp", data, i)

            case b if b == 0b_01110101:
                asm, i = jump("jnz", data, i)
            case b if b == 0b_01110100:
                asm, i = jump("jz", data, i)
            case b if b == 0b_01111100:
                asm, i = jump("jl", data, i)
            case b if b == 0b_01111110:
                asm, i = jump("jle", data, i)
            case b if b == 0b_01110010:
                asm, i = jump("jb", data, i)
            case b if b == 0b_01110110:
                asm, i = jump("jbe", data, i)
            case b if b == 0b_01111010:
                asm, i = jump("jp", data, i)
            case b if b == 0b_01110000:
                asm, i = jump("jo", data, i)
            case b if b == 0b_01111000:
                asm, i = jump("js", data, i)
            case b if b == 0b_01110101:
                asm, i = jump("jne", data, i)
            case b if b == 0b_01111101:
                asm, i = jump("jnl", data, i)
            case b if b == 0b_01111111:
                asm, i = jump("jg", data, i)
            case b if b == 0b_01110011:
                asm, i = jump("jnb", data, i)
            case b if b == 0b_01110111:
                asm, i = jump("ja", data, i)
            case b if b == 0b_01111011:
                asm, i = jump("jnp", data, i)
            case b if b == 0b_01110001:
                asm, i = jump("jno", data, i)
            case b if b == 0b_01111001:
                asm, i = jump("jns", data, i)
            case b if b == 0b_11100010:
                asm, i = jump("loop", data, i)
            case b if b == 0b_11100001:
                asm, i = jump("loopz", data, i)
            case b if b == 0b_11100000:
                asm, i = jump("loopnz", data, i)
            case b if b == 0b_11100011:
                asm, i = jump("jcxz", data, i)

            case _:
                print(f"Unknown instruction: {data[i]:08b}")
                break

        disasm.append(asm)
        print(asm)
        # print()

    print("ok" if code == disasm else "What have I done?!")


def jump(ins, data, i):
    i += 1
    off = literal(data, i, 1)
    i += 1
    return f"{ins} {off}", i


def reg_rm(ins, data, i):
    # print("reg_rm")
    d = (data[i] & 0b_1_0) >> 1
    w = data[i] & 0b_1
    i += 1

    mod = (data[i] & 0b_11_000000) >> 6
    reg = (data[i] & 0b_00_111_000) >> 3
    rm = data[i] & 0b_00000_111
    i += 1

    reg = REG[w][reg]
    ea_reg = EA_REG[rm]

    match mod:
        case 0b_00 if rm == 0b_110:
            j = 1 + w
            addr = literal(data, i, j)
            asm = f"{ins} {reg}, [{addr}]"
            i += j

        case 0b_00:
            eff_addr = format_eff_addr(ea_reg, 0)
            src, dst = (reg, eff_addr) if d == 0 else (eff_addr, reg)
            asm = f"{ins} {dst}, {src}"

        case 0b_01:
            off = literal(data, i, 1)
            eff_addr = format_eff_addr(ea_reg, off)
            src, dst = (reg, eff_addr) if d == 0 else (eff_addr, reg)
            asm = f"{ins} {dst}, {src}"
            i += 1

        case 0b_10:
            off = literal(data, i, 2)
            eff_addr = format_eff_addr(ea_reg, off)
            src, dst = (reg, eff_addr) if d == 0 else (eff_addr, reg)
            asm = f"{ins} {dst}, {src}"
            i += 2

        case 0b_11:
            eff_addr = REG[w][rm]
            src, dst = (reg, eff_addr) if d == 0 else (eff_addr, reg)
            asm = f"{ins} {dst}, {src}"

    return asm, i


def mov_imm_rm(ins, data, i):
    # print("mov_imm_rm")
    w = data[i] & 0b_0000000_1
    i += 1

    mod = (data[i] & 0b_11_000000) >> 6
    rm = data[i] & 0b_00000_111
    i += 1

    ea_reg = EA_REG[rm]

    match mod:
        case 0b_00 if rm == 0b_110:
            j = 1 + w
            addr = literal(data, i, j)
            eff_addr = f"[{addr}]"
            i += j

        case 0b_00:
            eff_addr = format_eff_addr(ea_reg, 0)

        case 0b_01:
            off = literal(data, i, 1)
            eff_addr = format_eff_addr(ea_reg, off)
            i += 1

        case 0b_10:
            off = literal(data, i, 2)
            eff_addr = format_eff_addr(ea_reg, off)
            i += 2

        case 0b_11:
            eff_addr = REG[w][rm]

    j = 1 + w
    imm = literal(data, i, j)
    i += j

    val = f"{'byte' if w == 0 else 'word'} {imm}"

    asm = f"{ins} {eff_addr}, {val}"

    return asm, i


def math_imm_rm(data, i):
    # print("math_imm_rm")
    sw = data[i] & 0b_000000_11
    w = data[i] & 0b_0000000_1
    i += 1

    mod = (data[i] & 0b_11_000000) >> 6
    ins = (data[i] & 0b_00_111_000) >> 3
    rm = data[i] & 0b_111
    i += 1

    # print(f"sw={sw:02b} w={w:01b} mod={mod:02b} ins={ins:03b} rm={rm:03b}")

    ea_reg = EA_REG[rm]

    match mod:
        case 0b_00 if rm == 0b_110:
            j = 1 + w
            addr = literal(data, i, j)
            eff_addr = f"[{addr}]"
            i += j

        case 0b_00:
            eff_addr = format_eff_addr(ea_reg, 0)

        case 0b_01:
            off = literal(data, i, 1)
            eff_addr = format_eff_addr(ea_reg, off)
            i += 1

        case 0b_10:
            off = literal(data, i, 2)
            eff_addr = format_eff_addr(ea_reg, off)
            i += 2

        case 0b_11:
            eff_addr = REG[w][rm]

    j = 1 + (1 if sw == 1 else 0)
    imm = literal(data, i, j)
    i += j

    val = f"{'byte' if w == 0 else 'word'} {imm}"

    asm = f"{MATH[ins]} {eff_addr}, {val}"

    return asm, i


def imm_reg(ins, data, i):
    # print("imm_reg")
    w = (data[i] & 0b_1_000) >> 3
    reg = REG[w][data[i] & 0b_00000_111]
    i += 1

    j = 1 + w
    imm = literal(data, i, j)
    i += j

    return f"{ins} {reg}, {imm}", i


def mem_acc(ins, data, i, d):
    # print("mem_acc")
    w = data[i] & 0b_1
    i += 1

    j = 1 + w
    addr = literal(data, i, j)
    addr = f"[{addr}]"
    i += j

    src, dst = (addr, "ax") if d == 0 else ("ax", addr)

    asm = f"{ins} {dst}, {src}"

    return asm, i


def imm_acc(ins, data, i):
    # print("imm_acc")
    w = data[i] & 0b_1
    i += 1

    j = 1 + w
    imm = literal(data, i, j)
    i += j

    reg = "al" if w == 0 else "ax"

    return f"{ins} {reg}, {imm}", i


def literal(data, i, size):
    val = int.from_bytes(data[i : i + size], byteorder="little", signed=True)
    return val


def format_eff_addr(ea_reg, off):
    eff_addr = f"[{ea_reg} + {off}]" if off != 0 else f"[{ea_reg}]"
    eff_addr = eff_addr.replace("+ -", "- ")
    return eff_addr


def parse_args():
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=textwrap.dedent("""Parse i8086 instructions."""),
    )

    arg_parser.add_argument(
        "--bin",
        "-b",
        type=Path,
        required=True,
        help="""Path to a binary file to parse.""",
    )

    arg_parser.add_argument(
        "--asm",
        "-a",
        type=Path,
        required=True,
        help="""Compare the results to this file.""",
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
