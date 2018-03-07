from proj.prog import Executor


class Coprocessor:

    def __init__(self, initial_values: dict=None):
        self.exc = Executor(sbox_locals=initial_values)

    def _val(self, x: str) -> str:
        """
        Returns the integer value of the input, formatted as a string
        :param x: An integer value or a register name
        :return: `x`, if `x` contains only an integer, or the eval of `x` in this object's local execution context
        """
        return x if x.isdigit() else str(self.exc.evals(x))

    def _interpret(self, instr: str) -> (str, int):
        """
        Interpret an instruction from the input as Python
        :return: `(source, step)`: `source` is a Python command, `step` is an integer increment to the next instruction
        """

        cmd, x, y = instr.split()
        source, step = '', 1
        if cmd == 'set':
            source = f'{x} = ' + self._val(y)
        elif cmd == 'sub':
            source = f'{x} -= ' + self._val(y)
        elif cmd == 'mul':
            source = f'{x} *= ' + self._val(y)
        elif cmd == 'jnz':
            # Note: This instruction complicates the class design. Have to evaluate `x` at the moment of execution.
            # Also, its value affects the instruction pointer owned by the caller, not the sandbox namespace owned by
            #  this instance's executor.
            if int(self._val(x)) != 0:
                step = int(self._val(y))
        else:
            raise ValueError(instr)

        return source, step

    def run(self, instr: str) -> (str, int):
        """
        Executes a pseudo-Assembly instruction from the input
        :return: `(source, step)`: `source` is the Python that was used to represent the input instruction, `step`
        is an integer increment to the next instruction
        """
        source, step = self._interpret(instr)
        self.exc.execs(source)
        return source, step


if __name__ == '__main__':

    proc = Coprocessor({k: 0 for k in [_ for _ in 'abcdefgh']})

    with open('./coprocessor.txt') as file:
        program = [x.rstrip() for x in file.readlines()]

    ptr = 0
    muls = 0
    while 0 <= ptr < len(program):

        # Part 1: Count 'mul' instructions
        if program[ptr][0:3] == 'mul':
            muls += 1

        source, step = proc.run(program[ptr])
        ptr += step

        # print(f'{ptr}: ' + source + f'\t\tstep {step}')  # debug

    print(f'Part 1: {muls} mul instructions executed.')
