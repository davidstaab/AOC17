class Wall:

    __slots__ = ['rng', 'loc', 'step']

    def _init_state(self):
        if self.rng != 0:
            self.loc = 0
            self.step = 1
        else:
            self.loc = -1
            self.step = 0

    def __init__(self, rng: int):
        self.rng = rng
        self._init_state()

    def __str__(self):
        return format('Range {0: d} - Scanner at {1: d}'.format(self.rng, self.loc))

    def move(self):
        if self.rng != 0:
            self.loc += self.step
            if not 0 < self.loc < self.rng - 1:  # scanner has hit a rail
                self.step *= -1

    def reset(self):
        self._init_state()


def reset_firewall(fw):
    for x in fw:
        x.reset()


if __name__ == '__main__':

    fw = []
    with open('./firewall.txt') as file:
        # build firewall layers
        layer = 0
        for line in file:
            wall_loc, rng = [int(x) for x in line.split(sep=': ')]
            for i in range(layer, wall_loc):
                fw.append(Wall(0))
            fw.append(Wall(rng))
            layer = wall_loc + 1

    # todo: TEST INPUT replaces above
    # fw = [
    #     Wall(3),
    #     Wall(2),
    #     Wall(0),
    #     Wall(0),
    #     Wall(4),
    #     Wall(0),
    #     Wall(4),
    # ]

    #########
    # Part 1: Run through the firewall immediately
    print('Part 1')
    severity = 0
    for layer in range(len(fw)):
        if fw[layer].loc == 0:  # collision detected
            sev = layer * fw[layer].rng
            print('Collision at depth {: >2d}! Severity: {: >3d}'.format(layer, sev))
            severity += sev
        for wall in fw:
            wall.move()

    print('Total path severity: {}'.format(severity))

    #########
    # Part 2: Delay until it's safe to go
    print('\n\nPart 2')

    # Run simulations until success
    delay, collided = -1, True
    while collided:
        if delay % 100 == 0:
            print('Running simulation {}'.format(delay + 1))

        reset_firewall(fw)
        delay += 1
        for _ in range(delay):
            for wall in fw:
                wall.move()

        collided = False  # reset flag
        for layer in range(len(fw)):
            if fw[layer].loc == 0:  # collision detected
                collided = True
                break
            for wall in fw:
                wall.move()
    print('No collision with delay {}.'.format(delay))
