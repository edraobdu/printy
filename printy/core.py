import platform

from .exceptions import (
    InvalidInputType, BoolOptionsNotValid,
    IntOptionsNotValid, FloatOptionsNotValid
)
from .flags import Flags
from . import syntax as highlight_syntax

LINUX = 'Linux'
WINDOWS = 'Windows'
OSX = 'Darwin'

# For format() and format_input()
default_end = '\n'


class Printy:
    """
    Applies a format to the output of the print statement according
    to the flag (or flags).

    We can either set a global set of flags like >>> printy('Some text', 'rB')
    or set inline formats with the especial characters
    like >>> printy('[rB]Some@ [y]text@')
    """

    # For inline formatting we'll use special characters to catch the flags
    end_format_char = '@'
    open_flag_char = '['
    close_flag_char = ']'
    special_chars = [end_format_char, open_flag_char, close_flag_char]

    # Actions for inline formats
    START_FLAGS = 'start_flags'
    START_FORMAT = 'start_format'
    END_FORMAT = 'end_format'
    ESCAPE_CHAR = 'escape_char'

    def __init__(self):
        self.platform = platform.system()
        self.virtual_terminal_processing = self.set_windows_console_mode()

    def set_windows_console_mode(self):
        """
        For Windows os to work and get the escape sequences correctly,
        we'll need to enable the variable ENABLE_VIRTUAL_TERMINAL_PROCESSING

        @Thanks to Mihir Singh (mihirs16) for this big improvement
        """
        # In case there is some error while setting it up, we returns False to
        # indicate that windows will not print the escape sequences correctly,
        # so we can print out the cleaned text
        if self.platform == WINDOWS:
            try:
                from ctypes import windll
                k = windll.kernel32
                k.SetConsoleMode(k.GetStdHandle(-11), 7)
                return True
            except ImportError:
                return False
        return False

    @classmethod
    def _define_char(cls, prev: str, current: str) -> bool:
        """
        Helper method that'll tell us if a character has to be treated as a
        special one or it is part of the text that 's intended to be printed
        out.

        Takes the previous character and the current character, in case it is
        one of the special characters defined in the class and is prepended by
        a '\' means that it has not to be treated as a special one

        Returns True if it's a special character
        """
        if current in cls.special_chars:
            if prev != '\\':
                return True
        return False

    @classmethod
    def _check_special_char_position(cls, last_special: str, special: str) -> str:
        """
        Returns an action to execute if the character is well placed. It should
        only be applied over special characters.

        If it's not well placed, the character will be included in the text
        """
        if special == cls.open_flag_char:
            # In this case the 'last_special' must always be
            # the 'end_format_char' or None if it's the first appearing
            if last_special not in [cls.end_format_char, None]:
                return cls.ESCAPE_CHAR
            else:
                return cls.START_FLAGS
        elif special == cls.close_flag_char:
            # In this case the 'last_special' must always be the 'open_flag_char'
            if last_special != cls.open_flag_char:
                return cls.ESCAPE_CHAR
            else:
                return cls.START_FORMAT
        elif special == cls.end_format_char:
            # In this case the 'last_special' must always be the 'close_flag_char'
            # Or None if the text does not include any other formatting character
            if last_special in [cls.open_flag_char, cls.end_format_char, None]:
                return cls.ESCAPE_CHAR
            else:
                return cls.END_FORMAT

    @classmethod
    def _replace_escaped(cls, text: str) -> str:
        """ Replaces escaped special characters for the character itself """
        for special_char in cls.special_chars:
            text = text.replace('\\' + special_char, special_char)
        return text

    @classmethod
    def _get_inline_format_as_tuple(cls, text: str) -> list:
        """
        In case some inline formats have been applied we need to get a list of
        tuples indicating the formats to be applied via flags and the text
        where the format should be applied, for instance, if the text is:
        "[rB]Some@ Te[H]xt@"
        We'll get the list [('Some', 'rB), (' Te', None), ('xt', 'H')]
        """
        prev = ''  # Stores the last character in the loop
        last_special_char = None
        list_of_formats = []  # Final list to be returned

        # While looping the text, we'll get the formats to be applied to
        # certain section of that text
        section_text = []
        section_flags = []
        current_action = cls.START_FORMAT

        # Will tell us when we're at the last character of the loop
        counter = 0
        # Will tell us if we need to reset the sections variables
        close_section = False
        for char in text:
            is_special = cls._define_char(prev, char)
            if is_special:
                action = cls._check_special_char_position(last_special_char, char)

                if action == cls.ESCAPE_CHAR:
                    # Add the character to the text
                    if current_action == cls.START_FLAGS:
                        section_flags.append(char)
                    elif current_action == cls.START_FORMAT:
                        section_text.append(char)
                else:
                    # Here we know that the special character is well placed
                    # and has a special meaning
                    current_action = action

                    if current_action == cls.END_FORMAT:
                        current_action = cls.START_FORMAT
                        close_section = True
                    if last_special_char in [cls.end_format_char, None]:
                        # Here we'll catch 'open_flag_char's
                        current_action = cls.START_FLAGS
                        close_section = True
                    last_special_char = char
            else:
                if current_action == cls.START_FLAGS:
                    section_flags.append(char)
                elif current_action == cls.START_FORMAT:
                    section_text.append(char)
            prev = char
            counter += 1

            if counter == len(text) or close_section:
                # Reset the 'section_*' lists and add them (joined)
                # to the final list
                list_of_formats.append((
                    ''.join(section_text),
                    ''.join(section_flags) if len(section_flags) > 0 else None
                ))
                section_text = []
                section_flags = []
                close_section = False

        return list_of_formats

    @classmethod
    def _get_cleaned_text(cls, text: str) -> str:
        """ Returns the cleaned value, with no formats """
        tuple_text = cls._get_inline_format_as_tuple(text)
        return cls._replace_escaped(''.join(x[0] for x in tuple_text))

    def get_formatted_text(self, value: str, flags='', predefined='', syntax='') -> str:
        """
        Applies the format specified by the 'flags' to the 'value'.

        If 'flag's is passed, 'predefined' will be omitted.
        """
        if self.platform == WINDOWS and not self.virtual_terminal_processing:
            text = self._get_cleaned_text(value)
        else:
            if flags:
                flags_values = Flags.get_flag_values(flags)
                value = self._get_cleaned_text(value)
                text = "%s%s%s" % (
                    Flags.join_flags(flags_values),
                    value,
                    Flags.get_end_of_line()
                )
            else:
                if syntax:
                    syntax_lang = getattr(highlight_syntax, syntax, None)
                    if syntax_lang:
                        from importlib import import_module
                        try:
                            syntax_module = import_module('printy.syntax.%s.patterns' % syntax_lang)
                        except ImportError:
                            syntax_module = None

                        if syntax_module:
                            tuple_text = syntax_module.get_syntax_as_tuples(value)
                        else:
                            raise TypeError("%s syntax is not supported" % syntax)
                    else:
                        raise TypeError("%s syntax is not supported" % syntax)
                else:
                    tuple_text = self._get_inline_format_as_tuple(value)

                text = ''
                for section in tuple_text:
                    section_text = self._replace_escaped(section[0])
                    section_flags = section[1] or predefined
                    if section_flags:
                        flags_values = Flags.get_flag_values(section_flags)
                        text += "%s%s%s" % (
                            Flags.join_flags(flags_values),
                            section_text,
                            Flags.get_end_of_line()
                        )
                    else:
                        text += section_text
        return text

    @staticmethod
    def read_file(file: str) -> str:
        """ Given a file path, we read it and print it out """
        file = str(file)
        with open(file) as f:
            text = f.read()
        return text

    def format(self, value='', flags='', predefined='', syntax='', file='', end=default_end):
        """ Prints out the value """
        value = self.read_file(file) if file else value
        print(self.get_formatted_text(value, flags, predefined, syntax), end=end)

    ##### Inputy

    # Types (str is the default)
    BOOL = 'bool'
    INT = 'int'
    FLOAT = 'float'
    STR = 'str'
    types = [BOOL, INT, FLOAT, STR]

    @staticmethod
    def get_bool_options(bool_options):
        """
        Strips the string passed as bool_options and returns the valid values,
        let's say the bool_options = 'i{Y/n}', then it will return a tuple
        containing:
            insensitive, true, false = True, 'Y', 'n'
        """
        insensitive, true_value, false_value = True, True, False
        if bool_options:
            opts = bool_options.replace('{', '-').replace('}', '-').replace('/', '-')
            opts = opts.split('-')
            if '' in opts:
                opts.remove('')
            # It might end up with 2 or 3 values, if its 3, the first one must be
            # the case insensitive indicator 'i'
            if len(opts) == 3 and opts[0] != 'i':
                raise BoolOptionsNotValid(bool_options)
            elif len(opts) > 3 or len(opts) <= 1:
                raise BoolOptionsNotValid(bool_options)
            elif len(opts) == 3:
                insensitive, true_value, false_value = True, opts[1], opts[2]
            else:
                true_value, false_value = opts
                insensitive = False

        return insensitive, true_value, false_value

    @staticmethod
    def get_int_options(int_options):
        """ Checks that only '+' or '-' are passed """
        # the default is None, which will accept any number, positive or negative
        if int_options:
            if len(int_options) > 1:
                raise IntOptionsNotValid(int_options)
            else:
                if int_options in ('+', '-'):
                    return int_options
                else:
                    raise IntOptionsNotValid(int_options)
        return None

    def check_boolean(self, value, bool_options=None):
        """
        Validates the value when the type must be a boolean, returns a boolean
        specifying whether it is a valid value, and if it is, returns the final
        value (after conversions if necessary)
        """
        insensitive, true_value, false_value = self.get_bool_options(bool_options)
        true_value = str(true_value)
        false_value = str(false_value)
        error_msg = "%s is not a valid value, enter %s or %s" % (
            value,
            true_value,
            false_value,
        )
        if insensitive:
            value = value.lower()
            true_value = true_value.lower()
            false_value = false_value.lower()
        if value == true_value:
            return True, True
        elif value == false_value:
            return False, True
        else:
            self.format(error_msg)
            return False, False

    def check_integer(self, value, int_options=None):
        """
        Validates the value when the type must be an integer, returns a boolean
        specifying whether it is a valid value, and if it is, returns the final
        value (after conversions if necessary)
        """
        # the only options allowed for integer types are '+' and '-'
        opt = self.get_int_options(int_options)
        error_msg = (
            "%s is not a valid number,please enter a [b]rounded@"
            " number, please check you are not adding some "
            "decimal digits" % value
        )
        if opt:
            error_msg += ', make sure also it is a %s number' % (
                'positive' if opt == '+' else 'negative'
            )
        # Let's try to convert it to integer
        valid_value = False
        try:
            value = int(value)
        except (ValueError, TypeError):
            self.format(error_msg)
        else:
            if opt:
                if opt == '+' and value >= 0:
                    valid_value = True
                elif opt == '-' and value < 0:
                    valid_value = True
                else:
                    valid_value = False
            else:
                valid_value = True

        return value, valid_value

    def check_float(self, value, float_options=None):
        """
        Validates the value when the type must be an float, similar to integer check,
        but now it can have decimal digits, returns a boolean specifying whether it
        is a valid value, and if it is, returns the final
        value (after conversions if necessary)
        """
        # Same integer options are allowed
        opt = self.get_int_options(float_options)
        error_msg = (
            "%s is not a valid number" % value
        )
        if opt:
            error_msg += ', make sure also it is a %s number' % (
                'positive' if opt == '+' else 'negative'
            )
        # Let's try to convert it to integer
        valid_value = False
        try:
            value = float(value)
        except (ValueError, TypeError):
            self.format(error_msg)
        else:
            if opt:
                if opt == '+' and value >= 0:
                    valid_value = True
                elif opt == '-' and value < 0:
                    valid_value = True
                else:
                    valid_value = False
            else:
                valid_value = True

        return value, valid_value

    def format_input(self, *args, **kwargs):
        """
        Colorize the text prompted by input().

        Also, it takes an additional parameter 'type', to tell the prompt not
        to accept a format other than the specified. As every input is converted
        to strings, a string that can be converted to the specified type is
        allowed. For example, if type=int, then the user would be forced to
        enter a number or a string that can be converted into an integer
        """

        # If passed, we'll force the user to write a value with the specific
        # input_types' format.
        input_type = kwargs.get('type', self.STR)
        if input_type not in self.types:
            raise InvalidInputType(input_type)

        # bool_options will override the default True/False
        # it has to be passed as a string with the following syntax:
        # bool_options="i{True/False}", where 'i', if passed, will tell us
        # that the values are case insensitive, otherwise, values will be forced
        # to a exact match
        options = kwargs.get('options', '')
        # when no value is entered, the default will be added
        default = kwargs.get('default', '')

        # remove extra parameters so we don't pass it to
        # the get_formatted_text function
        if 'type' in kwargs:
            kwargs.pop('type')
        if 'options' in kwargs:
            kwargs.pop('options')

        # Include the value for the get_formatted_text function
        if len(args) == 0:
            args = ['']

        # Will tell us whether the user sent a value value according to the
        # specified type or not
        valid_value = False
        result = None
        while not valid_value:
            # Prints out the message if any was passed
            result = str(input(self.get_formatted_text(*args, **kwargs)))

            if result == '':
                result = default

            if input_type == self.BOOL:
                # now let's try to convert the value to a Boolean
                result, valid_value = self.check_boolean(result, options)

            elif input_type == self.INT:
                # Let's try to convert it to integer
                result, valid_value = self.check_integer(result, options)

            elif input_type == self.FLOAT:
                # Almost the same for integer, but this time it just have to
                # be a number, rounded or not
                result, valid_value = self.check_float(result, options)
            else:
                result, valid_value = str(result), True

        return result
