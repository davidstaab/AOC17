import numpy as np

ud = '|'
lr = '-'
tn = '+'
end = ' '


def find_start(maze: np.ndarray) -> tuple:
    """
    Find the start of the maze.
    :return: `cursor`: index of start, `direction`: tuple of offsets for next position along maze path
    """
    start = np.where(maze[0] == '|')[0]  # `where` returns a tuple containing the ndarray for some dumb reason
    if start.size < 1:
        start = np.where(maze[...:0] == '-')[0]
        if start.size < 1:
            raise ValueError('Could not find the starting point on the top or left edges.')
        else:
            cursor = (start[0], 0)
            direction = (0, 1)
    else:
        cursor = (0, start[0])
        direction = (1, 0)
    return cursor, direction


def step(cursor: tuple, direction: tuple) -> tuple:
    """
    Advance `cursor` in `direction`
    """
    return tuple(a + b for a, b in zip(cursor, direction))


def turn(maze: np.ndarray, cursor: tuple, direction: tuple) -> tuple:
    dirs = [(-1, 0), (1, 0)] if direction[0] == 0 else [(0, -1), (0, 1)]
    for d in dirs:
        if maze[step(cursor, d)][0] != end:
            return d
    raise IndexError(f'Could not find a valid turn from position {cursor}')


if __name__ == '__main__':
    n = []
    with open('./tubes.txt') as file:
        n = [[c for c in r.rstrip('\r\n')] for r in file.readlines()]

        # Pad the grid back to a rectangle if git or a text editor has trimmed its rows to minimize the file size
        full_width = max([len(r) for r in n])
        for i, r in enumerate(n):
            w = len(r)
            if w < full_width:
                n[i] += [_ for _ in ' ' * (full_width - w)]
    maze = np.array(n, dtype=str)
    del n

    cursor, direction = find_start(maze)
    phrase = ''
    steps = 0
    while 1:
        char = maze[cursor][0]
        if char == end:
            break
        elif char == tn:
            direction = turn(maze, cursor, direction)
            cursor = step(cursor, direction)
            steps += 1
        else:
            if char not in (ud, lr):
                phrase += char
            cursor = step(cursor, direction)
            steps += 1
    print(f'Part 1: {phrase}')
    print(f'Part 2: {steps} steps')
