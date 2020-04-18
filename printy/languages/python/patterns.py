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
line_comment_flag = 'g'
block_comment_flag = 'n'
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
    'return': key_words_flag,
    'False': key_words_flag,
    'True': key_words_flag,
    'None': key_words_flag,
    ',': key_words_flag,
    'lambda': key_words_flag,

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
    'filter': builtin_flag,
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
    '@': decorator_flag,
    # f-strings
    'f\'': string_flag,
    'f\"': string_flag,
    # block_comment
    '\"\"\"': block_comment_flag,
    '\'\'\'': block_comment_flag,
    # line comment
    '#': line_comment_flag,
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
    'self': classes_key_words,
    'cls': classes_key_words
}


# stores the first character of the patters, so, while looping the test
# We can start an inspection on the text's sections that starts with one of
# this
POTENTIAL_GLOBAL_PATTERNS = set(map(lambda x: x[0], GLOBAL_PATTERNS.keys()))
POTENTIAL_IN_CLASSES_PATTERNS = set(map(lambda x: x[0], PATTERS_IN_CLASSES.keys()))

#### BLOCKS
# A block will tell us how to treat the remaining text after it is started
# for example, after a line comment start everything in that line must be
# formatted as a line comment, until a line-break escape sequence \n is find
LINE_COMMENT_BLOCK = 'line_comment'
BLOCK_COMMENT_BLOCK = 'block_comment'
F_STRING_BLOCK = 'f_string'
CLASS_BLOCK = 'class'
FUNCTION_DECLARED_BLOCK = 'function'


def potential_pattern(char: str, in_class=False) -> bool:
    """
    Function called whenever we want to know if a character must start
    an inspection, to identify if its a pattern or not.
    """
    if in_class:
        if char in POTENTIAL_IN_CLASSES_PATTERNS or char in POTENTIAL_GLOBAL_PATTERNS:
            return True
    else:
        if char in POTENTIAL_GLOBAL_PATTERNS:
            return True
    return False


# This list defines the characters that, in case we have found a potential
# pattern, produce a pattern, for example, if the current patter founded until
# now is 'from', and the following character is ' ', then we cut the string
# and return 'from' as the founded pattern.
WE_FOUND_A_PATTERN = [' ', '\n', '\t', ',', '(', ')', ':']


def check_potential_pattern(remaining_text: str, in_class: bool) -> tuple:
    """
    Given a text that starts with a potential pattern, we find the next
    character that can probably tell us whether that potential pattern is
    actually a pattern or not, if it is, we return the pattern, the
    remaining text and True
    """
    pattern, flags = '', ''
    winner_index = ''
    for c in WE_FOUND_A_PATTERN:
        try:
            idx = remaining_text.index(c)
        except ValueError:
            continue
        else:
            if winner_index:
                if idx < winner_index:
                    winner_index = idx
            else:
                winner_index = idx

    if winner_index:
        pattern = remaining_text[:winner_index]
    else:
        pattern = remaining_text
        remaining_text = ''

    if pattern not in GLOBAL_PATTERNS.keys():
        if not in_class:
            remaining_text = remaining_text[winner_index:] if remaining_text else ''
        else:
            flags = PATTERS_IN_CLASSES[pattern]
            remaining_text = remaining_text[winner_index:] if remaining_text else ''
    else:
        flags = GLOBAL_PATTERNS[pattern]
        remaining_text = remaining_text[winner_index:] if remaining_text else ''

    return list(pattern), remaining_text, in_class, flags


def define_pattern(remaining_text: str, current_block: str, in_class: bool) -> tuple:
    """
    Once we declare a character as a potential pattern, we need to start a block
    and figure out what special pattern it is, and what action to execute.

    for instance, if we find that character finally ends up being a 'class',
    we start a block called 'CLASS', so we can integrate some other patterns in
    the list (POTENTIAL_IN_CLASSES_PATTERNS), or, if it is an f-string, then we
    need to ensure that everything inside a {} is formatted as regular python
    and not as string.
    """

    pattern, block, remaining_text, flags = [], current_block, remaining_text, ''

    if current_block == FUNCTION_DECLARED_BLOCK:
        flags = function_declared_flag

    for c in range(0, len(remaining_text)):
        char = remaining_text[c]
        if potential_pattern(char, in_class):
            # Now, if the current pattern is already filled, that means that
            # when we start looping the the first character was not a pattern
            # so we need to return that as a pattern with no flags or formats
            # to apply
            if len(pattern) > 0:
                remaining_text = remaining_text[c:]
                break
            else:
                pattern, remaining_text, in_class, flags = check_potential_pattern(remaining_text, in_class)
                if pattern == 'def':
                    block = FUNCTION_DECLARED_BLOCK
                break
        else:
            pattern.append(char)
            continue
    return ''.join(pattern), block, remaining_text, in_class, flags


def get_syntax_as_tuples(text: str) -> list:
    """
    return a list of tuples containing the patterns and the formats to be
    applied to each of them

    for example, taking the text 'from printy import printy' should return
    [('from', 'r'), ('', ''), ('printy', None), ('', ''), ('import', 'r'), ('', ''), ('printy', None)]
    """
    current_block, in_class = None, False
    list_of_tuples = []
    remaining_text = text
    while len(remaining_text) > 0:
        pattern, current_block, remaining_text, in_class, flags = define_pattern(remaining_text, current_block, in_class)

        list_of_tuples.append((pattern, flags))
    return list_of_tuples


