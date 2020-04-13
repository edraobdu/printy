from .core import Printy

__version__ = "1.0.1"

printy_instance = Printy()

# Main function to extend print() functionality
printy = printy_instance.format

# If user just want to get the formatted text with the ANSII escape code
raw_format = printy_instance.get_formatted_text

# Main function to extend input() functionality
inputy = printy_instance.format_input

