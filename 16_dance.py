def s(x: list) -> str:
    return ''.join(x)


def spin(x: list, count: int) -> list:
    return x[-count:] + x[:-count]


def exchange(x: list, idx1: int, idx2: int) -> list:
    x[idx1], x[idx2] = x[idx2], x[idx1]
    return x


def partner(x: list, val1: str, val2: str) -> list:
    idx1 = x.index(val1)
    idx2 = x.index(val2)
    x[idx1], x[idx2] = x[idx2], x[idx1]
    return x


def dance(line: list, instrs: list) -> list:
    for x in instrs:
        instr = x[0]
        if instr == 's':
            line = spin(line, int(x[1:]))
        elif instr == 'x':
            a, b = map(int, x[1:].split('/'))
            line = exchange(line, int(a), int(b))
        elif instr == 'p':
            line = partner(line, x[1], x[3])
        else:
            raise ValueError(f'Invalid instruction code: {instr}')
    return line


if __name__ == '__main__':
    length = 16
    start = ord('a')
    line = [chr(x) for x in range(start, start + length)]
    line_init = line[:]
    print('Initial order: ' + s(line))

    instr_set = []
    with open('./dance.txt') as file:
        instr_set = file.read().strip().split(',')

    # PART 1
    line = dance(line, instr_set)
    print(f'Pt 1 final order: ' + s(line) + '\n')

    # PART 2
    # Confession: I had to read other people's answers to understand how this problem is solved. I'm doing it with two
    # optimizations: A memoized dance solver using `dance_memo` and a cycle finder using `cycle`. [NOTE] I'm assuming
    # a cycle is an integer multiple of dances. If the cycle is a multiple of instructions but not a multiple of dances,
    # the code becomes a bit more complex, but it's still feasible.

    dance_memo = {}  # k: starting permutation, v: final permutation
    line = line_init[:]
    key = s(line)
    cycle = [key]
    for i in range(int(1e9)):
        if key in dance_memo:
            line = dance_memo[key]
            key = s(line)
        else:
            line = dance(line, instr_set)
            dance_memo[key] = line
            key = s(line)

        if key in cycle:  # Cycle found. This # of dances returns the string back to its original state.
            break

        cycle.append(key)
    print(f'Cycle starting from initial value found. Length: {len(cycle)}')
    printout = ''
    for k in cycle:
        printout += f'{k} -> ' + s(dance_memo[k]) + '\n'
    print(printout)

    instr_ct = int(1e9) % len(cycle)
    print(f'Instructions after last cycle: {instr_ct}')
    final = cycle[instr_ct]  # value after `instr_ct`th dance already known. just get it.

    print('Pt 2 final order: ' + final)
