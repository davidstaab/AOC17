# series of all-lower chars
# sep='\s'
# no duplicate words


if __name__ == '__main__':
    with open('./passphrases.txt') as file:
        unique_ct = 0
        no_perm_ct = 0

        for line in file:
            words = line.rstrip().split(sep=' ')  # Remove '\n' from `line` so it doesn't show up in words[-1]

            # PART 1
            unique_ct += 1  # presume unique words
            for w in words:
                if words.count(w) > 1:
                    unique_ct -= 1  # remove presumption
                    break

            # PART 2
            no_perm_ct += 1  # presume no permutations
            for i, base in enumerate(words):
                pre_ct = no_perm_ct
                for test in words[i + 1:]:
                    test = list(test)
                    for c in base:
                        try:
                            test.remove(c)
                        except ValueError:  # "c not in list"
                            test = True  # 'True' fails final check below
                            break
                    if not test:  # if all chars were mapped from `base` to `test`...
                        no_perm_ct -= 1  # remove presumption
                        break
                if no_perm_ct < pre_ct:
                    break  # Don't test remaining words in line. Failure already found.

        print('Unique-word passphrases: {}'.format(unique_ct))
        print('Non-permuted passphrases: {}'.format(no_perm_ct))
