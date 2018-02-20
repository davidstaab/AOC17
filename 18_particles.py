import numpy as np

# Index names for legibility
si, dsi, d2si = 0, 1, 2
xi, yi, zi = 0, 1, 2


def m_norm(vector) -> int:
    """
    Manhattan norm of a vector
    """
    ret = 0
    for s in vector:
        ret += abs(s)
    return ret


def update(particles: np.ndarray):
    for i, p in enumerate(particles):
        np.add(p[dsi], p[d2si], out=particles[i, dsi])
        np.add(p[si], particles[i, dsi], out=particles[i, si])  # Note: Use updated `ds` value immediately


if __name__ == '__main__':

    # Build data structure: 3-d array of [particle][time-derivative][vector-component], i.e. [0][dsi][yi]
    raw_data = []
    with open('./particles.txt') as file:
        raw_data = [line.rstrip().split(', ') for line in file]
        for i, p in enumerate(raw_data):
            raw_data[i] = [[int(v) for v in vec[3:len(vec) - 1].split(',')] for vec in p]
    particles = np.array(raw_data)
    del raw_data

    # Mathematical conditions for being the "long-run closest" to the origin:
    # 1 Smallest distance from origin (norm of `pos`)
    # 2 Smallest speed (norm of `vel`) so it won't overtake any other particles
    # 3 All particles leaving origin (Sufficient, but probably not necessary. Will have slow convergence.):
    #   - Traveling away from origin (dot product of `pos` and `vel` > 0)
    #   - Accelerating away from origin (dot product of `pos` and `accel` > 0)

    leaving_origin = [False for _ in particles]
    while 1:
        update(particles)

        min_dist, min_speed = float('inf'), float('inf')
        min_dist_i, min_speed_i = -1, -1
        for i, p in enumerate(particles):
            dist = m_norm(p[si])
            speed = m_norm(p[dsi])
            if dist < min_dist:  # condition 1
                min_dist = dist
                min_dist_i = i
            if speed < min_speed:  # condition 2
                min_speed = speed
                min_speed_i = i
            if not leaving_origin[i]:  # only recalculate if not already true
                if np.dot(p[si], p[dsi]) > 0 and np.dot(p[si], p[d2si]) > 0:  # condition 3 for particle i
                    leaving_origin[i] = True

        print(f'Nearest: {min_dist_i:3}, Slowest: {min_speed_i:3}, # Leaving origin: {leaving_origin.count(True)}')

        if all(leaving_origin) and min_dist_i >= 0 and min_dist_i == min_speed_i:
            break
    print(f'Nearest particle at t = inf: {min_dist_i}')
