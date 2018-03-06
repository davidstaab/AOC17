"""
Components used by problems that involve interpreting and executing pseudo-assembly programs
"""

from collections.abc import Iterator
from abc import abstractmethod
from types import MethodType


class Executor:
    """
    Is a sandboxed executor and evaluator of Python statements.
    """

    def __init__(self, sbox_globals: dict=None, sbox_locals: dict=None):

        # Set up execution context for this instance
        if sbox_globals is not None:
            sbox_globals.setdefault('__builtins__', None)
            self.sbox_globals = sbox_globals
        else:
            self.sbox_globals = {'__builtins__': None}
        self.sbox_locals = {} if sbox_locals is None else sbox_locals

        # Monkey patch closures onto this instance
        def sbox_exec(self, source: str):
            """A persistent sandbox environment for calls to `exec`"""
            return exec(source, self.sbox_globals, self.sbox_locals)

        def sbox_eval(self, expr: str):
            """A persistent sandbox environment for calls to `eval`"""
            return eval(expr, self.sbox_globals, self.sbox_locals)

        self.execs = MethodType(sbox_exec, self)
        self.evals = MethodType(sbox_eval, self)


class Interpreter(Iterator):
    """
    Is a translator from input grammar to Python grammar.Is also an iterator that executes one statement per call.
    Has an Executor and uses this when called in iteration.
    """

    def _val(self, x: str) -> str:
        """
        Returns the integer value of the input, formatted as a string
        :param x: An integer value or a register name
        :return: `x`, if `x` contains only an integer, or the eval of `x` in this object's local execution context
        """
        if x.isdigit():
            return x
        else:
            return str(self.exc.evals(x))

    @property
    def vars(self) -> dict:
        return self.exc.sbox_locals

    @abstractmethod
    def _snd(self, reg: str) -> str:
        """
        Placeholder for the `snd` instruction's behavior. User needs to implement this and assign it to object.
        :return: A display string of the operation performed by this instruction, i.e. '10: Did a thing'
        """
        pass

    @abstractmethod
    def _rcv(self, reg) -> str:
        """
        Placeholder for the 'rcv` instruction's behavior. User needs to implement this and assign it to object.
        :return: A display string of the operation performed by this instruction, i.e. '10: Did a thing'
        """
        pass

    def __init__(self, instruction_set: list, pid: int=None):
        context = None if pid is None else {'p': pid}
        self.exc = Executor(sbox_locals=context)
        self.instrs = instruction_set
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
            if reg not in self.exc.sbox_locals:
                self.exc.sbox_locals[reg] = 0

            incr = 1
            if instr == 'set':
                cmd = f'{reg} = ' + self._val(instrs[self.i][2])
                self.exc.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'add':
                cmd = f'{reg} += ' + self._val(self.instrs[self.i][2])
                self.exc.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'mul':
                cmd = f'{reg} *= ' + self._val(self.instrs[self.i][2])
                self.exc.execs(cmd)
                ret = f'{self.i}: ' + cmd
            elif instr == 'mod':
                cmd = f'{reg} %= ' + self._val(self.instrs[self.i][2])
                self.exc.execs(cmd)
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