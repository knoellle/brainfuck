import argparse
from pathlib import Path
import math

SET_ZERO = "[-]"

def SHIFT(offset):
    if offset < 0:
        return "<" * -offset
    else:
        return ">" * offset

def COPY_FROM(offset, restore=True):
    ls = SHIFT(offset)
    rs = SHIFT(-offset)
    program = SET_ZERO + ls + "[-" + rs + "+>+<" + ls + "]" + rs
    if restore:
        program += ">[-<" + ls + "+>" + rs + "]<"
    return program

def MOVE_FROM(offset, zero=True):
    ls = SHIFT(offset)
    rs = SHIFT(-offset)
    program = (SET_ZERO if zero else "") + ls + "[-" + rs + "+" + ls + "]" + rs
    return program

def ADD_CONSTANT(i, fast):
    if fast:
        return "+" * i
    sqrt = round(math.sqrt(i))
    remainder = i - sqrt * sqrt
    program = ""
    if remainder < 0:
        program += "-" * abs(remainder)
    else:
        program += "+" * remainder
    program += ">" + "+" * sqrt + "[-<" + "+" * sqrt + ">]<"
    return program

def ADD_FROM(offset, fast):
    ls = SHIFT(offset)
    rs = SHIFT(-offset)
    return ls + "[-" + rs + "+" + ls + "]" + rs

def MULT_CONSTANT(i, fast):
    return ">" + SET_ZERO + ADD_CONSTANT(i, fast) + MULT(fast)

def MULT(fast):
    # initial stack layout
    # [a, b]
    # working stack layout
    # [output, b, a, copyable, atemp]
    program = ">" + MOVE_FROM(-2) + "<"
    program += "[->>" + COPY_FROM(-1) + "<<<" + ADD_FROM(3, fast) + ">]>[-]<<"
    return program

def compile(input, args):
    program = ""
    for line in input:
        # parse line
        segments = line.strip().split(" ")
        if len(segments) == 0:
            continue
        print(segments)
        cmd = segments[0]
        # include commands in output file for debugging and pass on raw brainfuck code
        if args.debug or all((c in "<>[],.+-" for c in cmd)):
            program += f"{cmd}\n"
        # push a value to the stack
        if cmd == "push":
            program += ">" + SET_ZERO + ADD_CONSTANT(int(segments[1]), args.fast)
        # add a number to the stack top or add the two top values of the stack together
        if cmd == "add":
            if len(segments) == 2:
                program += ADD_CONSTANT(int(segments[1]), args.fast)
            else:
                program += "<[-<+>]"
        # multiply the top most value of the stack either by a constant or by the penultimate value
        if cmd == "mult":
            if len(segments) == 2:
                program += MULT_CONSTANT(int(segments[1]), args.fast)
            else:
                program += MULT(args.fast)
        # print the top value on the stack to stdout
        if cmd == "print":
            n = 0
            if len(segments) == 2:
                n = int(segments[1]) - 1
            program += "<" * n + "." + ">." * n
        if args.debug:
            program += "\n"
    return program

def main():
    parser = argparse.ArgumentParser("Brainfuck compiler")
    parser.add_argument("file", nargs="+")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--fast", action="store_true")
    args = parser.parse_args()

    # compile program
    f = open(args.file[0], "r")
    program = compile(f, args)

    # remove redundancies
    while "<>" in program or "><" in program:
        program = program.replace("<>", "").replace("><", "")

    # write output
    output_file = Path(args.file[0]).with_suffix(".bf")
    print(program)
    with open(output_file, "w") as of:
        of.write(program)

if __name__ == "__main__":
    main()
