import re


def spin(count: int):
    global line
    line = line[-count:] + line[:-count]


def exchange(idx1: int, idx2: int):
    global line
    t = line[idx1]
    line[idx1] = line[idx2]
    line[idx2] = t


def partner(val1: str, val2: str):
    global line
    idx1 = line.index(val1)
    idx2 = line.index(val2)
    exchange(idx1, idx2)


def dance(x: str):
    instr = x[0]
    if instr == 's':
        spin(int(x[1:]))
    elif instr == 'x':
        a, b = re.findall('[0-9]+', x[1:])  # use re to find multi-digit arguments
        exchange(int(a), int(b))
    elif instr == 'p':
        partner(x[1], x[3])
    else:
        raise ValueError(f'Invalid instruction code: {instr}')


if __name__ == '__main__':
    length = 16
    start = ord('a')
    line = [chr(x) for x in range(start, start + length)]
    print('Initial order: ' + ''.join(line))

    instr_set = []
    with open('./dance.txt') as file:
        instr_set = file.read().strip().split(',')

    # PART 1
    for x in instr_set:
        dance(x)
    print('Pt 1 final order: ' + ''.join(line))

    # PART 2
    # Confession: This problem falls into the domain of group theory in mathematics, which is way beyond my
    # understanding of algebra. I'm going to implement the solution detailed here to practice coding:
    # https://www.reddit.com/r/adventofcode/comments/7k5mrq/spoilers_in_title2017_day_16_part_2_cycles/drcd8vj/
    memo = {}  # k: starting permutation, v: final permutation
    memo_acc_ct = 0
    for i in range(int(1e9 - 1)):
        if i % int(1e6) == 0:
            print(f'Iteration {i} - {memo_acc_ct} memo accesses - memo size {len(memo)}')
        key = ''.join(line)
        if key in memo:
            # skip instructions, just grab result from memo
            memo_acc_ct += 1
            line = memo[key]
        else:
            for x in instr_set:
                dance(x)
            # add result to memo
            memo[key] = line
    print('Pt 2 final order: ' + ''.join(line))
    print(f'{memo_acc_ct} total memo accesses - Final memo size {len(memo)}')
