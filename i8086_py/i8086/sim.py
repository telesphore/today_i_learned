#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib.action import ACTION
from pylib.cpu import Cpu
from pylib.disasmbler import OPS


def main(args):
    with args.bin.open("rb") as f:
        prog = f.read()

    cpu = Cpu(prog=prog)

    while cpu.ip < cpu.end:
        op = OPS[cpu.byte]
        instr = op.disasm(cpu)
        ACTION[instr.mnem](cpu, instr)
        if not args.quiet:
            print(instr.format())

    if not args.quiet:
        print()
        cpu.display(start=1000)

    if args.dump:
        cpu.dump(args.dump)


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
        "--dump",
        "-d",
        type=Path,
        help="""Dump the cpu's memory to this file.""",
    )

    arg_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="""Don't print the programe status.""",
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
