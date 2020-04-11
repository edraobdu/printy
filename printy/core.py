import os
import platform

from .exceptions import InvalidFlag


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
        self.flags = self._get_flags()
        self.platform = platform.system()

    #### COLORS
    GREY = 'g', '\033[90m'
    RED = 'r', '\033[31m'
    GREEN = 'n', '\033[92m'
    YELLOW = 'y', '\033[93m'
    BLUE = 'b', '\033[34m'
    MAGENTA = 'm', '\033[95m'
    CYAN = 'c', '\033[96m'
    BLACK = 'k', '\033[97m'
    PREDEFINED = 'p', '\033[98m'

    #### FORMATS
    BOLD = 'B', '\033[1m'
    ITALIC = 'I', '\033[3m'
    UNDERLINE = 'U', '\033[4m'
    HIGHLIGHT = 'H', '\033[7m'

    #### END OF LINE
    end_of_line = '\033[0m'

    @classmethod
    def _get_flags(cls):
        """
        returns a dictionary where the flag is the key and the attribute
        name is the value
        """
        return {y[0]: x for x, y in vars(cls).items() if x.isupper()}

    def get_flag_values(self, flags):
        """ returns a list of the escaped values for the flag labels """
        flags_values = []
        for flag in flags.replace(' ', ''):
            if flag not in self.flags:
                raise InvalidFlag(flag)
            else:
                if hasattr(self, self.flags[flag]):
                    flags_values.append(getattr(self, self.flags[flag])[1])
        return flags_values

    @classmethod
    def _define_char(cls, prev, current):
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
    def _check_special_char_position(cls, last_special, special):
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
    def _replace_escaped(cls, text):
        """ Replaces escaped special characters for the character itself """
        for special_char in cls.special_chars:
            text = text.replace('\\' + special_char, special_char)
        return text

    @classmethod
    def _get_inline_format_as_tuple(cls, text):
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
    def _get_cleaned_text(cls, text):
        """ Returns the cleaned value, with no formats """
        tuple_text = cls._get_inline_format_as_tuple(text)
        return cls._replace_escaped(''.join(x[0] for x in tuple_text))

    def get_formatted_text(self, value, flags=None, default=None):
        """
        Applies the format specified by the 'flags' to the 'value'.

        If 'flag's is passed, 'default' will be omitted.
        """
        if flags:
            flags_values = self.get_flag_values(flags)
            value = self._get_cleaned_text(value)
            text = f"{''.join(flags_values)}{value}{self.end_of_line}"
        else:
            tuple_text = self._get_inline_format_as_tuple(value)
            text = ''
            for section in tuple_text:
                section_text = self._replace_escaped(section[0])
                section_flags = section[1] or default
                if section_flags:
                    flags_values = self.get_flag_values(section_flags)
                    text += f"{''.join(flags_values)}{section_text}{self.end_of_line}"
                else:
                    text += section_text
        return text

    def format(self, value, flags=None, default=None):
        """ Prints out the value """
        print(self.get_formatted_text(value, flags, default))
