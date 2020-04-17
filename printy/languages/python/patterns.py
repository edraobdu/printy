"""
This module will contain the patters specific for the Python programming
language, like key words and some other patters that determine whether the text
must be colored or not, or if we should start a block where some other patterns
must be taken into account, and what other must not, like, e.g, only within a
class definition the special words 'self' and 'cls' and some methods like
__init__ or __str__ have a special meaning and therefore they should be colored.
"""

# Defines the patterns that represent keywords to be highlighted by the language
# and the color to be used represented by a flag
key_words_flag = 'r'
builtin_flag = 'b'
decorator_flag = 'y'
string_flag = 'n'
number_flag = 'c'
inline_comment_flag = 'g'
multiline_comment_flag = 'n'
function_declared_flag = 'yB'
# In classes
builtin_methods_flag = 'mB'
# like cls, self
classes_key_words = 'm'


GLOBAL_PATTERNS = {
    ### Key words
    'from': key_words_flag,
    'import': key_words_flag,
    'as': key_words_flag,
    'if': key_words_flag,
    'else': key_words_flag,
    'elif': key_words_flag,
    'in': key_words_flag,
    'is': key_words_flag,
    'or': key_words_flag,
    'and': key_words_flag,
    'not': key_words_flag,
    'def': key_words_flag,
    'class': key_words_flag,
    'while': key_words_flag,
    'try': key_words_flag,
    'except': key_words_flag,
    'raise': key_words_flag,
    'assert': key_words_flag,
    'continue': key_words_flag,
    'pass': key_words_flag,
    'break': key_words_flag,
    'False': key_words_flag,
    'True': key_words_flag,
    'None': key_words_flag,
    ',': key_words_flag,

    ### Builtin
    'type': builtin_flag,
    'int': builtin_flag,
    'float': builtin_flag,
    'str': builtin_flag,
    'bool': builtin_flag,
    'isinstance': builtin_flag,
    'print': builtin_flag,
    'len': builtin_flag,
    'list': builtin_flag,
    'set': builtin_flag,
    'dir': builtin_flag,
    'vars': builtin_flag,
    'object': builtin_flag,
    'Exception': builtin_flag,
    'TypeError': builtin_flag,
    'ValueError': builtin_flag,
    'KeyError': builtin_flag,
    'ImportError': builtin_flag,

    ### Other paters

    # Decorator
    # f-strings
    'f\'': string_flag,
    'f\"': string_flag,
    # multiline_comment
    '\"\"\"': multiline_comment_flag,
    '\'\'\'': multiline_comment_flag,
    # inline comment
    '#': inline_comment_flag,
}

# Patters that are only valid within a class definition
PATTERS_IN_CLASSES = {
    '__init__': builtin_methods_flag,
    '__init_subclass__': builtin_methods_flag,
    '__str__': builtin_methods_flag,
    '__repr__': builtin_methods_flag,
    '__unicode__': builtin_methods_flag,
    '__new__': builtin_methods_flag,
    '__delattr__': builtin_methods_flag,
    '__dir__': builtin_methods_flag,
    '__eq__': builtin_methods_flag,
    '__format__': builtin_methods_flag,
    '__getattribute__': builtin_methods_flag,
    '__ge__': builtin_methods_flag,
    '__hash__': builtin_methods_flag,
    '__le__': builtin_methods_flag,
    '__lt__': builtin_methods_flag,
    '__ne__': builtin_methods_flag,
    '__reduce_ex__': builtin_methods_flag,
    '__reduce__': builtin_methods_flag,
    '__setattr__': builtin_methods_flag,
    '__sizeof__': builtin_methods_flag,
    '__doc__': builtin_methods_flag,
    '__module__': builtin_methods_flag,
    '__abs__': builtin_methods_flag,
    '__add__': builtin_methods_flag,
    '__and__': builtin_methods_flag,
    '__bool__': builtin_methods_flag,
    '__ceil__': builtin_methods_flag,
    '__divmod__': builtin_methods_flag,
    '__floordiv__': builtin_methods_flag,
    '__float__': builtin_methods_flag,
    '__floor__': builtin_methods_flag,
}


# stores the first character of the patters, so, while looping the test
# We can start an inspection on the text's sections that starts with one of
# this
POTENTIAL_GLOBAL_PATTERNS = set(map(lambda x: x[0], GLOBAL_PATTERNS.keys()))
POTENTIAL_IN_CLASSES_PATTERNS = set(map(lambda x: x[0], PATTERS_IN_CLASSES.keys()))


def potential_pattern(char, in_class=False):
    """
    Function called whenever we want to know if a character must start
    an inspection, to identify if its a pattern or not.
    """
    if in_class:
        if char in POTENTIAL_IN_CLASSES_PATTERNS:
            return True
    else:
        if char in POTENTIAL_GLOBAL_PATTERNS:
            return True
    return False


def define_pattern(char, remaining_text, in_class):
    """
    Once we declare a character as a potential pattern, we need to start a block
    and figure out what special pattern it is, and what action to execute.

    for instance, if we find that character finally ends up being a 'class',
    we start a block called 'CLASS', so we can integrate some other patterns in
    the list (POTENTIAL_IN_CLASSES_PATTERNS), or, if it is an f-string, then we
    need to ensure that everything inside a {} is formatted as regular python
    and not as string.
    """
    if potential_pattern(char, in_class):
        # Now that we know this is a potential pattern, we keep looping
        # to know which pattern exactly it is
        pattern = [char]
        for c in remaining_text:
            pattern.append(c)
            new_pattern = ''.join(pattern)
            if not in_class:
                # we just look up for a match in the global patterns
                if new_pattern not in GLOBAL_PATTERNS.keys():
                    continue
                else:
                    # Now, we need to know how we need to proceed, let's start
                    # with Inline comments
                    # For inline comments, the block finishes when a new
                    # line-brake is made
                    pass
            else:
                # Then we need to lok up for a match in both global and
                # in_classes patterns
                pass
