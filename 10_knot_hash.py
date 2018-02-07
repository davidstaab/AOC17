from proj import kh


if __name__ == '__main__':

    # PART 1
    p = kh.KnotHash()
    with open('./knot_lengths.txt') as file:
        lengths = [int(x) for x in file.read().strip().split(sep=',')]

        for length in lengths:
            p.knot1(length)

    val1 = p.sparse_hash()[0]
    val2 = p.sparse_hash()[1]
    print('Part 1:')
    print('First two numbers in list: {}, {}'.format(val1, val2))
    print('Their product: {}'.format(val1 * val2))

    # PART 2
    p = kh.KnotHash()
    with open('./knot_lengths.txt') as file:
        lengths = file.read().strip()
        p.knot_all(lengths)

    print('\nPart 2:')
    print('Dense hash: {}'.format(kh.dh_hex(p.dense_hash(block_size=16))))
