list_sep = '->'

if __name__ == '__main__':

    # PART 1
    # find name at bottom of tree. just need the one in no other name's support list.
    bases = []
    supported = []
    with open('./circus.txt') as file:
        for line in file:
            if line.find(list_sep) >= 0:
                parts = line.split(list_sep)
                sup_list = parts[1].strip().split(sep=', ')
                supported.extend([x for x in sup_list if x not in supported])
                bases.append(parts[0].strip().split()[0])
            else:
                bases.append(line.strip().split()[0])
    print('Bottom of tree: {}'.format(set(bases) ^ set(supported)))
