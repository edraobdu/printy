import unittest
from unittest import mock
from printy.exceptions import InvalidFlag
from printy.core import Printy, WINDOWS
from printy.flags import Flags


class TestGlobalFlagsPrinty(unittest.TestCase):
    """ Test case for formatting with a global set of flags specified """

    def setUp(self):
        self.sample_text = "Some Text To Print Out"
        self.printy = Printy()
        self.raw_text = self.printy.get_formatted_text
        self.esc = self.printy.escape

    def test_empty_value(self):
        """ Tests passing an empty value print's nothing"""
        text = ''
        result = self.raw_text(text)

        self.assertEqual(result, text)

    def test_empty_value_with_flags(self):
        """
        Tests that passing and empty value with some flags returns the
        escape ansi characters
        """
        text = ''
        flags = 'rBH'
        result = self.raw_text(text, flags)
        expected_result = "%s%s" % (
                Flags.join_flags(Flags.get_flag_values(flags)),
                Flags.get_end_of_line()
        )

        self.assertEqual(result, expected_result)

    def test_single_invalid_flag(self):
        """
        Tests that passing an invalid flag (only one)
        raises and exception
        """
        invalid_flag = 'P'
        with self.assertRaises(InvalidFlag):
            self.printy.format(self.sample_text, invalid_flag)

    def test_multiple_invalid_flag(self):
        """
        Tests that passing multiple invalid flags raises an
        exception with the first invalid flag found
        """
        # P and G are invalid, should raise InvalidFlag
        # with 'P' as invalid flag
        flags = 'yBPGr'
        with self.assertRaises(InvalidFlag) as e:
            self.printy.format(self.sample_text, flags)
        self.assertEqual(e.exception.flag, 'P')

    def test_high_intensity_flag_color(self):
        """
        Checks the correct format is returned for a high
        intensity (>) flag color
        """
        flag = 'p>'
        text = 'Hello'
        expected_text = '\x1b[38;5;98mHello\x1b[0m'

        self.assertEqual(self.raw_text(text, flag), expected_text)

    def test_low_intensity_flag_color(self):
        """
        Checks the correct format is returned for a low
        intensity (<) flag color
        """
        flag = '<p'
        text = 'Hello'
        expected_text = '\x1b[38;5;54mHello\x1b[0m'

        self.assertEqual(self.raw_text(text, flag), expected_text)

    def tests_always_closing_format(self):
        """
        Tests that the returned text is always ended with the closing tag
        """
        result = self.raw_text(self.sample_text, 'r')
        closing_tag = result[-4:]
        self.assertEqual(len(closing_tag), 4)
        self.assertEqual(closing_tag, Flags.get_end_of_line())

    def test_no_flag_parameter_passed(self):
        """
        Tests that passing no flag parameter will return a default value
        """
        result = self.raw_text(self.sample_text)
        self.assertEqual(result, self.sample_text)

    def test_empty_flag(self):
        """
        Test that passing and empty string as a flag still returns the
        default value
        """
        result = self.raw_text(self.sample_text, '')
        self.assertEqual(result, self.sample_text)

    def test_flags_with_spaces_in_between(self):
        """
        Tests that passing a set of flags with some spaces in between
        (like 'yB H U') still applies the desired formats
        """
        desired_flags = 'yBH'
        flags_with_one_space = 'yB H'
        flags_with_multiple_spaces = 'y B H'
        result_one = self.raw_text(self.sample_text, desired_flags)
        result_two = self.raw_text(self.sample_text, flags_with_one_space)
        result_three = self.raw_text(self.sample_text, flags_with_multiple_spaces)

        self.assertTrue(result_one == result_two == result_three)

    def test_escape_with_global_flags(self):
        """
        Test escaping values with global flags
        """
        text = '[n]escaped@'
        expected_text = '\x1b[38;5;196m[n]escaped@\x1b[0m'
        result = self.raw_text(self.esc(text), 'r')

        self.assertEqual(result, expected_text)


    @mock.patch('printy.core.Printy.set_windows_console_mode', return_value=True)
    def test_virtual_terminal_processing_on_windows(self, mock_console_mode):
        """
        Tests that if platform is windows, then then returns True
        """
        self.printy.platform = WINDOWS
        virtual_terminal_processing = mock_console_mode()

        self.assertTrue(virtual_terminal_processing)

    def test_return_cleaned_value_if_windows_is_not_properly_configured(self):
        """
        Tests that if printy virtual_console_mode is false, then it returns the
        cleaned_text
        """
        flags = 'rBH'
        # Changes platform to Windows
        self.printy.platform = WINDOWS
        self.printy.virtual_terminal_processing = False

        result_one = self.raw_text(self.sample_text, flags)

        self.assertEqual(result_one, self.sample_text)

    def test_background_color_with_global_flags(self):
        """
        Test backgroun color with global flags
        """
        flags = 'yB{o}'
        text = 'Hello'
        expected_text = '\x1b[48;5;208;38;5;11;1mHello\x1b[0m'

        self.assertEqual(self.raw_text(text, flags), expected_text)

    def test_background_color_no_flag_with_global_flags(self):
        """
        Test backgroun color with no flag for it, with global flags
        """
        flags = 'yB{}'
        text = 'Hello'
        expected_text = '\x1b[38;5;11;1mHello\x1b[0m'

        self.assertEqual(self.raw_text(text, flags), expected_text)


class TestInlineFlagsPrinty(unittest.TestCase):
    """ Test case for inline formatting """

    def setUp(self):
        self.printy = Printy()
        self.raw_text = self.printy.get_formatted_text
        self.esc = self.printy.escape

    def test_inline_format_with_global_flags(self):
        """
        Tests that passing a text with inline formatting and also a global
        set of flags takes this last one as the format to be applied
        """
        inline_formatted = "[y]Hey you@"
        no_format = 'Hey you'
        global_flags = 'rB'
        result_one = self.raw_text(inline_formatted, global_flags)
        result_two = self.raw_text(no_format, global_flags)

        self.assertEqual(result_one, result_two)

    def test_inline_format_without_ending_format_character(self):
        """
        Tests that passing an inline formatted text without the ending
        formatting character still returns the formatted text
        """
        result_one = self.raw_text('[y]Hey you')
        result_two = self.raw_text('[y]Hey you@')

        self.assertEqual(result_one, result_two)

    def test_escape_special_characters(self):
        """ Tests that escaping special characters prints them out """
        inline_text_one = '[y]myemail\@mydomain.com@'
        global_text_one = 'myemail@mydomain.com', 'y'

        inline_text_two = '[bH]Some text \@@'
        global_text_two = 'Some text @', 'bH'

        inline_result_one = self.raw_text(inline_text_one)
        global_result_one = self.raw_text(global_text_one[0], global_text_one[1])

        inline_result_two = self.raw_text(inline_text_two)
        global_result_two = self.raw_text(global_text_two[0], global_text_two[1])

        self.assertEqual(inline_result_one, global_result_one)
        self.assertEqual(inline_result_two, global_result_two)

    def test_multiple_sections(self):
        """ Test that formats are applied correctly to each section """

        section_one = "Some"
        section_two = ' '
        section_three = 'text'
        global_format_one = self.raw_text(section_one, 'rB')
        global_format_two = self.raw_text(section_two)
        global_format_three = self.raw_text(section_three, 'y')
        joined_global_format = global_format_one + global_format_two + global_format_three

        inline_text = '[rB]Some@ [y]text@'
        inline_format = self.raw_text(inline_text)

        self.assertEqual(inline_format, joined_global_format)

    def test_read_file(self):
        """ Test retrieving the text from a file """
        text_in_file = 'printy'
        file_name = 'printy_file'
        with mock.patch('builtins.open', mock.mock_open(read_data=text_in_file)) as m:
            result = self.printy.read_file(file_name)

        m.assert_called_once_with(file_name)
        self.assertEqual(result, text_in_file)

    def test_escape_special_chars_method(self):
        """
        Test escaping especial characters correctly, this method is used when
        an object other than a string is passed
        """
        text_to_escape = '[some text @ ]'
        expected_value = '\[some text \@ \]'
        escaped_text = Printy._escape_special_chars(text_to_escape)

        self.assertEqual(expected_value, escaped_text)

    def test_pretty_print_dicts(self):
        """ Test pretty printing dictionaries """
        dict_to_print = {'name': 'John Doe', 'age': 34}
        expected_result = '{\n    [n>]\'name\'@: [c>]\'John Doe\'@[<oB],@\n    [n>]\'age\'@: [c]34@[<oB],@\n}'
        pretty_dict = Printy._repr_value(dict_to_print)

        self.assertEqual(expected_result, pretty_dict)

    def test_pretty_print_lists(self):
        """ Test pretty printing lists """
        list_to_print = [1, 2, 'hello']
        expected_result = '\[\n    [c]1@[<oB],@ [c]2@[<oB],@ [c>]\'hello\'@\n\]'
        pretty_list = Printy._repr_value(list_to_print)

        self.assertEqual(expected_result, pretty_list)

    def test_pretty_printy_tuples(self):
        """ Test pretty printing tuples """
        tuple_to_print = (1, 2, 'hello')
        expected_result = '(\n    [c]1@[<oB],@ [c]2@[<oB],@ [c>]\'hello\'@\n)'
        pretty_tuple = Printy._repr_value(tuple_to_print)

        self.assertEqual(expected_result, pretty_tuple)

    def test_pretty_printy_sets(self):
        """ Test pretty printing sets """
        set_to_print = {1, 2, 'hello'}
        expected_result = '{\n    [c]1@[<oB],@ [c]2@[<oB],@ [c>]\'hello\'@\n}'
        pretty_set = Printy._repr_value(set_to_print)

        self.assertEqual(expected_result, pretty_set)

    def test_pretty_printy_dict_pretty_false(self):
        """ Tests pretty printing a dict when 'pretty' parameter is set to False """
        dict_to_print = {'name': 'John Doe', 'age': 34}
        expected_result = '{\'name\': \'John Doe\', \'age\': 34}'
        not_pretty_dict = Printy._repr_value(dict_to_print, pretty=False)

        self.assertEqual(expected_result, not_pretty_dict)

    def test_pretty_printy_list_pretty_false(self):
        """ Tests pretty printing a list when 'pretty' parameter is set to False """
        list_to_print = [1, 2, 'hello']
        expected_result = '\[1, 2, \'hello\'\]'
        not_pretty_list = Printy._repr_value(list_to_print, pretty=False)

        self.assertEqual(expected_result, not_pretty_list)

    def test_pretty_printy_tuple_pretty_false(self):
        """ Tests pretty printing a tuple when 'pretty' parameter is set to False """
        tuple_to_print = (1, 2, 'hello')
        expected_result = '(1, 2, \'hello\')'
        not_pretty_tuple = Printy._repr_value(tuple_to_print, pretty=False)

        self.assertEqual(expected_result, not_pretty_tuple)

    def test_pretty_printy_set_pretty_false(self):
        """ Tests pretty printing a set when 'pretty' parameter is set to False """
        set_to_print = {1, 2, 'hello'}
        expected_result = '{1, 2, \'hello\'}'
        not_pretty_set = Printy._repr_value(set_to_print, pretty=False)

        self.assertEqual(expected_result, not_pretty_set)

    def test_pretty_print_str_method_of_objects(self):
        """ Test printing the str method of an object, both not defined and defined """
        builtin_obj = int
        expected_builtin_result = '<class \'int\'>'
        pretty_builtin = Printy._repr_value(builtin_obj)

        class Person:
            def __str__(self):
                return '[c]I am a person@'
        custom_str = Person()
        # Notice how it should not return the escaped character
        expected_custom_result = '[c]I am a person@'
        pretty_custom = Printy._repr_value(custom_str)

        self.assertEqual(expected_builtin_result, pretty_builtin)
        self.assertEqual(expected_custom_result, pretty_custom)

    def test_pretty_object_in_dictionary(self):
        """
        Test pretty printing an str method of an object inside a dictionary
        or any iterable, it should give it a light magenta color
        """
        dict_to_print = {'class': int}
        expected_result = '{\n    [n>]\'class\'@: <class \'int\'>[<oB],@\n}'
        pretty_dict = Printy._repr_value(dict_to_print)

        self.assertEqual(expected_result, pretty_dict)

    def test_pretty_custom_str_method_in_dictionary(self):
        class CustomStrMethod:
            def __str__(self):
                return '[rBU]Red Bold Underlined@ and [y]Yellow@'

        dict_to_print = {'str': CustomStrMethod()}
        expected_result = '{\n    [n>]\'str\'@: [rBU]Red Bold Underlined@ and [y]Yellow@[<oB],@\n}'
        pretty_dict = Printy._repr_value(dict_to_print)

        self.assertEqual(expected_result, pretty_dict)

    def test_print_number(self):
        integer_to_print = 123
        float_to_print = 123.45
        expected_result_integer = '[c]123@'
        expected_result_float = '[c]123.45@'

        result_integer = Printy._repr_value(integer_to_print)
        result_float = Printy._repr_value(float_to_print)

        self.assertEqual(expected_result_integer, result_integer)
        self.assertEqual(expected_result_float, result_float)

    def test_print_boolean(self):
        expected_false = '[<o]False@'
        expected_true = '[<o]True@'

        result_false = Printy._repr_value(False)
        result_true = Printy._repr_value(True)

        self.assertEqual(expected_false, result_false)
        self.assertEqual(expected_true, result_true)

    def test_print_none(self):
        expected_none = '[<o]None@'
        result_none = Printy._repr_value(None)

        self.assertEqual(expected_none, result_none)

    def test_escape_with_inline_flags(self):
        """
        Test escaping values on inline formats
        """
        email = 'escaped@gmail.com'        
        expected_text = '\x1b[38;5;28mescaped@gmail.com\x1b[0m'
        result = self.raw_text(f'[n]{self.esc(email)}@')

        self.assertEqual(result, expected_text)

    def test_background_color_with_inline_flags(self):
        """
        Test backgroun color with inline flags
        """        
        text = '[yB{o}]Hello@'
        expected_text = '\x1b[48;5;208;38;5;11;1mHello\x1b[0m'

        self.assertEqual(self.raw_text(text), expected_text)

    def test_background_color_no_flag_with_global_flags(self):
        """
        Test backgroun color with no flag for it, with global flags
        """
        text = '[yB{}]Hello@'
        expected_text = '\x1b[38;5;11;1mHello\x1b[0m'
        self.assertEqual(self.raw_text(text), expected_text)