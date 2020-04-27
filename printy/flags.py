from .exceptions import InvalidFlag


class Flags:

    escape_ansi_code = '\x1b['
    escape_ansi_end = 'm'

    start_foreground = '38;5;'

    #### COLORS

    # Gray Scale
    BLACK = 'k', start_foreground + '16'
    GRAY = 'g', start_foreground + '243'
    WHITE = 'w', start_foreground + '15'

    # Red Scale
    DARKRED = '<r', start_foreground + '88'
    RED = 'r', start_foreground + '196'
    LIGHTRED = 'r>', start_foreground + '9'

    # Green Scale
    DARKGREEN = '<n', start_foreground + '22'
    GREEN = 'n', start_foreground + '28'
    LIGHTGREEN = 'n>', start_foreground + '65'

    # Yellow Scale
    DARKYELLOW = '<y', start_foreground + '58'
    YELLOW = 'y', start_foreground + '11'
    LIGHTYELLOW = 'y>', start_foreground + '3'

    # Blue Scale
    DARKBLUE = '<b', start_foreground + '17'
    BLUE = 'b', start_foreground + '20'
    LIGHTBLUE = 'b>', start_foreground + '4'

    # Magenta Scale
    DARKMAGENTA = '<m', start_foreground + '125'
    MAGENTA = 'm', start_foreground + '198'
    LIGHTMAGENTA = 'm>', start_foreground + '13'

    # Cyan Scale
    DARKCYAN = '<c', start_foreground + '30'
    CYAN = 'c', start_foreground + '39'
    LIGHTCYAN = 'c>', start_foreground + '51'

    # Orange Scale
    DARKORANGE = '<o', start_foreground + '130'
    ORANGE = 'o', start_foreground + '208'
    LIGHTORANGE = 'o>', start_foreground + '214'

    # Purple Scale
    DARKPURPLE = '<p', start_foreground + '54'
    PURPLE = 'p', start_foreground + '91'
    LIGHTPURPLE = 'p>', start_foreground + '98'

    #### FORMATS
    BOLD = 'B', '1'
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
        return {y[0]: x for x, y in vars(cls).items() if x.isupper() and isinstance(y, tuple)}

    @classmethod
    def get_flag_values(cls, flags):
        """ returns a list of the escaped values for the flag labels """
        available_flags = cls.get_flags()
        flags_values = []

        # New in v1.3.0
        # flags can get a dark or a light intensity through the '<' and '>'
        # characters respectively. Dark colors have the form: <color, i.e. <b
        # light colors have the form color>, i.e. b>
        potential_flag = []
        flags = flags.replace(' ', '')  # remove white-spaces
        # We use inspect so we can check the following character also
        for f in range(len(flags)):
            flag = flags[f]

            if flag == '<':
                potential_flag.append(flag)
                continue
            elif flag == '>':
                potential_flag.append(flag)
                flag = ''.join(potential_flag)
                potential_flag.clear()
            else:
                try:
                    next_flag = flags[f + 1]
                except IndexError:
                    # the last one
                    next_flag = None

                if next_flag == '>':
                    potential_flag.append(flag)
                    continue
                else:
                    potential_flag.append(flag)
                    flag = ''.join(potential_flag)
                    potential_flag.clear()

            if flag not in available_flags:
                raise InvalidFlag(flag)
            else:
                if hasattr(cls, available_flags[flag]):
                    flags_values.append(getattr(cls, available_flags[flag])[1])
        return flags_values
