#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib.action import ACTION
from pylib.cpu import Cpu
from pylib.disasmbler import OPS


def main(args):
    with args.bin.open("rb") as f:
        data = f.read()

    cpu = Cpu(data=data, end=len(data))

    while cpu.ip < cpu.end:
        op = OPS[cpu.byte]
        instr = op.disasm(cpu)
        ACTION[instr.mnem](cpu, instr)
        print(instr.format())

    print()
    cpu.display()


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

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
