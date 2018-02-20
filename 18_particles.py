import numpy as np

# Index names for legibility
si, dsi, d2si = 0, 1, 2
xi, yi, zi = 0, 1, 2

# Toggle parts 1 and 2
do_p1 = True


def m_norm(vector) -> int:
    """
    Manhattan norm of a vector
    """
    ret = 0
    for s in vector:
        ret += abs(s)
    return ret


def update(particles: np.ndarray, particles_old: np.ndarray=None):
    """
    Update the simulation. Response to "clock tick" in main loop.
    """
    if particles_old is not None:
        np.copyto(particles_old, particles)
    for i, p in enumerate(particles):
        np.add(p[dsi], p[d2si], out=particles[i, dsi])
        np.add(p[si], particles[i, dsi], out=particles[i, si])  # Note: Use updated `ds` value immediately


def collide(particles: np.ndarray, collisions: np.ndarray):
    """
    Update list of collisions
    """
    for i in range(len(particles)):
        if collisions[i]:
            continue
        else:
            coll = False
            for j in range(i + 1, len(particles)):
                if all([particles[i, si, c] == particles[j, si, c] for c in (xi, yi, zi)]):
                    collisions[j] = True
                    coll = True
            if coll:
                collisions[i] = True


if __name__ == '__main__':

    # Build data structure: 3-d array of [particle][time-derivative][vector-component], i.e. [0][dsi][yi]
    raw_data = []
    with open('./particles.txt') as file:
        raw_data = [line.rstrip().split(', ') for line in file]
        for i, p in enumerate(raw_data):
            raw_data[i] = [[int(v) for v in vec[3:len(vec) - 1].split(',')] for vec in p]
    particles = np.array(raw_data)

    # PART 1
    # Mathematical conditions for being the "long-run closest" to the origin:
    # 1 Smallest distance from origin (norm of `pos`)
    # 2 Smallest speed (norm of `vel`) so it won't overtake any other particles
    # 3 All particles leaving origin (Sufficient, but probably not necessary. Will have slow convergence.):
    #   - Traveling away from origin (dot product of `pos` and `vel` > 0)
    #   - Accelerating away from origin (dot product of `pos` and `accel` > 0)

    if do_p1:
        leaving_origin = [False for _ in particles]
        t = 0
        print('Proximity simulation:')
        while 1:
            update(particles)
            t += 1

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

            str1 = f't={t}, Nearest: {min_dist_i:3}, Slowest: {min_speed_i:3}'
            str2 = f'Leaving origin: {leaving_origin.count(True)}/{len(leaving_origin)}'
            print(str1 + ' ' + str2)

            if all(leaving_origin) and min_dist_i >= 0 and min_dist_i == min_speed_i:
                break
        print(f'Nearest particle at t->inf: {min_dist_i}', end='\n\n')

    # PART 2
    # How do I know whether a collision will happen? If each particle is moving away from each other particle and
    # accelerating away too, they can't collide.
    # 1 Each particle traveling away from every other particle (dot product <= 0 -- n! complexity?)
    # 2 Each paricle accelerating in the direction of its travel so it won't turn and collide with another particle
    #     cos theta = dot(A, B) / norm(A) / norm(B)
    # Condition 2 needs a threshold for comparison because cosine similarity between vel and acc asymptotically
    # approaches 1 in some cases.

    particles = np.array(raw_data)  # reinit data structure for new simulation
    particles_old = np.copy(particles)
    collisions = np.zeros(len(particles), dtype=bool)  # flattened mask for collision checks

    t = 0
    print(f'Collision simulation:\nt={t}, Particles remaining: {len(particles)}')
    while 1:
        update(particles, particles_old)
        collide(particles, collisions)
        t += 1
        live_particles = len(particles) - np.count_nonzero(collisions)
        print(f't={t}, Particles remaining: {live_particles}')

        # Note: Remove scientist hat, don engineer hat: I can guess the answer by watching the output until I'm
        # satisfied the number of live particles hasn't dropped in sufficient time. Faster than cding the conditions
        # above and running the simulation with them enabled. (Result: it worked. I found the answer in less than a
        # minute.)
