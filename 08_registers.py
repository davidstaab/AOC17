if __name__ == '__main__':

    exc_globals = {'__builtins__': None}
    exc_locals = {}

    with open('./registers.txt') as file:
        for line in file:
            fields = line.rstrip().split(sep=' ').__iter__()
            var = next(fields)
            opr = next(fields).replace('inc', '+=').replace('dec', '-=')
            val = next(fields)
            cond = [f for f in fields]
            cond_var = cond[1]

            for v in [var, cond_var]:
                exec('try: {}\nexcept: {} = 0'.format(v, v), exc_globals, exc_locals)  # initialize var

            cmd = '{} {} {} {}'.format(var, opr, val, ' '.join(cond)) + ' else 0'
            exec(cmd, exc_globals, exc_locals)
            print(cmd + '... ' + str(exc_locals[var]))

        print(exc_locals)
        print(max(exc_locals.values()))
