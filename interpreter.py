import argparse
import sys
import time

def main():
    parser = argparse.ArgumentParser("Brainfuck interpreter")
    parser.add_argument("file", nargs="+")
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--nowait", action="store_true", default=False)
    args = parser.parse_args()

    f = open(args.file[0], "r")

    memory = [0]
    pointer = 0
    # ignore non brainfuck instructions in code
    program = list(filter(lambda c: c in "><+-.,[]", "".join(f.readlines())))
    ip = 0
    output = ""
    cycles = 0

    while ip < len(program):
        cycles += 1
        c = program[ip]
        if c == "q":
            break
        if c == ">":
            pointer += 1
            if len(memory) == pointer:
                memory.append(0)
        if c == "<":
            if pointer > 0:
                pointer -= 1
            else:
                memory.insert(0, 0)
        if c == "+":
            memory[pointer] = (memory[pointer] + 1) % 256
        if c == "-":
            memory[pointer] = (memory[pointer] - 1) % 256
        if c == ".":
            output += chr(memory[pointer])
            print(chr(memory[pointer]), end="")
        if c == ",":
            memory[pointer] = ord(sys.stdin.read(1))
        if c == "[":
            if memory[pointer] == 0:
                level = 1
                while level > 0:
                    ip += 1
                    if len(program) == ip:
                        print("Error: invalid loop! ']' missing")
                        return
                    if program[ip] == "[":
                        level += 1
                    if program[ip] == "]":
                        level -= 1
        if c == "]":
            if memory[pointer] != 0:
                level = 1
                while level > 0:
                    ip -= 1
                    if ip < 0:
                        print("Error: invalid loop! '[' missing")
                        return
                    if program[ip] == "]":
                        level += 1
                    if program[ip] == "[":
                        level -= 1
        if args.debug:
            # display memory
            s = [str(i) for i in memory]
            print(" ".join(s[:pointer]) + "[" + s[pointer] + "]" + " ".join(s[pointer+1:]))
            # display program
            print("".join(program[:ip]), program[ip], "".join(program[ip+1:]))
            # print ALL the output again so it doesn't get lost in the debug information
            print(output)
            if not args.nowait:
                time.sleep(0.05)
        # increment instruction pointer
        ip += 1

    print(memory)
    print("".join(program))
    print(f"Cycles: {cycles}. Program length: {len(program)}")

if __name__ == "__main__":
    main()
