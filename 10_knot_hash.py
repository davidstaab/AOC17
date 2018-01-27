from collections.abc import MutableSequence


class PieceOfString(MutableSequence):
    """
    A list with its ends tied together like an oroborous. Indexing never raises IndexError.
    """

    @staticmethod
    def __slice_bounds(key: slice, length: int):
        """
        Validates these assumptions about a slice:
         * `key.start` will be in [-len+1:len]
         * `key.stop` will be in [0:2*len]
         * `key.stop` - `key.start` will be <= len
        """
        if key.step is not None:
            if not 0 <= key.step <= 1:
                raise IndexError('Sorry, can\'t handle step {}. Too hard.'.format(key.step))
        if key.start is not None:
            if not 1 - length < key.start < length:
                raise IndexError('Can\'t unwrap list that far. Too hard.')
            if key.stop is not None:
                if key.stop < key.start:
                    raise IndexError('End of range must be greater or equal to Start.')
                if key.stop - key.start > length:
                    raise IndexError('Slice span is longer than the collection.')
        if key.stop is not None:
            if not 0 < key.stop < 2 * length:
                raise IndexError('Can\'t unwrap list that far. Too hard.')

    def __init__(self, length: int):
        self._string = [_ for _ in range(length)]
        self._ptr = 0
        self._skip = 0

    def knot(self, length: int):
        # Note: Don't work on `self._string`! Work on `self` so data method overrides are put to use.
        # (Using own public interface is a code smell. Should put this method in an encapsulating class. Oh, well.)
        self[self._ptr : self._ptr + length] = reversed(self[self._ptr : self._ptr + length])
        self._ptr += length + self._skip
        self._skip += 1

    def insert(self, index, obj):
        self._string.insert(self.__idx(index), obj)

    def __idx(self, index: int) -> int:
        _s = len(self._string)
        if index >= 0:
            return index if index < _s else index - _s
        else:
            return index if abs(index) <= _s else index + _s

    def __getitem__(self, key):
        """
        Allows indices beyond range of buffer. Can also return spans longer than buffer, instead of truncating span as
        default slicing behavior does.
        """
        if isinstance(key, slice):
            _s = len(self._string)
            self.__slice_bounds(key, _s)
            if key.stop >= _s:
                new_stop = key.stop - _s
                return self._string[key.start:] + self._string[:new_stop]
            else:
                if key.start < 0:
                    return self._string[key.start:] + self._string[:key.stop]
                else:
                    return self._string[key.start:key.stop]
        return self._string[self.__idx(key)]

    def __setitem__(self, key, value):
        val = [_ for _ in value]  # convert possibly non-subscriptable type to definitely subscriptable type
        if isinstance(key, slice):
            _s = len(self._string)
            self.__slice_bounds(key, _s)
            if key.stop >= _s:
                split = _s - key.start
                self._string[key.start:] = val[:split]
                self._string[:key.stop - _s - 1] = val[split:]
            else:
                if key.start < 0:
                    split = len(val) + key.start
                    self._string[key.start:] = val[:split]
                    self._string[:key.stop] = val[split:]
                else:
                    self._string[key.start:key.stop] = val
        else:
            self._string[self.__idx(key)] = val

    def __delitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError  # todo
        del(self._string[self.__idx(key)])

    def __len__(self):
        return len(self._string)

    def __str__(self):
        return str(self._string)


if __name__ == '__main__':

    # p = PieceOfString(256)
    p = PieceOfString(5)  # todo: TEST CODE replaces above line

    with open('./knot_lengths.txt') as file:
        # lengths = [int(x) for x in file.read().strip().split(sep=',')]
        lengths = [3, 4, 1, 5]  # todo: TEST CODE replaces above line
        for length in lengths:
            p.knot(length)

    # print('First two numbers in list: {}, {}'.format(p[0], p[1]))
    print(p)  # todo: TEST CODE replaces above line
    print('Their product: {}'.format(p[0] * p[1]))
