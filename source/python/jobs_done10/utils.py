from __future__ import unicode_literals



#===================================================================================================
# Dedent
#===================================================================================================
def Dedent(text):
    '''
    Heavily inspired by textwrap.dedent, with a few changes (as of python 2.7)
        - No longer transforming all-whitespace lines into ''
        - Options to ignore first and last linebreaks of `text`.

    The last option is particularly useful because of ESSS coding standards.
    For example, using the default textwrap.dedent to create a 3-line string would look like this:
        textwrap.dedent("""    line1
            line2
            line3"""
        )

    With these options, you can create a better looking code with:
        Dedent(
            """
            line1
            line2
            line3
            """
        )

    :param unicode text:
        Text to be dedented (see examples above)

    :param bool ignore_first_linebreak:
        If True, everything up to the first '\n' is ignored

    :param bool ignore_last_linebreak:
        If True, everything after the last '\n' is ignored


    Original docs:
        Remove any common leading whitespace from every line in `text`.

        This can be used to make triple-quoted strings line up with the left edge of the display,
        while still presenting them in the source code in indented form.

        Note that tabs and spaces are both treated as whitespace, but they are not equal: the lines
        "  hello" and "\thello" are  considered to have no common leading whitespace.  (This
        behaviour is new in Python 2.5; older versions of this module incorrectly expanded tabs
        before searching for common leading whitespace.)
    '''
    if '\n' in text:
        text = text.split('\n', 1)[1]
    if '\n' in text:
        text = text.rsplit('\n', 1)[0]

    import re
    _leading_whitespace_re = re.compile('(^[ ]*)(?:[^ \n])', re.MULTILINE)

    # Look for the longest leading string of spaces and tabs common to
    # all non-empty lines.
    margin = None
    indents = _leading_whitespace_re.findall(text)

    for indent in indents:
        if margin is None:
            margin = indent

        # Current line more deeply indented than previous winner:
        # no change (previous winner is still on top).
        elif indent.startswith(margin):
            pass

        # Current line consistent with and no deeper than previous winner:
        # it's the new winner.
        elif margin.startswith(indent):
            margin = indent

    if margin:
        text = re.sub(r'(?m)^' + margin, '', text)
    return text


import collections
import functools

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
