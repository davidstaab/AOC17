from math import floor
import numpy as np

loc = 347991

# TOOLS FOR PART 2


def init_grid(initial_val: int, *args, **kwargs) -> (np.matrix, object):
    """
    Initializes a grid with `initial_val` and provides a generator function for calculating each next value.
    :return: `grid` (a NumPy array) and `calculator` (a generator for each next value)
    """

    grid = np.matrix(np.zeros(*args, **kwargs))
    center_offset = []
    for dim in grid.shape:
        center_offset.append(floor(dim / 2))
    center_offset = tuple(center_offset)

    def coord2idx(*cargs) -> list:
        """
        A coordinate-based indexer for the grid returned by `init_grid()`. Coordinates should be provided as individual,
        ordered arguments; not as a container object.
        :return: A list of numpy index arrays pointing to that coordinate position in the 0-centered grid
        """
        translated = [sum(x) for x in zip(cargs, center_offset)]
        return [np.array(x) for x in translated]

    lrot = np.matrix([[0, -1], [1, 0]])  # Left-rotation matrix
    vector = np.matrix([[1], [0]])  # Step vector for finding next cell
    curr_idx = coord2idx(0, 0)

    def _find_next_cell():
        """
        Generator for use by other functions in this scope. Yields the indices of the next cell in the grid.
        :return:
        """

        nonlocal curr_idx, vector, lrot

        curr_idx = np.matrix(curr_idx).transpose()  # Convert to column vector
        layer = max(curr_idx)  # Largest dimension defines current layer, thanks to square shape
        corners = [
            np.matrix([[layer], [layer]]),
            np.matrix([[-layer], [layer]]),
            np.matrix([[-layer], [-layer]]),
            np.matrix([[layer], [-layer]]),  # Ordered! Last item is final square in layer
        ]

        if curr_idx in corners:
            if curr_idx == corners[3]:
                # go straight, yield new loc, and then turn
                yield curr_idx + vector
                vector = lrot * vector
            else:
                # turn, go straight, and then yield new loc
                vector = lrot * vector
                yield curr_idx + vector
        else:
            # go straight and then yield loc
            yield curr_idx + vector

    def sum_neighbors(indices: list) -> int:
        """
        Sums the 8 neighboring values for a given index in the grid array
        :param indices: A list of indices, probably returned by `coord2idx()`
        :return: The summed values of the neightboring cells
        """
        indices = np.matrix(indices).transpose()  # Convert to column vector



    def calculator(grid: np.array):

        sq_idx = 0
        while True:
            curr_cell = _find_next_cell(grid, curr_cell)
            val = sum_neighbors(curr_cell)
            grid[coord2idx(curr_cell)] = val
            yield val

    grid[coord2idx(0, 0)] = initial_val
    return grid, calculator


if __name__ == '__main__':
    # PART 1

    # The spiral comprises a square of filled memory locations and a tail wrapping around it. The number of locs in the
    # square is its edge length (its dimension) ^ 2. The tail is the difference of the current location and the square's
    # area.
    sq_dim = floor(pow(loc, 0.5))
    filled_ct = sq_dim * sq_dim
    tail_ct = loc - filled_ct
    print('Filled square dimension: {}\nLocations in filled square: {}'.format(sq_dim, filled_ct))

    # The tail wraps around the square. Its bends occur once every [square dimension + 1]. (The '+1' gets around the corner
    # of the square.) There's a remainder that's shorter than the square's dimension.
    tail_rem = tail_ct % (sq_dim + 1)
    print('Locations in tail: {}\nRemainder of tail: {}'.format(tail_ct, tail_rem))

    # The remainder of the tail starts alongside the edge of the square. The square has an odd-valued dimension, and the
    # distance from the corner to the edge's midpoint is [(dim - 1) / 2]. The tail under- or over-hangs the midpoint by
    # some length.
    corner_to_midpt = int((sq_dim - 1) / 2)
    dist_to_midpt = corner_to_midpt - tail_rem
    print('Steps from edge\'s corner to midpoint: {}\nDistance to midpoint: {}'.format(corner_to_midpt, dist_to_midpt))

    # The distance from the midpoint to the center of the square is the same as the corner-to-midpoint distance.
    total_steps = abs(dist_to_midpt) + corner_to_midpt
    print('Steps from location to access port: {}'.format(total_steps))
    print('\n\n')


    # PART 2

    grid, value = init_grid(1, (11, 11), dtype=int)
    # todo: while loop using generator with a condition to fill grid
    print(grid)
