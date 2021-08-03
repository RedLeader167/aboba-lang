import sys

if len(sys.argv) < 2:
    print("Usage: python aboba.py <filename> [dbg]")
    sys.exit(1)

try:
    code = open(sys.argv[1]).read()
except:
    print("Failed to open.")
    sys.exit()

pointer = -1
vars = {0: 0}
stack = []
openvar = 0
cmd = None
loop = []
loopif = 0

def advance(step=1):
    global code, pointer, cmd
    pointer += step
    cmd = code[pointer] if pointer < len(code) else None

def crash(text):
    print("*** Program got crashed! ***\nDetails: " + text + "\nCrash occured at char " + str(pointer + 1))
    sys.exit(1)

def toint(num):
    try:
        return int(num)
    except:
        crash("Not an integer!")
advance()
while cmd != None:
    if len(sys.argv) > 2 and sys.argv[2] == "dbg": print("dbg:", pointer, cmd, openvar, vars[openvar], stack)
    if cmd == "%":
        advance()
        f = ""
        while cmd != None and cmd in "0123456789":
            f += cmd
            advance()
        advance(-1)
        f = toint(f)
        if f not in vars:
            vars[f] = 0
        openvar = f
    if cmd == "\"":
        while cmd != None and cmd != "\n":
            advance()
    elif cmd == "+":
        advance()
        f = ""
        while cmd != None and cmd in "0123456789":
            f += cmd
            advance()
        advance(-1)
        f = toint(f)
        vars[openvar] += f
    elif cmd == "-":
        advance()
        f = ""
        while cmd != None and cmd in "0123456789":
            f += cmd
            advance()
        advance(-1)
        f = toint(f)
        vars[openvar] -= f
    elif cmd == "?":
        advance()
        if vars[openvar] == 0:
            if cmd == "<":
                while cmd != None and cmd != "|":
                    advance(-1)
            elif cmd == ">":
                while cmd != None and cmd != "|":
                    advance(1)
            else:
                crash("Invalid ? instruction")
    elif cmd == "i":
        advance()
        if cmd == "c":
            vars[openvar] = toint(ord(input()[0]))
        elif cmd == "n":
            vars[openvar] = toint(input())
        else:
            crash("Invalid input instruction")
    elif cmd == "{":
        if vars[openvar] != 0:
            loop.append(pointer)
        else:
            ip = 0
            while cmd != None:
                advance()
                if cmd == "{": ip += 1
                if cmd == "}":
                    if ip == 0: break
                    else: ip -= 1
    elif cmd == "}":
        if loopif == 0:
            if vars[openvar] != 0:
                pointer = loop[len(loop) - 1]
            else:
                loop.pop()
    elif cmd == "[":
        advance()
        f = ""
        while cmd != None and cmd in "0123456789":
            f += cmd
            advance()
        advance(-1)
        f = toint(f)
        if vars[openvar] != f:
            while cmd != None and cmd != "]":
                advance()
            advance()
    elif cmd == "(":
        print(chr(vars[openvar]), end='')
    elif cmd == ")":
        print(vars[openvar], end='')
    elif cmd == "~":
        sys.exit(0)
    elif cmd == "s":
        advance()
        if cmd == "p":
            stack.append(vars[openvar])
        elif cmd == "g":
            vars[openvar] = stack.pop()
        elif cmd == "d":
            stack.append(stack[len(stack) - 1])
        elif cmd == "+":
            stack.append(stack.pop() + stack.pop())
        elif cmd == "-":
            stack.append(stack.pop() - stack.pop())
        elif cmd == "*":
            stack.append(stack.pop() * stack.pop())
        elif cmd == "/":
            stack.append(int(stack.pop() / stack.pop()))
        elif cmd == "w":
            s1 = stack.pop()
            s2 = stack.pop()
            stack.extend([s1, s2])
        else:
            crash("Stack instruction is invalid!")
    advance()