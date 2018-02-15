from proj import kh

input = 343

# TEST CODE
# input = 3

buf = kh.CircularBuffer([0])

if __name__ == '__main__':
    i = 0
    for x in range(1, 2018):
        i += input
        i = buf.insert(i + 1, x) % len(buf)
    print(f'Pt 1: Interesting values: {buf[i]}, {buf[i + 1]}')
