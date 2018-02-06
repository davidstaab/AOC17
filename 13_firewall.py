class Wall:

    __slots__ = ['rng', 'loc', 'step']

    def __init__(self, rng: int):
        self.rng = rng

        if rng != 0:
            self.loc = 0
            self.step = 1
        else:
            self.loc = -1
            self.step = 0

    def __str__(self):
        return format('Range {0: d} - Scanner at {1: d}'.format(self.rng, self.loc))

    def move(self):
        if self.rng != 0:
            self.loc += self.step
            if not 0 < self.loc < self.rng - 1:  # scanner has hit a rail
                self.step *= -1


def did_collide(fw: list, depth: int) -> bool:
    return fw[depth].loc == 0


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

    # # todo: TEST INPUT
    # fw = [
    #     Wall(3),
    #     Wall(2),
    #     Wall(0),
    #     Wall(0),
    #     Wall(4),
    #     Wall(0),
    #     Wall(4),
    # ]

    # run through the firewall
    severity = 0
    for layer in range(len(fw)):
        if did_collide(fw, layer):
            sev = layer * fw[layer].rng
            print('Collision at depth {: >2d}! Severity: {: >3d}'.format(layer, sev))
            severity += sev
        for wall in fw:
            wall.move()

    print('Total path severity: {}'.format(severity))
