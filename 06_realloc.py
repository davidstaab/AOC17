# 16 banks
# N blocks / bank
# cycle:
# 	find bank with most blocks (lower index wins tie)
# 	remove all blocks from bank
# 	add blocks one-by-one to banks, starting with next-index and wrapping until done
# 	store hash of final configuration.
# 	if hash is non-unique, break
# how many cycles?


def incr(i: int, ct: int) -> int:
    i += 1
    return i if i < ct else 0


if __name__ == '__main__':

    with open('./memory_banks.txt') as file:
        banks = [int(x) for x in file.read().split()]

        configs = [hash(tuple(banks))]

        while 1:
            fullest_idx = banks.index(max(banks))
            blocks = banks[fullest_idx]
            banks[fullest_idx] = 0
            idx = fullest_idx
            while blocks > 0:
                idx = incr(idx, len(banks))
                blocks -= 1
                banks[idx] += 1
            config = hash(tuple(banks))
            if config in configs:
                break
            configs.append(config)
        print('Steps to infinite loop: {}'.format(len(configs)))
