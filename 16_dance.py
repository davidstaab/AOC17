def spin(count: int):
    global line
    line = line[-count:] + line[:-count]


def exchange(idx1: int, idx2: int):
    global line
    line[idx1], line[idx2] = line[idx2], line[idx1]


def partner(val1: str, val2: str):
    global line
    idx1 = line.index(val1)
    idx2 = line.index(val2)
    line[idx1], line[idx2] = line[idx2], line[idx1]


def dance(instrs: list):
    for x in instrs:
        instr = x[0]
        if instr == 's':
            spin(int(x[1:]))
        elif instr == 'x':
            a, b = map(int, x[1:].split('/'))
            exchange(int(a), int(b))
        elif instr == 'p':
            partner(x[1], x[3])
        else:
            raise ValueError(f'Invalid instruction code: {instr}')


if __name__ == '__main__':
    length = 16
    start = ord('a')
    line = [chr(x) for x in range(start, start + length)]
    line_init = line[:]
    print('Initial order: ' + ''.join(line))

    instr_set = []
    with open('./dance.txt') as file:
        instr_set = file.read().strip().split(',')

    # PART 1
    dance(instr_set)
    print('Pt 1 final order: ' + ''.join(line), end='\n\n')

    # PART 2
    # Confession: I had to read other people's answers to understand how this problem is solved. I'm doing it with two
    # optimizations: A memoized dance solver using `dance_memo` and a cycle finder using `cycle`. [NOTE] I'm assuming
    # a cycle is an integer multiple of dances. If the cycle is a multiple of instructions but not a multiple of dances,
    # the code becomes a bit more complex, but it's still feasible.

    dance_memo = {}  # k: starting permutation, v: final permutation
    cycle = [''.join(line_init), ''.join(line)]  # permutations already seen in Pt 1
    key = ''.join(line)
    for i in range(int(1e9) - 1):
        if key in dance_memo:
            line = dance_memo[key]
        else:
            dance(instr_set)
            dance_memo[key] = line

        key = ''.join(line)
        if key in cycle:  # Cycle found. This # of dances returns the string back to its original state.
            break
        cycle.append(key)
    print(f'Cycle found with length {len(cycle)}')

    line = line_init
    for i in range(int(1e9) % len(cycle)):
        if key in dance_memo:
            line = dance_memo[key]
        else:
            dance(instr_set)
            dance_memo[key] = line

    print('Pt 2 final order: ' + ''.join(line))
