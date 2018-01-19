from math import floor
import numpy as np
from collections import Iterable

loc = 347991


# CALCS FOR PART 1


# The spiral comprises a square of filled memory locations and a tail wrapping around it. The number of locs in the
# square is its edge length (its dimension) ^ 2. The tail is the difference of the current location and the square's
# area.
sq_dim = floor(pow(loc, 0.5))
filled_ct = sq_dim * sq_dim
tail_ct = loc - filled_ct
# The tail wraps around the square. Its bends occur once every [square dimension + 1]. (The '+1' gets around the
# corner of the square.) There's a remainder that's shorter than the square's dimension.
tail_rem = tail_ct % (sq_dim + 1)
# The remainder of the tail starts alongside the edge of the square. The square has an odd-valued dimension, and the
# distance from the corner to the edge's midpoint is [(dim - 1) / 2]. The tail under- or over-hangs the midpoint by
# some length.
corner_to_midpt = int((sq_dim - 1) / 2)
dist_to_midpt = corner_to_midpt - tail_rem
# The distance from the midpoint to the center of the square is the same as the corner-to-midpoint distance.
total_steps = abs(dist_to_midpt) + corner_to_midpt


# TOOLS FOR PART 2


def init_grid(initial_val: int, *args, **kwargs) -> (np.matrix, object):
    """
    Initializes a grid with `initial_val` and provides ... #todo
    :return: `grid` (a NumPy matrix) and ... #todo
    """

    grid = np.matrix(np.zeros(*args, **kwargs))
    center_offset = []
    for dim in grid.shape:
        center_offset.append(floor(dim / 2))
    center_offset = tuple(center_offset)

    def _idx2coord(indices: Iterable) -> tuple:
        """
        Reverse of `_coord2idx`. Turns a list of index arrays back into a tuple of coordinates using `center_offset`.
        :param indices: A list of np.array containing index arrays
        :return: A coordinate pair
        """
        return tuple([int(x1) - x2 for x1, x2 in zip(indices, center_offset)])

    def _coord2idx(*cargs) -> list:
        """
        A coordinate-based indexer for the grid returned by `init_grid()`.
        :return: A list of numpy index arrays pointing to that coordinate position in the 0-centered grid
        """

        # Catch and convert a list or tuple argument. God help them if they pass a string or other non-numeric iterable.
        if isinstance(cargs[0], Iterable):
            cargs = cargs[0]
        translated = [sum(x) for x in zip(cargs, center_offset)]
        return [np.array(x) for x in translated]

    def _sum_neighbors(mat: np.matrix, indices: np.array) -> int:
        """
        Sums the 8 neighboring values for a given index in the grid array
        :param mat: The grid (an np.matrix) to work on
        :param indices: A list of indices, probably returned by `_coord2idx()`
        :return: The summed values of the neightboring cells
        """

        # todo: Known bug - can request indices out of range of `mat`

        # Current value at `indices` is 0, so we can just sum the entire 9-grid around that cell
        idx_ranges = [np.arange(x[0] - 1, x[0] + 2) for x in indices]
        neighbors = mat[idx_ranges[0], :][:, idx_ranges[1]]
        return int(np.sum(neighbors))

    def spiral(mat: np.matrix, verbose: bool=False):
        """
        Generator. Yields the indices of the next cell in the spiral pattern and the value to write there.
        :return:
        """

        def _print_coord(idx):
            if verbose:
                print(_idx2coord(idx))

        start = (0, 0)
        lrot = np.matrix([[0, -1], [1, 0]])  # Left-rotation matrix
        vector = np.matrix([[1], [0]])  # Step vector for finding next cell
        curr_idx = np.matrix(_coord2idx(start)).transpose()  # Convert to indices, then to column vector

        while 1:
            layer = max(_idx2coord(curr_idx))  # Largest dimension defines current layer, thanks to square shape
            corners_idx = [
                np.matrix(_coord2idx(layer, layer)).transpose(),
                np.matrix(_coord2idx(-layer, layer)).transpose(),
                np.matrix(_coord2idx(-layer, -layer)).transpose(),
                np.matrix(_coord2idx(layer, -layer)).transpose(),  # Ordered! Last item is final square in layer
            ]
            is_corner = [np.array_equiv(curr_idx, i) for i in corners_idx]
            if any(is_corner):
                if is_corner[3]:
                    # go straight, calculate/store val, and then turn
                    curr_idx += vector
                    _print_coord(curr_idx)
                    val = _sum_neighbors(mat, curr_idx)
                    mat[int(curr_idx[0]), int(curr_idx[1])] = val
                    yield val
                    vector = lrot * vector
                else:
                    # turn, go straight, and then calculate/store val
                    vector = lrot * vector
                    curr_idx += vector
                    _print_coord(curr_idx)
                    val = _sum_neighbors(mat, curr_idx)
                    mat[int(curr_idx[0]), int(curr_idx[1])] = val
                    yield val
            else:
                # go straight and then calculate/store val
                curr_idx += vector
                _print_coord(curr_idx)
                val = _sum_neighbors(mat, curr_idx)
                mat[int(curr_idx[0]), int(curr_idx[1])] = val
                yield val

    grid[_coord2idx(0, 0)] = initial_val
    return grid, spiral


if __name__ == '__main__':
    # PART 1
    print('Filled square dimension: {}\nLocations in filled square: {}'.format(sq_dim, filled_ct))
    print('Locations in tail: {}\nRemainder of tail: {}'.format(tail_ct, tail_rem))
    print('Steps from edge\'s corner to midpoint: {}\nDistance to midpoint: {}'.format(corner_to_midpt, dist_to_midpt))
    print('Steps from location to access port: {}'.format(total_steps))
    print('\n')

    # PART 2
    mem, walk_spiral = init_grid(1, (11, 11), dtype=int)

    # Generator will run forever. Constrain it to size of `mem`.
    cell = walk_spiral(mem, verbose=False)
    for i in range(mem.size - 1):
        val = next(cell)
        print(val)
        if val > loc:
            break
    # print(mem)
