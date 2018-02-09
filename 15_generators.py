mult_a = 16807
mult_b = 48271
div = 2147483647
start_a = 289
start_b = 629
count = 40000000

# TEST INPUTS
# start_a = 65
# start_b = 8921
# count = 5


def gen() -> tuple:
    a = start_a
    b = start_b
    yield a, b
    for _ in range(count - 1):
        a = (a * mult_a) % div
        b = (b * mult_b) % div
        yield a, b


if __name__ == '__main__':

    # PART 1
    match_ct = 0
    for a, b in gen():
        # print(f'{bin(a)}, {bin(b)}')
        match_ct += bin(a)[-16:] == bin(b)[-16:]
    print(f'Matches: {match_ct}')

