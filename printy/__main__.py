"""
renders the helper text that shows some of the available functions
by running python -m printy
"""

from printy import printy

if __name__ == '__main__':
    from printy.helpme import helpme
    printy(helpme)
