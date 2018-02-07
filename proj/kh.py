from collections.abc import MutableSequence, Iterable


class CircularBuffer(MutableSequence):
    """
    A list with its ends tied together like an oroborous. Indexing never raises IndexError. Slicing can start at any
    index.
    """

    def __init__(self, data_source: Iterable):
        if isinstance(data_source, Iterable):
            self._coll = [_ for _ in data_source]
        else:
            raise ValueError('data_source does not implement __iter__.')

    def insert(self, index, obj):
        self._coll.insert(self.__idx(index), obj)

    def __idx(self, index: int) -> int:
        """
        Guarantees no 'index out of range' errors by mapping index into legal range.
        """
        return index % len(self._coll)

    def __slice(self, key: slice) -> slice:
        """
        Validates necessary assumptions about a slice, then maps the `start` and `stop` indices into the bounds of the
        collection.
        """
        _s = len(self._coll)
        if not (key.step == 1 or key.step is None):
            raise NotImplementedError('Step size > 1')

        if key.start is None or key.stop is None:
            start = 0 if key.start is None else key.start
            stop = _s if key.stop is None else key.stop
        else:
            if key.stop < key.start:
                raise IndexError(
                    'Stop must be greater or equal to Start. Add len(self) to Stop if slice should wrap buffer.'
                )
            if key.stop - key.start > _s:
                raise IndexError('Slice span is longer than the collection.')
            span = key.stop - key.start
            start = key.start % _s
            stop = start + span

        # Map slice bounds into range of [0 : 2*len - 1]
        return slice(start, stop, key.step)

    def __getitem__(self, key):
        """
        Allows indices beyond range of buffer.
        """
        if isinstance(key, slice):
            _s = len(self._coll)
            key = self.__slice(key)
            if key.stop >= _s:
                split = key.stop - _s
                return self._coll[key.start:] + self._coll[:split]
            else:
                return self._coll[key.start:key.stop]
        return self._coll[self.__idx(key)]

    def __setitem__(self, key, value):
        """
        Allows indices beyond range of buffer.
        """
        if isinstance(key, slice):
            val = [_ for _ in value]  # convert non-subscriptable type to subscriptable type
            _s = len(self._coll)
            key = self.__slice(key)
            if key.stop >= _s:
                split = _s - key.start
                self._coll[key.start:] = val[:split]
                self._coll[:key.stop - _s] = val[split:]
            else:
                self._coll[key.start:key.stop] = val
        else:
            self._coll[self.__idx(key)] = value

    def __delitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError  # todo
        del(self._coll[self.__idx(key)])

    def __len__(self):
        return len(self._coll)

    def __repr__(self):
        extra = '...' if len(self._coll) > 20 else ''
        return '<CircularBuffer object {}'.format(self._coll[:20]) + extra + '>'

    def __str__(self):
        return str(self._coll)


class KnotHash:
    """
    A CircularBuffer interface that follows the rules of Exercise 10 with respect to pointer incrementation and the use
    of a skip value
    """

    salt = [17, 31, 73, 47, 23]
    rounds = 64

    def knot1(self, length: int):
        sub = self._buf[self._ptr: self._ptr + length]
        sub.reverse()
        self._buf[self._ptr: self._ptr + length] = sub

        self._ptr += length + self._skip
        self._skip += 1

    def knot_all(self, lengths: Iterable):
        if isinstance(lengths, str):
            lengths = [ord(c) for c in lengths]  # interpret at ASCII
        lengths += self.salt
        for _ in range(self.rounds):
            for length in lengths:
                self.knot1(length)

    def __init__(self, lengths: Iterable=None):
        self._buf = CircularBuffer(range(256))
        self._ptr = 0
        self._skip = 0

        if lengths is not None:
            self.knot_all(lengths)

    def dense_hash(self, block_size: int) -> list:
        hash_size = int(len(self._buf) / block_size)
        dense_hash = []
        for i in range(hash_size):
            block_start = i * block_size
            dense_hash.append(self._buf[block_start: block_start + block_size])
        for i, block in enumerate(dense_hash):
            hash_val = block[0]
            for j in block[1:]:
                hash_val ^= j
            dense_hash[i] = hash_val
        return dense_hash

    def sparse_hash(self) -> list:
        return self._buf[:]


def dh_hex(dense_hash: list) -> str:
    """
    Format a `dense_hash` (list) into a hex string
    """
    return ''.join(f'{v:02X}' for v in dense_hash)


def dh_bin(dense_hash: list) -> str:
    """
    Format a `dense_hash` (list) into a binary string
    """
    return ''.join(f'{v:0>8b}' for v in dense_hash)
