import re

from .exceptions import InvalidFlag


class Flags:

    escape_ansi_code = '\x1b['
    escape_ansi_end = 'm'

    start_foreground = '38;5;'
    start_background = '48;5;'

    #### COLORS

    # Gray Scale
    COLOR_BLACK = 'k', '16'
    COLOR_GRAY = 'g', '243'
    COLOR_WHITE = 'w', '15'

    # Red Scale
    COLOR_DARKRED = '<r', '88'
    COLOR_RED = 'r', '196'
    COLOR_LIGHTRED = 'r>', '9'

    # Green Scale
    COLOR_DARKGREEN = '<n', '22'
    COLOR_GREEN = 'n', '28'
    COLOR_LIGHTGREEN = 'n>', '65'

    # Yellow Scale
    COLOR_DARKYELLOW = '<y', '58'
    COLOR_YELLOW = 'y', '11'
    COLOR_LIGHTYELLOW = 'y>', '3'

    # Blue Scale
    COLOR_DARKBLUE = '<b', '17'
    COLOR_BLUE = 'b', '20'
    COLOR_LIGHTBLUE = 'b>', '4'

    # Magenta Scale
    COLOR_DARKMAGENTA = '<m', '125'
    COLOR_MAGENTA = 'm', '198'
    COLOR_LIGHTMAGENTA = 'm>', '13'

    # Cyan Scale
    COLOR_DARKCYAN = '<c', '30'
    COLOR_CYAN = 'c', '39'
    COLOR_LIGHTCYAN = 'c>', '51'

    # Orange Scale
    COLOR_DARKORANGE = '<o', '130'
    COLOR_ORANGE = 'o', '208'
    COLOR_LIGHTORANGE = 'o>', '214'

    # Purple Scale
    COLOR_DARKPURPLE = '<p', '54'
    COLOR_PURPLE = 'p', '91'
    COLOR_LIGHTPURPLE = 'p>', '98'

    #### FORMATS
    FORMAT_BOLD = 'B', '1'
    FORMAT_DIM = 'D', '2'
    FORMAT_ITALIC = 'I', '3'
    FORMAT_UNDERLINE = 'U', '4'
    FORMAT_HIGHLIGHT = 'H', '7'
    FORMAT_STRIKE = 'S', '9'

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
    def get_fg_value(cls, flags, flag):
        """
        Return the flag as fg ansi code
        """
        # The name of the attribute in the class
        flag_name = flags[flag]
        if flag_name.startswith('FORMAT_'):
            return getattr(cls, flag_name)[1]
        return cls.start_foreground + getattr(cls, flag_name)[1]

    @classmethod
    def get_bg_value(cls, flags, flag):
        """
        Truns a flag ansi code from doreground to background code
        """
        # The name of the attribute in the class
        flag_name = flags[flag]
        if flag_name.startswith('FORMAT_'):
            return getattr(cls, flag_name)[1]
        return cls.start_background + getattr(cls, flag_name)[1]

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

        # New in 2.2
        # Extract the background, teh chars on brackets {}        
        bg_regex = '[a-zA-Z<>]{0,}(?P<background>{[a-zA-Z<>]{0,}})[a-zA-Z<>]{0,}'
        matched_bg = re.match(bg_regex, flags)
        
        if matched_bg is not None:
            bg = matched_bg.groupdict().get('background')            
            if bg:
                # Remove the background from the flags, so we end up 
                # with the foreground flasg only
                flags = flags.replace(bg, '')
                # remove brackets from background
                bg = bg[1:-1]
                # bg now can be an empty string if there's nothing between the brackets {}
                if bg:
                    if bg not in available_flags:
                        raise InvalidFlag(bg)
                    if hasattr(cls, available_flags[bg]):
                        flags_values.append(cls.get_bg_value(available_flags, bg))

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
                    flags_values.append(cls.get_fg_value(available_flags, flag))

        return flags_values
