from collections.abc import MutableSequence


class PieceOfString(MutableSequence):
    """
    A list with its ends tied together like an oroborous. Indexing never raises IndexError.
    """

    def __init__(self, length: int):
        self._string = [_ for _ in range(length)]
        self._ptr = 0
        self._skip = 0

    def knot(self, length: int):
        # Note: Don't work on `self._string`! Work on `self` so data method overrides are put to use.
        # (Using own public interface is a code smell. Should put this method in an encapsulating class. Oh, well.)
        sub = self[self._ptr : self._ptr + length]
        sub.reverse()
        self[self._ptr: self._ptr + length] = sub

        self._ptr += length + self._skip
        self._skip += 1

    def insert(self, index, obj):
        self._string.insert(self.__idx(index), obj)

    def __idx(self, index: int) -> int:
        """
        Guarantees no 'index out of range' errors by mapping index into legal range.
        """
        return index % len(self._string)

    def __slice(self, key: slice) -> slice:
        """
        Validates necessary assumptions about a slice, then maps the `start` and `stop` indices into the bounds of the
        collection.
        """
        _s = len(self._string)
        if key.step is not None:
            if not 0 <= key.step <= 1:
                raise NotImplementedError('Step size > 1')
        if key.start is not None and key.stop is not None:
            if key.stop < key.start:
                raise IndexError('Stop must be greater or equal to Start.')
            if key.stop - key.start > _s:
                raise IndexError('Slice span is longer than the collection.')

        # Map slice bounds into range of [0 : 2*len - 1]
        span = key.stop - key.start
        start = key.start % _s
        stop = start + span
        return slice(start, stop, key.step)

    def __getitem__(self, key):
        """
        Allows indices beyond range of buffer.
        """
        if isinstance(key, slice):
            _s = len(self._string)
            key = self.__slice(key)
            if key.stop >= _s:
                split = key.stop - _s
                return self._string[key.start:] + self._string[:split]
            else:
                return self._string[key.start:key.stop]
        return self._string[self.__idx(key)]

    def __setitem__(self, key, value):
        """
        Allows indices beyond range of buffer.
        """
        if isinstance(key, slice):
            val = [_ for _ in value]  # convert non-subscriptable type to subscriptable type
            _s = len(self._string)
            key = self.__slice(key)
            if key.stop >= _s:
                split = _s - key.start
                self._string[key.start:] = val[:split]
                self._string[:key.stop - _s] = val[split:]
            else:
                self._string[key.start:key.stop] = val
        else:
            self._string[self.__idx(key)] = value

    def __delitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError  # todo
        del(self._string[self.__idx(key)])

    def __len__(self):
        return len(self._string)

    def __str__(self):
        return str(self._string)


if __name__ == '__main__':

    p = PieceOfString(256)

    with open('./knot_lengths.txt') as file:
        lengths = [int(x) for x in file.read().strip().split(sep=',')]
        for length in lengths:
            p.knot(length)

    print('First two numbers in list: {}, {}'.format(p[0], p[1]))
    print('Their product: {}'.format(p[0] * p[1]))
