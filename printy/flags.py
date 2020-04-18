from .exceptions import InvalidFlag


class Flags:

    escape_ansi_code = '\x1b['
    escape_ansi_end = 'm'

    #### COLORS (FG CODES)
    BLACK = 'k', '30'
    RED = 'r', '31'
    GREEN = 'n', '32'
    YELLOW = 'y', '33'
    BLUE = 'b', '34'
    MAGENTA = 'm', '35'
    CYAN = 'c', '36'
    WHITE = 'w', '37'
    GREY = 'g', '90'

    DEFAULT = 'p', '10'

    #### FORMATS
    BOLD = 'B', '1'
    DIM = 'D', '2'
    ITALIC = 'I', '3'
    UNDERLINE = 'U', '4'
    HIGHLIGHT = 'H', '7'
    STRIKE = 'S', '9'

    #### END OF LINE
    reset = '0'

    @classmethod
    def get_end_of_line(cls):
        """ Defined method to get the 'reset' code """
        return cls.escape_ansi_code + cls.reset + cls.escape_ansi_end

    @classmethod
    def join_flags(cls, flags):
        """ Given a set of flags, returned the final ansi code to add to the text"""
        return "%s%s%s" % (cls.escape_ansi_code, ';'.join(flags), cls.escape_ansi_end)

    @classmethod
    def get_flags(cls):
        """
        returns a dictionary where the flag is the key and the attribute
        name is the value
        """
        return {y[0]: x for x, y in vars(cls).items() if x.isupper() and isinstance(y, tuple) and len(y[0]) == 1}

    @classmethod
    def get_flag_values(cls, flags):
        """ returns a list of the escaped values for the flag labels """
        available_flags = cls.get_flags()
        flags_values = []
        for flag in flags.replace(' ', ''):
            if flag not in available_flags:
                raise InvalidFlag(flag)
            else:
                if hasattr(cls, available_flags[flag]):
                    flags_values.append(getattr(cls, available_flags[flag])[1])
        return flags_values

    @classmethod
    def get_formatted_text(cls, value, flags):
        if flags:
            return "%s%s%s" % (
                cls.join_flags(cls.get_flag_values(flags)),
                value,
                cls.get_end_of_line()
            )
        return value

