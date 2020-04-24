import datetime
from unittest import mock


# This is an line comment
# This is an line comment too
@mock.patch('builtins.open', return_value='hey')
def my_function(str_parameter: str, int_parameter: int) -> tuple:
    """
    This is a docstring, a long docstring, probably longer
    than it should be
    """

    # Another line comment
    variable = 'Sample String' + str_parameter
    plus = int_parameter + 5
    date = datetime.date.today()

    try:
        str(plus)
    except (ValueError, TypeError):
        raise

    if isinstance(date, datetime.date) and len(variable) < 4:
        print('It\'s working')

    return variable, date, plus


class GreetingClass:

    def __init__(self):
        self.greeting = "Hello"
