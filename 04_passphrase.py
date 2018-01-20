# series of all-lower chars
# sep='\s'
# no duplicate words


if __name__ == '__main__':
    with open('./passphrases.txt') as file:
        valid_ct = 0
        for line in file:
            words = line.rstrip().split(sep=' ')  # Remove '\n' from `line` so it doesn't show up in words[-1]

            valid_ct += 1  # presume unique words
            for w in words:
                if words.count(w) > 1:
                    valid_ct -= 1  # remove presumption
                    break
        print('Valid passphrases: {}'.format(valid_ct))
