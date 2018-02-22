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
