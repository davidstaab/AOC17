def init_safe_exec(exc_locals: dict):
    """
    Creates a persistent sandbox environment for calls to `exec`
    :return: `safe_exec`, a function that can be called instead of `exec`
    """
    exc_globals = {'__builtins__': None}

    def safe_exec(cmd: str):
        exec(cmd, exc_globals, exc_locals)

    return safe_exec


def init_safe_eval(exc_locals: dict):
    """
    Creates a persistent sandbox environment for calls to `eval`
    :return: `safe_eval`, a function that can be called instead of `eval`
    """
    exc_globals = {'__builtins__': None}

    def safe_eval(expr: str):
        return eval(expr, exc_globals, exc_locals)

    return safe_eval


if __name__ == '__main__':
    context = {}
    execs = init_safe_exec(exc_locals=context)
    evals = init_safe_eval(exc_locals=context)

    def val(x: str) -> str:
        if x.isdigit():
            return x
        else:
            return str(evals(x))

    instrs = []
    with open('./duet.txt') as file:
        instrs = [x.rstrip().split() for x in file.readlines()]

    # TEST CODE
    # test = """set a 1
    #         add a 2
    #         mul a a
    #         mod a 5
    #         snd a
    #         set a 0
    #         rcv a
    #         jgz a -1
    #         set a 1
    #         jgz a -2"""
    # instrs = [x.strip().split() for x in test.split(sep='\n')]
    ###########

    i = 0
    while 0 <= i < len(instrs):
        instr = instrs[i][0]
        reg = instrs[i][1]
        if reg not in context:
            context[reg] = '0'

        if instr == 'set':
            cmd = f'{reg} = ' + val(instrs[i][2])
        elif instr == 'add':
            cmd = f'{reg} += ' + val(instrs[i][2])
        elif instr == 'mul':
            cmd = f'{reg} *= ' + val(instrs[i][2])
        elif instr == 'mod':
            cmd = f'{reg} %= ' + val(instrs[i][2])
        elif instr == 'snd':
            cmd = 'sound = ' + val(reg)
        elif instr == 'rcv' and int(val(reg)) != 0:
            cmd = ''
            print(f"Last frequency played: {context['sound']}")
            break  # PART 1
        elif instr == 'jgz' and int(val(reg)) > 0:
            i_old = i
            i += int(val(instrs[i][2]))
            print(f'{i_old}: Skipping to instruction {i}')
            continue
        print(f'{i}: {cmd}')
        execs(cmd)
        i += 1
