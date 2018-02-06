class Scanner:
    """
    A stateful scanner for one layer of the firewall.
    """

    # [dstaab] I recognize that providing public access to internal state and a setter for applying it is an OO anti-
    # pattern. I'm desperate to make the simulation run faster, though, and deep copying (my other attempted solution)
    # creates a memory leak!

    __slots__ = ['rng', 'loc', 'step']

    def _init_state(self, loc: int=0, step: int=1):
        if self.rng != 0:
            self.loc = loc
            self.step = step
        else:
            self.loc = -1
            self.step = 0

    def __init__(self, rng: int):
        self.rng = rng
        self._init_state()

    def __str__(self):
        return format('Range {0: d} - Scanner at {1: d}'.format(self.rng, self.loc))

    @property
    def state(self) -> tuple:
        return self.loc, self.step

    def move(self):
        if self.rng:
            self.loc += self.step
            if not 0 < self.loc < self.rng - 1:  # scanner has hit a rail
                self.step *= -1

    def reset(self, state: tuple=None):
        if state is not None:
            self._init_state(*state)
        else:
            self._init_state()


def reset_firewall(fw: list, states: list=None):
    if states is None:
        for x in fw:
            x.reset()
    else:
        for x, y in zip(fw, states):
            x.reset(y)


if __name__ == '__main__':

    fw = []
    with open('./firewall.txt') as file:
        # build firewall layers
        layer = 0
        for line in file:
            wall_loc, rng = [int(x) for x in line.split(sep=': ')]
            for i in range(layer, wall_loc):
                fw.append(Scanner(0))
            fw.append(Scanner(rng))
            layer = wall_loc + 1

    # todo: TEST INPUT replaces above
    # fw = [
    #     Scanner(3),
    #     Scanner(2),
    #     Scanner(0),
    #     Scanner(0),
    #     Scanner(4),
    #     Scanner(0),
    #     Scanner(4),
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
        for scanner in fw:
            scanner.move()
    print('Total path severity: {}'.format(severity))
    reset_firewall(fw)

    #########
    # Part 2: Delay until it's safe to go
    print('\n\nPart 2')

    # Run simulations until success
    delay, collided = 0, True
    fw_init_state = [(None, None) for _ in fw]
    while collided:
        if delay % 10000 == 0:
            print('{} simulations done.'.format(delay))

        # delay once (more) while scanners move. grab post-delay state so firewall can be reset after simulation.
        delay += 1
        for i, scanner in enumerate(fw):
            scanner.move()
            fw_init_state[i] = scanner.state

        # run simulation after delay.
        collided = False
        for layer in range(len(fw)):
            if fw[layer].loc == 0:  # collision detected
                collided = True
                break
            for scanner in fw:
                scanner.move()

        reset_firewall(fw, fw_init_state)

    print('No collision with delay {}.'.format(delay))
