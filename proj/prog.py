"""
Components used by problems that involve interpreting and executing pseudo-assembly programs
"""

import types


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

        self.execs = types.MethodType(sbox_exec, self)
        self.evals = types.MethodType(sbox_eval, self)
