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

    with open('./dance.txt') as file:
        for x in file.read().strip().split(','):
            dance(x)
    print('Final order: ' + ''.join(line))
