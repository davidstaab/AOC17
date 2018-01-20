# grab current value
# increment value
# jump by grabbed value
# increment step counter

if __name__ == '__main__':

    # PART 1
    steps = 0
    with open('jumps.txt') as file:
        jumps = [int(x) for x in file.readlines()]
        i = 0
        while i < len(jumps):
            j = jumps[i]
            jumps[i] += 1
            i += j
            steps += 1
    print('Part 1: Steps taken: {}'.format(steps))

    # PART 2
    steps = 0
    with open('jumps.txt') as file:
        jumps = [int(x) for x in file.readlines()]
        i = 0
        while i < len(jumps):
            j = jumps[i]
            jumps[i] = jumps[i] + 1 if j < 3 else jumps[i] - 1
            i += j
            steps += 1
    print('Part 2: Steps taken: {}'.format(steps))
