from proj import kh


if __name__ == '__main__':

    # PART 1
    p = kh.KnotHash(256)
    with open('./knot_lengths.txt') as file:
        lengths = [int(x) for x in file.read().strip().split(sep=',')]

        for length in lengths:
            p.knot(length)

    val1 = p.values[0]
    val2 = p.values[1]
    print('Part 1:')
    print('First two numbers in list: {}, {}'.format(val1, val2))
    print('Their product: {}'.format(val1 * val2))

    # PART 2
    p = kh.KnotHash(256)
    seq_end = [17, 31, 73, 47, 23]
    rounds = 64
    with open('./knot_lengths.txt') as file:
        lengths = [ord(c) for c in file.read().strip()]  # interpret chars in file as ASCII
        lengths += seq_end
        for _ in range(rounds):
            for length in lengths:
                p.knot(length)

    print('\nPart 2:')
    print('Dense hash: {}'.format(kh.dh_hex(p.dense_hash(block_size=16))))
