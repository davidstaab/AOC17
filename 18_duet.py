from collections.abc import Iterator
from collections import deque
from types import MethodType

# Note: Man, this got ugly. I approached the different method implementations for snd() and rcv() in a Javascript way
#  using MethodType() here. A more natural implementation would probably be to make Program a base class for Program1
#  and Program2 using the abc module, then make snd() and rcv() @abstractmethods. That would eliminate the clunky
#  factory functions and IDE-breaking run-time property definitions. I'd definitely like to do this "the right way"
#  later.


class Program(Iterator):

    @staticmethod
    def init_safe_exec(exc_locals: dict):
        """
        Creates a persistent sandbox environment for calls to `exec`
        :return: `safe_exec`, a function that can be called instead of `exec`
        """
        safe_globals = {'__builtins__': None}

        def safe_exec(source: str):
            return exec(source, safe_globals, exc_locals)

        return safe_exec

    @staticmethod
    def init_safe_eval(exc_locals: dict):
        """
        Creates a persistent sandbox environment for calls to `eval`
        :return: `safe_eval`, a function that can be called instead of `eval`
        """
        safe_globals = {'__builtins__': None}

        def safe_eval(expr: str):
            return eval(expr, safe_globals, exc_locals)

        return safe_eval

    def _val(self, x: str) -> str:
        """
        Returns the integer value of the input, formatted as a string
        :param x: An integer value or a register name
        :return: `x`, if `x` contains only an integer, or the eval of `x` in this object's local execution context
        """
        if x.isdigit():
            return x
        else:
            return str(self.evals(x))

    @property
    def vars(self) -> dict:
        return self.context

    def _snd(self, reg: str) -> str:
        """
        Placeholder for the `snd` instruction's behavior. User needs to implement this and assign it to object.
        :return: A display string of the operation performed by this instruction, i.e. '10: Did a thing'
        """
        raise NotImplementedError

    def _rcv(self, reg) -> str:
        """
        Placeholder for the 'rcv` instruction's behavior. User needs to implement this and assign it to object.
        :return: A display string of the operation performed by this instruction, i.e. '10: Did a thing'
        """
        raise NotImplementedError

    def __init__(self, instruction_set: list, pid: int=None):
        self.instrs = instruction_set
        self.context = {} if pid is None else {'p': pid}
        self.execs = self.init_safe_exec(exc_locals=self.context)
        self.evals = self.init_safe_eval(exc_locals=self.context)
        self.i = 0

    def __iter__(self):
        return super().__iter__()  # use default behavior

    def __next__(self):
        if 0 <= self.i < len(self.instrs):

            # try:
            #     print('{}: i = {}'.format(self._val('p'), self.i))
            # except TypeError:
            #     pass

            instr = self.instrs[self.i][0]
            reg = self.instrs[self.i][1]
            if reg not in self.context:
                self.context[reg] = 0

            incr = 1
            if instr == 'set':
                cmd = f'{reg} = ' + self._val(instrs[self.i][2])
                self.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'add':
                cmd = f'{reg} += ' + self._val(self.instrs[self.i][2])
                self.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'mul':
                cmd = f'{reg} *= ' + self._val(self.instrs[self.i][2])
                self.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'mod':
                cmd = f'{reg} %= ' + self._val(self.instrs[self.i][2])
                self.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'snd':
                ret = self._snd(reg)
            elif instr == 'rcv':
                ret = self._rcv(reg)
            elif instr == 'jgz' and int(self._val(reg)) > 0:
                incr = int(self._val(self.instrs[self.i][2]))
                ret = f'{self.i}: Jump to {self.i + incr}'
            else:
                ret = f'{self.i}: {instr} no-op'

            self.i += incr
            return ret
        else:
            raise StopIteration


class FailedRcvError(Exception):
    """
    Notification that a program failed to receive a value when trying to use its deque
    """
    pass


def pt1_program(instructions: list) -> Program:
    """
    A factory method for creating the program that executes in part 1 of the puzzle.
    """

    def snd1(self, reg: str) -> str:
        """
        An implementation of Program.snd() for Part 1 of the puzzle
        """
        cmd = 'sound = ' + self._val(reg)
        self.execs(cmd)
        return f'{self.i}: ' + cmd

    def rcv1(self, reg: str):
        """
        An implementation of Program.rcv() for Part 1 of the puzzle
        """
        if int(self._val(reg)) != 0:
            m = '{}: sound = {}'.format(self.i, self.context['sound'])
            raise StopIteration(m)

    ret = Program(instructions)
    ret._snd = MethodType(snd1, ret)  # Note: This is how you attach method implmementations to an object
    ret._rcv = MethodType(rcv1, ret)
    return ret


def pt2_program(pid: int, instructions: list) -> Program:
    """
    A factory method for creating one of the programs that execute in part 2 of the puzzle.
    """

    def snd2(self, reg: str) -> str:
        """
        An implementation of Program.snd() for Part 2 of the puzzle
        """
        val = self._val(reg)
        self.sq.append(val)
        return f'{self.i}: Send {reg} -> {val}'

    def rcv2(self, reg: str):
        """
        An implementation of Program.rcv() for Part 2 of the puzzle
        """
        try:
            val = self.rq.popleft()
            cmd = f'{reg} = {val}'
            self.execs(cmd)
            return f'{self.i}: Receive {val} -> {reg}'
        except IndexError:
            raise FailedRcvError(f'{self.i}: Receive failure')

    ret = Program(instructions, pid=pid)
    ret.sq = deque()
    ret.rq = deque()
    ret._snd = MethodType(snd2, ret)
    ret._rcv = MethodType(rcv2, ret)
    return ret


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
    prog = pt1_program(instrs)
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
    progs = [pt2_program(x, instrs) for x in range(2)]
    running = [True for _ in progs]
    sent_by_1_ct = 0
    while any(running):
        for i, p in enumerate(progs):
            try:
                cmd = next(p)
                # print(f'p{i}: ' + cmd)  # Pretty, but slow
                running[i] = True
            except FailedRcvError as e:
                # print(f'p{i}: ' + str(e))  # Pretty, but slow
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
