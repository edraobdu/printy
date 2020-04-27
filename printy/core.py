import platform

from .exceptions import InvalidInputType
from .flags import Flags

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
    def _check_special_char_position(cls, last_special: str,
                                     special: str) -> str:

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
                action = cls._check_special_char_position(last_special_char,
                                                          char)

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

    def get_formatted_text(self, value: str, flags='', predefined='',
                           **kwargs) -> str:
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

    def format(self, value='', flags='', predefined='', file='',
               end=default_end):
        """ Prints out the value """
        value = self.read_file(file) if file else value
        print(self.get_formatted_text(value, flags, predefined), end=end)

    ##### ============= INPUTY ======================

    # Types (str is the default)
    BOOL = 'bool'
    INT = 'int'
    FLOAT = 'float'
    STR = 'str'
    types = [BOOL, INT, FLOAT, STR]

    def check_boolean(self, value: str, options: dict, condition: str) -> tuple:
        """
        Validates the value when the type must be a boolean, returns a boolean
        specifying whether it is a valid value, and if it is, returns the final
        value (after conversions if necessary)
        """

        true_value, false_value = options["1"], options["2"]
        error_msg = "[o]%s@ is not a valid value, enter %s or %s" % (
            value,
            true_value,
            false_value,
        )
        if condition == 'i':
            true_value = true_value.lower()
            false_value = false_value.lower()
            value = value.lower()

        if value == true_value:
            return True, True
        elif value == false_value:
            return False, True
        else:
            self.format(error_msg)
            return False, False

    def check_integer(self, value: str, condition: str) -> tuple:
        """
        Validates the value when the type must be an integer, returns a boolean
        specifying whether it is a valid value, and if it is, returns the final
        value (after conversions if necessary)
        """
        # the only options allowed for integer types are '+' and '-'
        error_msg = (
                "[o]%s@ is not a valid number,please enter a [b]rounded@"
                " number, please check you are not adding some "
                "decimal digits" % value
        )
        if condition in ['+', '-']:
            error_msg += ', make sure also it is a [y]%s@ number' % (
                'positive' if condition == '+' else 'negative'
            )
        # Let's try to convert it to integer
        valid_value = False
        try:
            value = int(value)
        except (ValueError, TypeError):
            self.format(error_msg)
        else:
            if condition:
                if condition == '+' and value >= 0:
                    valid_value = True
                elif condition == '-' and value < 0:
                    valid_value = True
                else:
                    self.format(error_msg)
                    valid_value = False
            else:
                valid_value = True

        return value, valid_value

    def check_float(self, value: str, condition: str) -> tuple:
        """
        Validates the value when the type must be an float, similar to integer check,
        but now it can have decimal digits, returns a boolean specifying whether it
        is a valid value, and if it is, returns the final
        value (after conversions if necessary)
        """
        # Same integer options are allowed
        error_msg = "[o]%s@ is not a valid number" % value
        if condition in ['+', '-']:
            error_msg += ', make sure also it is a [y]%s@ number' % (
                'positive' if condition == '+' else 'negative'
            )
        # Let's try to convert it to integer
        valid_value = False
        try:
            value = float(value)
        except (ValueError, TypeError):
            self.format(error_msg)
        else:
            if condition:
                if condition == '+' and value >= 0:
                    valid_value = True
                elif condition == '-' and value < 0:
                    valid_value = True
                else:
                    valid_value = False
            else:
                valid_value = True

        return value, valid_value

    def check_string(self, value: str, options: dict, condition: str):
        """
        if options were passed, then it validates that the value belongs to
        those options
        """
        error_msg = "[o]%s@ is not a valid value" % value
        if options:
            if condition == 'i':
                # then we need to create a dictionary where the keys are the
                # lowercase of the options' values, and the values are the
                # options' keys
                new_options = {}
                for key, val in options.items():
                    new_options[val.lower()] = key
                value = value.lower()

                if value in new_options.keys():
                    return options[new_options[value]], True
                elif value in options.keys():
                    return options[value], True
                else:
                    self.format(error_msg)
                    return value, False
            else:
                if value in options.values():
                    return value, True
                elif value in options.keys():
                    return options[value], True
                else:
                    self.format(error_msg)
                    return value, False
        else:
            return value, True

    @classmethod
    def _render_options(cls, options: dict, input_type: str, default: str,
                        render_options: bool) -> str:
        """
        Returns a string to present to the user specifying the available
        options. 'options' must be normalized.
        """
        render = ""
        if render_options:
            if options and input_type in [cls.STR, cls.BOOL]:
                if input_type == cls.BOOL:
                    if len(options) >= 2:
                        render += " (%s/%s)" % (options['1'], options['2'])
                    if default:
                        # We escape the '[' and ']' so they can be formatted
                        render += " \[%s\]" % default
                else:
                    render += " default: %s\n" % default
                    for item, value in options.items():
                        render += "  %s) %s\n" % (item, value)

        return render

    @classmethod
    def _normalize_options(cls, options: list, input_type: str):
        """
        Takes the list passed as options and returns a dictionary enumerating
        all the options, i.e. if we pass ['option_1', 'options_2'], then we
        return {'1': 'option_1', '2': 'option_2'}
        """
        normalized_options = {}
        if options is not None:
            if input_type == cls.BOOL:
                if len(options) < 2:
                    options = ['True', 'False']
                else:
                    options = options[:2]
            else:
                if len(options) < 2:
                    raise ValueError("'options' must contain at least two items")
        else:
            options = ['True', 'False'] if input_type == cls.BOOL else []

        for option in range(len(options)):
            normalized_options[str(option + 1)] = str(options[option])

        return normalized_options

    def format_input(self, *args, **kwargs):
        """
        Colorize the text prompted by input() and applies some validation.

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

        # A list containing the value valid values
        options = kwargs.get('options', None)
        # render_options defines whether the options should be rendered or not
        render_options = kwargs.get('render_options', True)
        # when no value is entered, the default will be added
        default = str(kwargs.get('default', ''))
        # Tells us the conditions according to the type, for numbers
        # we can say '+' or '-' whether we want only positives values or negative
        # values, for strings and boolean we can specify 'i' if we want to allow
        # user to type cas insensitive values
        condition = str(kwargs.get('condition', ''))

        # Include the value for the get_formatted_text function
        text, flags = '', ''
        if len(args) == 0:
            args = [text, flags]
        elif len(args) == 1:
            text = args[0]
        else:
            text, flags = args[0], args[1]

        # Normalize the options
        options = self._normalize_options(options, input_type)
        # Will tell us whether the user sent a value value according to the
        # specified type or not
        valid_value = False
        result = None
        while not valid_value:
            render_options = self._render_options(options, input_type, default, render_options)
            # Prints out the message if any was passed
            result = str(
                input(
                    self.get_formatted_text(*args, **kwargs)
                    + self.get_formatted_text(render_options, flags)
                )
            )

            if result == '':
                result = default

            if input_type == self.BOOL:
                result, valid_value = self.check_boolean(result, options, condition)

            elif input_type == self.INT:
                result, valid_value = self.check_integer(result, condition)

            elif input_type == self.FLOAT:
                result, valid_value = self.check_float(result, condition)

            else:
                result, valid_value = self.check_string(result, options, condition)

        return result
