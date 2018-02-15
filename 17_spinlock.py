from proj import kh

incr = 343

# TEST PARAMS
# input = 3
# insertions = 5
############

buf = kh.CircularBuffer([0])

if __name__ == '__main__':
    i = 0
    insertions = 2017
    for x in range(1, insertions + 1):
        i += incr
        i = buf.insert(i + 1, x) % len(buf)
    print(f'Pt 1: Interesting values: {buf[i]}, {buf[i + 1]}')

    # Part 2: I don't need the list any more, since I'm just looking for the last value inserted to index 1 (the slot
    #  after the value `0`). Now I just need the mathematical properties of the growing buffer.
    i = 0
    ct = 1
    val_1 = 0
    insertions = int(50e6)
    for x in range(1, insertions + 1):
        i = (i + incr) % ct
        # insertion after `i` would occur here
        if i == 0:
            val_1 = x
        ct += 1
        i = (i + 1) % ct
    print(f'Pt 2: Value at index 1 after {insertions} insertions: {val_1}')
