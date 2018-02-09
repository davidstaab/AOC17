mult_a = 16807
mult_b = 48271
div = 2147483647
start_a = 289
start_b = 629


def gen_pt1(count: int) -> tuple:
    a, b = start_a, start_b
    yield a, b
    for _ in range(count - 1):
        a = (a * mult_a) % div
        b = (b * mult_b) % div
        yield a, b


def gen_pt2(count: int) -> tuple:

    check_a = 4
    check_b = 8

    def get(val: int, multiplier: int, multiple: int) -> int:
        skip = True
        while skip:
            val = (val * multiplier) % div
            skip = val % multiple
        return val

    a, b = start_a, start_b
    if a % check_a == 0 and b % check_b == 0:
        yield a, b
        count -= 1
    for _ in range(count):
        a = get(a, mult_a, check_a)
        b = get(b, mult_b, check_b)
        yield a, b


if __name__ == '__main__':

    # PART 1
    # count = 40000000
    # match_ct = 0

    # TEST INPUTS
    # start_a = 65
    # start_b = 8921
    # count = 5

    # for a, b in gen_pt1(count):
    #     match_ct += bin(a)[-16:] == bin(b)[-16:]

    # PART 2
    count = 5000000
    match_ct = 0

    # TEST INPUTS
    # start_a = 65
    # start_b = 8921
    # count = 1056

    for a, b in gen_pt2(count):
        match_ct += bin(a)[-16:] == bin(b)[-16:]

    print(f'Matches: {match_ct}')
