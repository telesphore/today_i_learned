#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib.disasmbler import OPS
from pylib.executable import Exe
from pylib.instruction import INSTR, Instr


def main(args):
    with args.bin.open("rb") as f:
        data = f.read()

    exe = Exe(data=data, end=len(data))

    while exe.idx < exe.end:
        op = OPS[exe.byte]
        src, dst, *mnem = op.disasm(exe)
        instr = Instr(src=src, dst=dst)
        instr.mnem = mnem if mnem else op.mnem
        instr.act = INSTR[instr.mnem].act


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
