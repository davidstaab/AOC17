import numpy as np


def a_to_s(a: np.ndarray) -> str:
    return ''.join(a.flatten().tolist())


def s_to_a(s: str) -> np.ndarray:
    a = np.array(list(s))
    if a.size == 4:
        a.shape = (2, 2)
    elif a.size == 9:
        a.shape = (3, 3)
    elif a.size == 16:
        a.shape = (4, 4)
    else:
        raise ValueError(f'{s} does not hold a 2x2, 3x3, or 4x4 array')
    return a


def enhance(image: np.ndarray, sub_dim: int) -> np.ndarray:
    vsubs = np.vsplit(image, image.shape[0] / sub_dim)
    subs = [np.hsplit(v, v.shape[1] / sub_dim) for v in vsubs]
    new_subs = [[s_to_a(rules[a_to_s(h)]) for h in v] for v in subs]
    new_vsubs = [np.hstack(v) for v in new_subs]
    return np.vstack(new_vsubs)


image = s_to_a('010001111')

if __name__ == '__main__':

    rules = {}
    with open('./fractal.txt') as file:
        for line in file:
            k, v = line.rstrip().replace('.', '0').replace('#', '1').replace('/', '').split(' => ')
            rules[k] = v

    # expand dictionary to include all rotations and flips of each key. saves time and code later.
    new_rules = {}
    for k in rules:
        a = s_to_a(k)
        b = np.fliplr(a)
        new_rules[a_to_s(b)] = rules[k]
        new_rules[a_to_s(np.flipud(a))] = rules[k]
        new_rules[a_to_s(np.rot90(a, 1))] = rules[k]
        new_rules[a_to_s(np.rot90(a, 2))] = rules[k]
        new_rules[a_to_s(np.rot90(a, 3))] = rules[k]
        new_rules[a_to_s(np.rot90(b, 1))] = rules[k]
        new_rules[a_to_s(np.rot90(b, 3))] = rules[k]
    rules.update(new_rules)
    del new_rules

    for _ in range(5):
        if image.size % 4 == 0:  # can be split into 2x2 subarrays
            image = enhance(image, sub_dim=2)
        elif image.size % 9 == 0:  # can be split into 3x3 subarrays
            image = enhance(image, sub_dim=3)
    print(f"Part 1: {a_to_s(image).count('1')} pixels on.", end='\n\n')
    print(image)