# Lexer reqs:
# '\{.*\}' is a group.
#       nestable, so pure regex is out.
#       groups are scored by nesting level. sum scores of all groups (i.e. '{{{}}}' = 1 + 2 + 3 = 6)
# '<.*>' is garbage.
#       inside a garbage group, '!' cancels next char, including another '!'
#       non-nestable, so '<', '{', and '}' are just chars.


class BangSkipper:

    def __init__(self, stream, skip=True):
        self.stream = stream
        self.skip = skip
        self.count = 0

    def __get_char(self):
        c = self.stream.read(1)
        if c == '':
            raise EOFError()
        self.count += 1
        return c

    def __iter__(self):
        return self

    def __next__(self):
        try:
            while 1:
                char = self.__get_char()
                if self.skip and char == '!':
                    self.__get_char()  # ignore `char`, throw away next character, too
                else:
                    break
            return char, self.count
        except EOFError:
            raise StopIteration


class GarbageChecker:
    """
    To be used AFTER BangSkipper if both are invoked!
    """

    def __init__(self, skip=True):
        self.skip = skip
        self.group = False

    def is_garbage(self, char: str) -> bool:
        if self.group:
            if char == '>':
                self.group = False
            return True
        elif char == '<':
            self.group = True
            return True
        else:
            return False


def gen_token(stream, skip_bang: bool=True, skip_garbage: bool=True) -> str:
    """
    Strips the the next token from `stream` and yields it
    :param stream: Text stream to read from. Must be mutable.
    :param skip_bang: When true, skip and throw away each '!' and character following it
    :param skip_garbage: When true, skip and thrwo away everything in a garbage group
    :return: Token from `stream`
    """
    gc = GarbageChecker(skip_garbage)
    for char, ct in BangSkipper(stream, skip=skip_bang):
        if not gc.is_garbage(char):
            yield char, ct


if __name__ == '__main__':

    sum_levels = 0
    with open('./stream.txt') as file:
        cur_level = 0
        for tok, ct in gen_token(file):
            print('{}:\t{}'.format(ct, tok))
            if tok == '{':
                cur_level += 1
                sum_levels += cur_level
            elif tok == '}' and cur_level > 0:
                cur_level -= 1
    print('Sum of all nesting levels: {}'.format(sum_levels))
