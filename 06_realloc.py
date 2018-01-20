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

        cycle_len = 0
        recur_len = 0
        did_once = False
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
                if not did_once:
                    cycle_len = len(configs)
                    configs = []
                    did_once = True
                else:
                    recur_len = len(configs)
                    break
            configs.append(config)

        print('Part 1: Steps to infinite loop: {}'.format(cycle_len))
        print('Part 2: Steps to second recurrence: {}'.format(recur_len))

