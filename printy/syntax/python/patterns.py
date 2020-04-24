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
key_words_flag = '<o'
builtin_flag = 'p>'
decorator_flag = 'y'
string_flag = 'n>'
number_flag = 'c'
line_comment_flag = 'g'
block_comment_flag = 'n>I'
function_declared_flag = 'y>'
# In classes
builtin_methods_flag = '<m'
# like cls, self
classes_key_words = 'm'
equal_flag = None


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
    'tuple': builtin_flag,
    'filter': builtin_flag,
    'range': builtin_flag,
    'set': builtin_flag,
    'dir': builtin_flag,
    'vars': builtin_flag,
    'object': builtin_flag,
    'Exception': builtin_flag,
    'TypeError': builtin_flag,
    'ValueError': builtin_flag,
    'SyntaxError': builtin_flag,
    'KeyError': builtin_flag,
    'ImportError': builtin_flag,

    ### Other paters

    # Decorator
    '@': decorator_flag,
    # line comment
    '#': line_comment_flag,
}

# Patters that are only valid within a class definition
PATTERNS_IN_CLASSES = {
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

# When we found a '\' in a regular string
# we can say we found a potential escape sequence
# so we need to determine whether it is one of them or not
PATTERNS_ESCAPE_SEQUENCES = {
    '\\\\': key_words_flag,
    '\\\'': key_words_flag,
    '\\\"': key_words_flag,
    '\\\a': key_words_flag,
    '\\\b': key_words_flag,
    '\\\f': key_words_flag,
    '\\\n': key_words_flag,
    '\\\r': key_words_flag,
    '\\\t': key_words_flag,
}


# stores the first character of the patters, so, while looping the test
# We can start an inspection on the text's sections that starts with one of
# this
POTENTIAL_GLOBAL_PATTERNS = set(map(lambda x: x[0], GLOBAL_PATTERNS.keys()))
POTENTIAL_IN_CLASSES_PATTERNS = set(map(lambda x: x[0], PATTERNS_IN_CLASSES.keys()))

#### BLOCKS
# A block will tell us how to treat the remaining text after it is started
# for example, after a line comment start everything in that line must be
# formatted as a line comment, until a line-break escape sequence \n is find
LINE_COMMENT_BLOCK = 'line_comment'
BLOCK_COMMENT_BLOCK = 'block_comment'
REGULAR_STRING = 'string'
F_STRING_BLOCK = 'f_string'
CLASS_BLOCK = 'class'
FUNCTION_DECLARED_BLOCK = 'function'
DECORATOR_BLOCK = 'decorator'
NUMBER_BLOCK = 'number'


def potential_pattern(char: str, block: str) -> bool:
    """
    Function called whenever we want to know if a character must start
    an inspection, to identify if its a pattern or not.
    """
    if block == CLASS_BLOCK:
        if char in POTENTIAL_IN_CLASSES_PATTERNS or char in POTENTIAL_GLOBAL_PATTERNS:
            return True
    elif block == FUNCTION_DECLARED_BLOCK:
        # This means that everything after the 'def' keyword, would be taken
        # as the function_name (only if it's a character that is not in the
        # WE_FOUND_A_PATTERN list (except the first whit-spaces if any)
        return True
    else:
        if char in ['\'', '\"', '=']:
            return True
        elif char in POTENTIAL_GLOBAL_PATTERNS:
            return True

        # If the character can be converted into a number, then it
        # is a potential pattern
        try:
            int(char)
        except (ValueError, TypeError):
            pass
        else:
            return True
    return False


# This list defines the characters that, in case we have found a potential
# pattern, produce a pattern, for example, if the current patter founded until
# now is 'from', and the following character is ' ', then we cut the string
# and return 'from' as the founded pattern.
WE_FOUND_A_PATTERN = [' ', '\n', '\t', ',', '(', ')', ':', '=']


def check_potential_pattern(remaining_text: str, block: str) -> tuple:
    """
    Given a text that starts with a potential pattern, we find the next
    character that can probably tell us whether that potential pattern is
    actually a pattern or not, if it is, we return the pattern, the
    remaining text and True
    """
    pattern, flags = '', ''
    winner_index = ''

    # First, we need to know if we are dealing with a string or a block comment
    # or non of them.
    # A string will be catch when the first character is either ' or ", and the
    # following character is different than those. In case the following char
    # is different that ' or ", then it is just a regular string
    first_char = remaining_text[0]
    first_three_chars = remaining_text[:3]

    if first_char == '\'':
        # check the first 3 characters
        if first_char == '\'' and first_three_chars == '\'\'\'':
            # Then it is a block comment  and we need to look up the
            # next three ''' in the text
            block = BLOCK_COMMENT_BLOCK
        else:
            block = REGULAR_STRING
    elif first_char == '\"':
        if first_char == '\"' and first_three_chars == '\"\"\"':
            # then is also a block comment
            block = BLOCK_COMMENT_BLOCK
        else:
            block = REGULAR_STRING
    else:
        try:
            int(first_char)
        except (ValueError, TypeError):
            pass
        else:
            # Stars a number block
            block = NUMBER_BLOCK

    # Only for FUNCTION_DECLARED_BLOCK
    white_space_at_the_beginning = False
    if block in [FUNCTION_DECLARED_BLOCK, DECORATOR_BLOCK]:
        # we omit the the white spaces at the beginning of the function name
        white_space_at_the_beginning = remaining_text[0] in [' ']
        if white_space_at_the_beginning:
            remaining_text = remaining_text[1:]

    # Only for strings and block comments
    quotes_at_the_beginning = ''

    if block == LINE_COMMENT_BLOCK:
        # Then this pattern will end only when a line break is found
        try:
            winner_index = remaining_text.index('\n')
        except ValueError:
            # In case it is at the end of the string and no '\n' is found
            winner_index = None

    elif block == REGULAR_STRING:
        remaining_text = remaining_text[1:]
        quotes_at_the_beginning = first_char

        # Let's try to detect if the quote is a escaped one or if
        # it is the end of the string
        # get the index of the 'ending' quote
        winner_index = remaining_text.index(first_char)
        # get the previous character
        escape_quote = remaining_text[winner_index - 1]
        while escape_quote == '\\':
            # if its the escape character, then we keep adding the index
            # (+ 1 because indexes starts at 0) to the winner_index
            winner_index += remaining_text[winner_index + 1:].index(first_char) + 1
            escape_quote = remaining_text[winner_index - 1]
        # the next character after the match
        winner_index += 1

    elif block == BLOCK_COMMENT_BLOCK:
        remaining_text = remaining_text[3:]
        quotes_at_the_beginning = first_three_chars
        winner_index = remaining_text.index(first_three_chars) + 3

    else:
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

    if block in [FUNCTION_DECLARED_BLOCK, DECORATOR_BLOCK]:
        flags = function_declared_flag if block == FUNCTION_DECLARED_BLOCK else decorator_flag
        # then we stop the block
        block = None
        # and also add the whit space at the beginning if any
        if white_space_at_the_beginning:
            pattern = ' ' + pattern
        remaining_text = remaining_text[winner_index:] if remaining_text else ''

    elif block == LINE_COMMENT_BLOCK:
        block = None
        flags = line_comment_flag
        remaining_text = remaining_text[winner_index:] if remaining_text else ''

    elif block == BLOCK_COMMENT_BLOCK:
        block = None
        flags = block_comment_flag
        pattern = quotes_at_the_beginning + pattern
        remaining_text = remaining_text[winner_index:] if remaining_text else ''

    elif block == REGULAR_STRING:
        block = None
        flags = string_flag
        pattern = quotes_at_the_beginning + pattern
        remaining_text = remaining_text[winner_index:] if remaining_text else ''

    elif block == NUMBER_BLOCK:
        block = None
        flags = number_flag
        remaining_text = remaining_text[winner_index:] if remaining_text else ''

    else:
        if pattern not in GLOBAL_PATTERNS.keys():
            if block != CLASS_BLOCK:
                remaining_text = remaining_text[winner_index:] if remaining_text else ''
            else:
                flags = PATTERNS_IN_CLASSES[pattern]
                remaining_text = remaining_text[winner_index:] if remaining_text else ''
        else:
            flags = GLOBAL_PATTERNS[pattern]
            remaining_text = remaining_text[winner_index:] if remaining_text else ''

    return list(pattern), remaining_text, block, flags


def define_pattern(remaining_text: str, current_block: str) -> tuple:
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

    for c in range(0, len(remaining_text)):
        char = remaining_text[c]
        if char == ',':
            # In the case of the ',', it will pass immediately as a patterns, unless it
            # it is inside a comment block
            if block not in [LINE_COMMENT_BLOCK, BLOCK_COMMENT_BLOCK]:
                pattern, remaining_text, flags = [char], remaining_text[c + 1:], key_words_flag
                break
        if potential_pattern(char, block):
            # Now, if the current pattern is already filled, that means that
            # when we start looping the the first character was not a pattern
            # so we need to return that as a pattern with no flags or formats
            # to apply
            if len(pattern) > 0:
                remaining_text = remaining_text[c:]
                break
            elif char == '=':
                remaining_text = remaining_text[c + 1:]
                pattern = [char]
                flags = equal_flag
                break
            else:
                if char == '#':
                    block = LINE_COMMENT_BLOCK
                elif char == '@':
                    block = DECORATOR_BLOCK

                pattern, remaining_text, block, flags = check_potential_pattern(remaining_text, block)

                if ''.join(pattern) == 'def':
                    block = FUNCTION_DECLARED_BLOCK
                break
        else:
            pattern.append(char)

            if ''.join(pattern) == remaining_text:
                # This means that we have reached the end of the text
                remaining_text = ''
            continue
    return ''.join(pattern), block, remaining_text, flags


def get_syntax_as_tuples(text: str) -> list:
    """
    return a list of tuples containing the patterns and the formats to be
    applied to each of them

    for example, taking the text 'from printy import printy' should return
    [('from', 'r'), ('', ''), ('printy', None), ('', ''), ('import', 'r'), ('', ''), ('printy', None)]
    """
    current_block = None
    list_of_tuples = []
    remaining_text = text
    while len(remaining_text) > 0:
        pattern, current_block, remaining_text, flags = define_pattern(remaining_text, current_block)
        list_of_tuples.append((pattern, flags))
    return list_of_tuples
