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
        self._count = 0

    def is_garbage(self, char: str) -> bool:
        if self.group:
            # inside a garbage group
            if char == '>':
                # ending the group
                self.group = False
            else:
                self._count += 1
            return True
        elif char == '<':
            # starting a garbage group
            self.group = True
            return True
        else:
            # outside a garbage group
            return False

    @property
    def count(self):
        return self._count


def gen_token(stream, skip_bang: bool=True, skip_garbage: bool=True) -> str:
    """
    Strips the the next token from `stream` and yields it
    :param stream: Text stream to read from. Must be mutable.
    :param skip_bang: When true, skip and throw away each '!' and character following it
    :param skip_garbage: When true, skip and thrwo away everything in a garbage group
    :return: Token from `stream`
    """

    # [dstaab] Note: `garbage_ct` is what happens when you try to quickly adapt (hack) an OO design change to accomodate
    # a new requirement specification. I hacked the property into the class that encapsulates the needed info, then had
    # to poll it excessively in this loop -- AFTER calling the method that updates it, which breaks the abstraction of
    # the class! -- and dump it out to the main app that actually needs it, because this generator function itself
    # encapsulates the class that the app needs to ask for its property value. What a mess.

    gc = GarbageChecker(skip_garbage)
    for char, ct in BangSkipper(stream, skip=skip_bang):
        g = gc.is_garbage(char)
        garbage_ct = gc.count
        if not g:
            yield char, ct, garbage_ct


if __name__ == '__main__':

    sum_levels = 0
    sum_garbage = 0
    with open('./stream.txt') as file:
        cur_level = 0
        for tok, ct, g_ct in gen_token(file):
            sum_garbage = g_ct
            print('{}:\t{}'.format(ct, tok))
            if tok == '{':
                cur_level += 1
                sum_levels += cur_level
            elif tok == '}' and cur_level > 0:
                cur_level -= 1
    print('Sum of all nesting levels: {}'.format(sum_levels))
    print('Sum of all garbage characters: {}'.format(sum_garbage))
