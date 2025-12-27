import platform

from .flags import Flags

LINUX = "Linux"
WINDOWS = "Windows"
OSX = "Darwin"

# For format() and format_input()
default_end = "\n"


class Printy:
    """
    Applies a format to the output of the print statement according
    to the flag (or flags).

    We can either set a global set of flags like >>> printy('Some text', 'rB')
    or set inline formats with the especial characters
    like >>> printy('[rB]Some@ [y]text@')
    """

    # For inline formatting we'll use special characters to catch the flags
    end_format_char = "@"
    open_flag_char = "["
    close_flag_char = "]"
    special_chars = [end_format_char, open_flag_char, close_flag_char]

    # Actions for inline formats
    START_FLAGS = "start_flags"
    START_FORMAT = "start_format"
    END_FORMAT = "end_format"
    ESCAPE_CHAR = "escape_char"

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

                k = windll.kernel32  # pragma: no cover
                k.SetConsoleMode(k.GetStdHandle(-11), 7)  # pragma: no cover
                return True  # pragma: no cover
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
            if prev != "\\":
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
        """Replaces escaped special characters for the character itself"""
        for special_char in cls.special_chars:
            text = text.replace("\\" + special_char, special_char)
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
        prev = ""  # Stores the last character in the loop
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
                    if current_action == cls.START_FLAGS:  # pragma: no cover
                        section_flags.append(char)  # pragma: no cover
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
                list_of_formats.append(
                    (
                        "".join(section_text),
                        "".join(section_flags) if len(section_flags) > 0 else None,
                    )
                )
                section_text = []
                section_flags = []
                close_section = False

        return list_of_formats

    @classmethod
    def _get_cleaned_text(cls, text: str) -> str:
        """Returns the cleaned value, with no formats"""
        tuple_text = cls._get_inline_format_as_tuple(text)
        return cls._replace_escaped("".join(x[0] for x in tuple_text))

    @classmethod
    def _escape_special_chars(cls, value):
        """
        Escape all the special characters in the value (or the string
        representation of the value if an object is passed)
        """
        _str = str(value)
        for char in cls.special_chars:
            _str = _str.replace(char, "\\" + char)
        return _str

    @classmethod
    def _pretty_print_object(cls, obj, indentation: int, level: int = 1) -> str:
        """
        Recursive function to pretty print objects, with some
        indentations if needed.
        """

        def _nested(nested_obj, nested_level: int = level) -> str:
            indentation_values = " " * indentation * nested_level
            indentation_braces = " " * indentation * (nested_level - 1)
            if isinstance(nested_obj, dict):
                return "{\n%(body)s%(indent_braces)s}" % {
                    "body": "".join(
                        "%(indent_values)s[n>]'%(key)s'@: %(value)s[<oB],@\n"
                        % {
                            "key": str(key),
                            "value": _nested(value, nested_level + 1),
                            "indent_values": indentation_values,
                        }
                        for key, value in nested_obj.items()
                    ),
                    "indent_braces": indentation_braces,
                }
            elif isinstance(nested_obj, list):
                return "\\[\n%(indent_values)s%(body)s\n%(indent_braces)s\\]" % {
                    "body": "[<oB],@ ".join(
                        "%(value)s"
                        % {
                            "value": _nested(value, nested_level + 1),
                        }
                        for value in nested_obj
                    ),
                    "indent_braces": indentation_braces,
                    "indent_values": indentation_values,
                }
            elif isinstance(nested_obj, tuple):
                return "(\n%(indent_values)s%(body)s\n%(indent_braces)s)" % {
                    "body": "[<oB],@ ".join(
                        "%(value)s"
                        % {
                            "value": _nested(value, nested_level + 1),
                        }
                        for value in nested_obj
                    ),
                    "indent_braces": indentation_braces,
                    "indent_values": indentation_values,
                }
            elif isinstance(nested_obj, set):
                return "{\n%(indent_values)s%(body)s\n%(indent_braces)s}" % {
                    "body": "[<oB],@ ".join(
                        "%(value)s"
                        % {
                            "value": _nested(value, nested_level + 1),
                        }
                        for value in nested_obj
                    ),
                    "indent_braces": indentation_braces,
                    "indent_values": indentation_values,
                }
            else:
                if isinstance(nested_obj, str):
                    return "[c>]'" + cls._escape_special_chars(nested_obj) + "'@"
                elif isinstance(nested_obj, bool) or nested_obj is None:
                    return "[<o]" + cls._escape_special_chars(nested_obj) + "@"
                elif isinstance(nested_obj, (int, float)):
                    return "[c]" + str(nested_obj) + "@"
                else:
                    return str(nested_obj)

        return _nested(obj)

    @classmethod
    def _repr_value(cls, value, pretty: bool = True, indentation: int = 4) -> str:
        """
        In case a dictionary or a list or a set is passed as a value, we need
        to get the representation of it, and, escape all the '[', ']' and '@'
        characters that we find
        """
        if isinstance(value, (dict, list, tuple, set)):
            if pretty:
                return cls._pretty_print_object(value, indentation)
            else:
                return cls._escape_special_chars(value)
        elif isinstance(value, bool) or value is None:
            return "[<o]" + str(value) + "@"
        elif isinstance(value, (int, float)):
            return "[c]" + str(value) + "@"
        else:
            return str(value)

    def get_formatted_text(
        self,
        value: str,
        flags: str = "",
        predefined: str = "",
        pretty: bool = True,
        indentation: int = 4,
        **kwargs,
    ) -> str:
        """
        Applies the format specified by the 'flags' to the 'value'.

        If 'flag's is passed, 'predefined' will be omitted.
        """
        # In case an object is passed instead of a string
        value = self._repr_value(value, pretty, indentation)

        if self.platform == WINDOWS and not self.virtual_terminal_processing:
            text = self._get_cleaned_text(value)
        else:
            if flags:
                flags_values = Flags.get_flag_values(flags)
                value = self._get_cleaned_text(value)
                text = "%s%s%s" % (
                    Flags.join_flags(flags_values),
                    value,
                    Flags.get_end_of_line(),
                )
            else:
                tuple_text = self._get_inline_format_as_tuple(value)
                text = ""
                for section in tuple_text:
                    section_text = self._replace_escaped(section[0])
                    section_flags = section[1] or predefined
                    if section_flags:
                        flags_values = Flags.get_flag_values(section_flags)
                        text += "%s%s%s" % (
                            Flags.join_flags(flags_values),
                            section_text,
                            Flags.get_end_of_line(),
                        )
                    else:
                        text += section_text
        return text

    @staticmethod
    def read_file(file: str) -> str:
        """Given a file path, we read it and print it out"""
        file = str(file)
        with open(file) as f:
            text = f.read()
        return text

    def format(
        self,
        value="",
        flags="",
        predefined="",
        file="",
        end=default_end,
        pretty=True,
        indentation=4,
    ):
        """Prints out the value"""
        value = self.read_file(file) if file else value
        print(
            self.get_formatted_text(value, flags, predefined, pretty, indentation),
            end=end,
        )

    def escape(self, value):
        """
        Escape the special characters of the value passed to printy. Useful
        for untrusted sources.
        """
        for char in self.special_chars:
            value = value.replace(char, r"\{}".format(char))
        return value
