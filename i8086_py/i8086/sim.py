#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib.action import ACTION
from pylib.cpu import Cpu
from pylib.disasmbler import OPS
from pylib.executable import Exe


def main(args):
    with args.bin.open("rb") as f:
        data = f.read()

    exe = Exe(data=data, end=len(data))
    cpu = Cpu()

    while exe.idx < exe.end:
        op = OPS[exe.byte]
        instr = op.disasm(exe)
        ACTION[instr.mnem](cpu, instr)
        print(instr.format())

    cpu.output()


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
        help="""Compare the results to this file.""",
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
