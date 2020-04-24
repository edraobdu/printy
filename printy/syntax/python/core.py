from .patterns import get_syntax_as_tuples
from ...flags import Flags


def return_formatted_syntax(text):
    final_text = ''
    tuple_text = get_syntax_as_tuples(text)
    for value, flags in tuple_text:
        final_text += Flags.get_formatted_text(value, flags)
    return final_text


def test_syntax_highlight():

    with open(
            '/home/edgar/Documents/PythonProjects/printy/test_syntax.py') as f:
        file = f.read()

    print(return_formatted_syntax(file))
