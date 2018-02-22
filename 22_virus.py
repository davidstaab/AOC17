# Note: I wrote this using sets and tuples because it looks like memory was going to be more valuable (on a
# "near-infinite grid") than CPU. Also, pt. 1 only needed a boolean flag for each location. Whoops. It would probably
#  be optimized for part 2 by defining the grid and locations using NumPy arrays for in-place access and trivial
#  addition functions. The array could hold 4-bit values, or just strings if that's fast enough.

# define all these names so debugging is easier
left = (0, -1)  # dec col
up = (-1, 0)    # dec row
down = (1, 0)   # inc row
right = (0, 1)  # inc col

turn = {
    left: {
        'L': down,
        'R': up,
    },
    up: {
        'L': left,
        'R': right,
    },
    right: {
        'L': up,
        'R': down,
    },
    down: {
        'L': right,
        'R': left,
    },
}


def tuple_add(t: tuple, o) -> tuple:
    if isinstance(o, (list, tuple)):
        return tuple(a + b for a, b in zip(t, o))
    elif isinstance(o, (int, float)):
        return tuple(a + o for a in t)


if __name__ == '__main__':
    width, height = -1, -1
    infected = set()
    with open('./grid.txt') as file:
        for i, line in enumerate(file):
            height = i + 1
            width = len(line.rstrip())
            for j, c in enumerate(line.rstrip()):
                if c == '#':
                    infected.add((i, j))

    cur = (int(width / 2), int(height / 2))  # int() rounds down, which works with 0-indexing
    step = up

    # TEST INPUTS
    # infected = {(0, 2), (1, 0)}
    # cur = (1, 1)
    # step = up

    # PART 1
    infected_init = infected.copy()
    cur_init = cur
    step_init = step
    new_infections = 0
    for _ in range(10000):
        if cur in infected:
            step = turn[step]['R']
            infected.remove(cur)
        else:
            step = turn[step]['L']
            infected.add(cur)
            new_infections += 1
        cur = tuple_add(cur, step)
    print(f'Part 1: {new_infections} new infections')

    # PART 2
    infected = infected_init
    weakened, flagged = set(), set()
    cur = cur_init
    step = step_init
    new_infections = 0
    for _ in range(int(10e6)):
        if cur in infected:
            step = turn[step]['R']
            infected.remove(cur)
            flagged.add(cur)
        elif cur in weakened:
            # do not turn
            weakened.remove(cur)
            infected.add(cur)
            new_infections += 1
        elif cur in flagged:
            step = turn[step]['R']
            step = turn[step]['R']
            flagged.remove(cur)
        else:
            step = turn[step]['L']
            weakened.add(cur)
        cur = tuple_add(cur, step)
    print(f'Part 2: {new_infections} new infections')
