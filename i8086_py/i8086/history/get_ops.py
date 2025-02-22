#!/usr/bin/env python3

from pylib import disasm, instr

mnem = set()

for op in disasm.OPS:
    if op.mnem:
        mnem.add(op.mnem)

for ops_ in instr.OPS2:
    for op in ops_:
        if op != "ERR":
            mnem.add(op)

for op in sorted(mnem):
    print(f"def {op}():")
    print("    pass")
    print("\n")

print("INSTR = [")
for op in sorted(mnem):
    print(f'    Instr("{op}", act={op}),')
print("]")
