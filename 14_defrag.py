from proj import kh
import numpy as np
from scipy.ndimage import label

seed = 'jzgqcdpd'

if __name__ == '__main__':

    hashes = []
    ones = 0
    for i in range(128):
        dh = kh.KnotHash(f'{seed}-{i}').dense_hash()
        dhb = kh.dh_bin(dh)
        ones += dhb.count('1')  # PART 1
        hashes.append([int(_) for _ in dhb])  # PART 2
    print(f'Used squares: {ones}')

    # PART 2 CONT'd
    disk = np.array(hashes)
    labeled, regions_ct = label(disk)  # default structure is cross shape needed here
    print(f'Used regions: {regions_ct}')
