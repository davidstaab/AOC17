from collections.abc import Sequence, Mapping, Iterator, Iterable
from collections import namedtuple
from types import GeneratorType
from io import TextIOBase


class HexPoint(Iterator):
    """
    Implements a point on a hexagonal movement grid. Works with axial (q, r) or cuboid (x, y, z) coordinate systems.
    Uses Manhattan distance and movement calculations in its operators.

    When iterating over this object, cuboid coordinates are returned.
    """

    class CoordError(ValueError):

        def __init__(self, *args):
            self.args = args

        def __str__(self):
            return 'Invalid triple: {}, {}, {}'.format(
                self.args[0],
                self.args[1],
                self.args[2],
            )

    __slots__ = [
        'q',
        'r',
        'it',
    ]

    AxialDir = namedtuple('AxialDir', ['q', 'r'])
    direcs_a = {
        #       q,  r
        #       x,  z,  y = -x - z
        'ne': AxialDir( 1, -1),
        'n':  AxialDir( 0, -1),
        'nw': AxialDir(-1,  0),
        'sw': AxialDir(-1,  1),
        's':  AxialDir( 0,  1),
        'se': AxialDir( 1,  0),
    }

    def __init__(self, *args):
        """
        Creates a HexPoint using coordinates provided as a Sequence, Mappping, or Generator. At least 2 coordinate
        values must be provided, i.e. (q, r), (x, y, z).
        :param coords:
        """
        self.it = 0

        # Unpack args, if necessary
        if isinstance(args[0], (Sequence, Mapping)):
            coords = args[0]
        else:
            coords = args

        # Extract coords from arg and assign to self
        if isinstance(coords, Sequence):
            if len(coords) == 2:
                self.q = int(coords[0])
                self.r = int(coords[1])
            else:
                if not sum(coords) == 0:
                    raise HexPoint.CoordError(coords)
                self.q = int(coords[0])
                self.r = int(coords[2])
        elif isinstance(coords, Mapping):
            if len(coords) == 3:
                if not sum(coords.values()) == 0:
                    raise HexPoint.CoordError(coords.values())
            try:
                self.q = int(coords['q'])
                self.r = int(coords['r'])
            except NameError:
                try:
                    self.q = int(coords['x'])
                    self.r = int(coords['z'])
                except NameError:
                    raise
        elif isinstance(coords, GeneratorType):
            try:
                items = [_ for _ in coords]
                if len(items) == 2:
                    self.q = int(items[0])
                    self.r = int(items[1])
                else:
                    self.q = int(items[0])
                    self.r = int(items[2])
            except IndexError:
                raise ValueError('Generator did not output at least 2 coordinates.')
        else:
            raise ValueError('Unrecognized initialization object type: {}'.format(type(coords)))

    @property
    def x(self):
        return self.q

    @property
    def y(self):
        return -self.q - self.r

    @property
    def z(self):
        return self.r

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def __repr__(self):
        return 'HexPoint<q/x={}, r/z={}>'.format(self.q, self.r)

    def __iter__(self):
        return self

    def __next__(self):
        vals = (self.x, self.y, self.z)
        if self.it >= len(vals):
            raise StopIteration
        else:
            ret = vals[self.it]
            self.it += 1
            return ret

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplementedError('Expecting both arguments of type {}'.format(type(self)))
        else:
            return HexPoint([a1 + a2 for a1, a2 in zip(self, other)])

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplementedError('Expecting both arguments of type {}'.format(type(self)))
        else:
            return HexPoint([a1 - a2 for a1, a2 in zip(self, other)])

    def step(self, direc: (str, object)):
        """
        Move one step in the given direction. Modifies self in-place.
        :param direc: One of the values of HexPoint.direcs_a or another HexPoint instance
        """
        if isinstance(direc, str):
            self.q = self.q + HexPoint.direcs_a[direc].q
            self.r = self.r + HexPoint.direcs_a[direc].r
        elif isinstance(direc, HexPoint):
            self.q = self.q + direc.q
            self.q = self.q + direc.r
        else:
            return ValueError('Invalid argument type: {}. Expected str or HexPoint.'.format(type(direc)))


def manhattan_dist(a: HexPoint, b: HexPoint = None) -> int:
    """
    Distance between two HexPoints or, if only one point is given, distance to that point from the grid's origin
    """
    if b is None:
        return max(abs(a.x), abs(a.y), abs(a.z))
    return max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z))


def word_reader_factory(source):
    if isinstance(source, TextIOBase):
        def reader():
            while 1:  # until end of source
                w = ''
                while 1:  # until word delimeter or EOF
                    c = source.read(1)
                    if c in ['', None]:
                        return
                    elif c in [',', '\r', '\n']:
                        yield w
                        break
                    else:
                        w += c
    elif isinstance(source, Iterable):
        def reader():
            for i in source:
                yield i
    else:
        raise ValueError('Invalid argument type: {} Must be TextIOBase or Iterable.'.format(type(source)))
    return reader


if __name__ == '__main__':

    ### TESTS ###
    print('HexPoint tests:')
    print('(1, 0, -1) + (1, 1, -2) = ' + str(HexPoint(1, 0, -1) + HexPoint(1, 1, -2)))

    test_cases = [
        ['ne', 'ne', 'ne'],
        ['ne', 'ne', 'sw', 'sw'],
        ['ne', 'ne', 's', 's'],
        ['se', 'sw', 'se', 'sw', 'sw'],
    ]
    for test in test_cases:
        print('Test case: {}'.format(test), end='\t\t\t')
        read_word = word_reader_factory(test)
        pt = HexPoint(0, 0, 0)
        for w in read_word():
            pt.step(w)
        print('Final location: {}'.format(pt), end='\t')
        print('Distance to location: {}'.format(manhattan_dist(pt)))
    #############

    print('\nActual problem:')
    with open('./hex_steps.txt') as file:
        read_word = word_reader_factory(file)
        pt = HexPoint(0, 0, 0)
        max_dist = 0
        for w in read_word():
            pt.step(w)
            max_dist = max(max_dist, manhattan_dist(pt))
        print('Final location: {}'.format(pt), end='\t')
        print('Distance to location: {}'.format(manhattan_dist(pt)))
        print('Farthest from origin during path navigation: {}'.format(max_dist))
