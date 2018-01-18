from math import floor
import numpy as np

loc = 347991

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


def init_grid(*args, **kwargs) -> (list, object):
    """
    Initializes a grid and provides a function for indexing it using coordinates from the center point. The center point
    is coordinate (0, 0, ..., 0)
    :return: `grid` (a NumPy array) and `indexer` (a coordinate-mapping function)
    """
    _grid = np.zeros(*args, **kwargs)
    center_offset = []
    for dim in _grid.shape:
        center_offset.append(floor(dim / 2))
    center_offset = tuple(center_offset)

    def indexer(*cargs) -> list:
        """
        A coordinate-based indexer for the grid returned by `init_grid()`. Coordinates should be provided as individual,
        ordered arguments; not as a list or tuple.
        :return: A list of numpy index arrays pointing to that coordinate position
        """
        translated = [sum(x) for x in zip(cargs, center_offset)]
        return [np.array(x) for x in translated]  # Convert to numpy index arrays

    return _grid, indexer


grid, coords = init_grid((11, 11))
val = 1
while val <= loc:
    grid[coords(1, 0)] = 1

print(grid)
