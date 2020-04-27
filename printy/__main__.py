"""
renders the helper text that shows some of the available functions
by running python -m printy
"""

from . import printy

if __name__ == '__main__':
    from .helpme import helpme
    printy(helpme)
