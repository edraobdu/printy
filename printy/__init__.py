"""

Printy extends the capabilities of the builtin print(), allowing
us to add some colors and formats to the text, either globally or inline with
a friendly and intuitive syntax

"""

from .core import Printy
from .flags import Flags

__version__ = "3.0.0"

__all__ = ['raw_format', 'printy', 'escape', 'COLORS', 'FORMATS']

printy_instance = Printy()

# If user just want to get the formatted text with the ANSI escape sequences
raw_format = printy_instance.get_formatted_text

# Main function to extend print() functionality
printy = printy_instance.format

# Escaping function for untrusted sources
escape = printy_instance.escape

# shortcut to get a list of the available flags and formats
available_flags = Flags.get_flags().keys()
COLORS = list(filter(lambda c: c.islower(), available_flags))
FORMATS = list(filter(lambda f: f.isupper(), available_flags))
