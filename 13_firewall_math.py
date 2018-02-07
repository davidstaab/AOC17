# A solution for Part 2 of Ex 13 using math instead of simulation.

if __name__ == '__main__':
    fw = []
    with open('./firewall.txt') as file:
        fw = [tuple([int(x) for x in line.split(sep=': ')]) for line in file]

    # Each scanner starts in the "hot seat" where it'll catch the packet. It leaves the seat and returns every integer
    # multiple of 2(`rng` - 1) ps later. The packet reaches the hot seat (`depth` + `delay`) ps after it starts moving.
    # [dstaab] Solve by brute force. Could probably go even more quickly by using linear algebra on the system of
    # equations, but the modulo operator scares me, and I don't want to read a math whitepaper today.
    delay, collided = 0, True
    while collided:
        collided = False
        if delay % 50000 == 0:
            print('Delay = {} ps...'.format(delay))

        delay += 1
        for depth, rng in fw:
            scanner_pos = (depth + delay) % (2 * (rng - 1))
            if scanner_pos == 0:
                collided = True
                break

    print('No collisions with delay {} ps.'.format(delay))
