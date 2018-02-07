from proj import kh

seed = 'jzgqcdpd'

if __name__ == '__main__':
    ones = 0
    for i in range(128):
        dh = kh.KnotHash(f'{seed}-{i}').dense_hash()
        ones += kh.dh_bin(dh).count('1')
    print(f'Used squares: {ones}')
