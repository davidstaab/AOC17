from collections import deque
from proj import prog


class Part1Program(prog.Interpreter):

    def _snd(self, reg: str) -> str:
        """
        An implementation of Interpreter.snd() for Part 1 of the puzzle
        """
        cmd = 'sound = ' + self._val(reg)
        self.exc.execs(cmd)
        return f'{self.i}: ' + cmd

    def _rcv(self, reg: str):
        """
        An implementation of Interpreter.rcv() for Part 1 of the puzzle
        """
        if int(self._val(reg)) != 0:
            m = '{}: sound = {}'.format(self.i, self.exc.sbox_locals['sound'])
            raise StopIteration(m)


class Part2Program(prog.Interpreter):

    class FailedRcvError(Exception):
        """Notification that a program failed to receive a value when trying to use its deque"""
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sq = deque()
        self.rq = deque()

    def _snd(self, reg: str) -> str:
        val = self._val(reg)
        self.sq.append(val)
        return f'{self.i}: Send {reg} -> {val}'

    def _rcv(self, reg: str):
        try:
            val = self.rq.popleft()
            cmd = f'{reg} = {val}'
            self.exc.execs(cmd)
            return f'{self.i}: Receive {val} -> {reg}'
        except IndexError:
            raise type(self).FailedRcvError(f'{self.i}: Receive failure')


if __name__ == '__main__':

    instrs = []
    with open('./duet.txt') as file:
        instrs = [x.rstrip().split() for x in file.readlines()]

    # PART 1
    # TEST CODE
    # test = """set a 1
    #         add a 2
    #         mul a a
    #         mod a 5
    #         snd a
    #         set a 0
    #         rcv a
    #         jgz a -1
    #         set a 1
    #         jgz a -2"""
    # instrs = [x.strip().split() for x in test.split(sep='\n')]
    ###########
    prog = Part1Program(instrs)
    for cmd in prog:
        # print(cmd)  # Pretty, but slow
        pass
    print(f"Part 1: Last frequency played: {prog.vars['sound']}")
    del prog

    # PART 2
    # TEST CODE
    # test = """snd 1
    #         snd 2
    #         snd p
    #         rcv a
    #         rcv b
    #         rcv c
    #         rcv d"""
    # instrs = [x.strip().split() for x in test.split(sep='\n')]
    ###########
    progs = [Part2Program(instruction_set=instrs, pid=x) for x in range(2)]
    running = [True for _ in progs]
    sent_by_1_ct = 0
    while any(running):
        for i, p in enumerate(progs):
            try:
                cmd = next(p)
                print(f'p{i}: ' + cmd)  # Pretty, but slow
                running[i] = True
            except Part2Program.FailedRcvError as e:
                print(f'p{i}: ' + str(e))  # Pretty, but slow
                running[i] = False
        try:
            progs[1].rq.append(progs[0].sq.popleft())
        except IndexError:
            pass
        try:
            progs[0].rq.append(progs[1].sq.popleft())
            sent_by_1_ct += 1
        except IndexError:
            pass
    print(f'Part 2: Values sent by program 1: {sent_by_1_ct}')
