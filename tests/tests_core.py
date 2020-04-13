import unittest
from unittest import mock
from printy.exceptions import InvalidFlag, InvalidInputType
from printy.core import (Printy, LINUX, OSX, WINDOWS)

# If you find yourself struggling with import errors like
# 'ImportError: attempted relative import with no known parent package'
# while running tests with 'unittest', just install 'nose2'
# >>> pip install nose2


class TestGlobalFlagsPrinty(unittest.TestCase):
    """ Test case for formatting with a global set of flags specified """

    def setUp(self):
        self.sample_text = "Some Text To Print Out"
        self.printy_instance = Printy()
        self.printy = self.printy_instance.format
        self.raw_text = self.printy_instance.get_formatted_text

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
        i_printy = self.printy_instance
        text = ''
        flags = 'rBH'
        result = self.raw_text(text, flags)
        expected_result = "%s%s" % (
                i_printy._join_flags(i_printy.get_flag_values(flags)),
                i_printy._get_end_of_line()
        )

        self.assertEqual(result, expected_result)

    def test_single_invalid_flag(self):
        """
        Tests that passing an invalid flag (only one)
        raises and exception
        """
        invalid_flag = 'P'
        with self.assertRaises(InvalidFlag):
            self.printy(self.sample_text, invalid_flag)

    def test_multiple_invalid_flag(self):
        """
        Tests that passing multiple invalid flags raises an
        exception with the first invalid flag found
        """
        # P and G are invalid, should raise InvalidFlag
        # with 'P' as invalid flag
        flags = 'yBPGr'
        with self.assertRaises(InvalidFlag) as e:
            self.printy(self.sample_text, flags)
        self.assertEqual(e.exception.flag, 'P')

    def tests_always_closing_format(self):
        """
        Tests that the returned text is always ended with the closing tag
        """
        result = self.raw_text(self.sample_text, 'r')
        closing_tag = result[-4:]
        self.assertEqual(len(closing_tag), 4)
        self.assertEqual(closing_tag, Printy._get_end_of_line())

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

    def test_no_linux_platform_return_cleaned_value(self):
        """
        Tests that if printy is used on platforms other than Linux it still
        returns the cleaned value
        """
        flags = 'rBH'
        # Changes platform to Windows
        self.printy_instance.platform = WINDOWS
        result_one = self.raw_text(self.sample_text, flags)
        # Changes platform to Darwin
        self.printy_instance.platform = OSX
        result_two = self.raw_text(self.sample_text, flags)

        self.assertTrue(result_one == result_two == self.sample_text)


class TestInlineFlagsPrinty(unittest.TestCase):
    """ Test case for inline formatting """

    def setUp(self):
        self.printy_instance = Printy()
        self.printy = self.printy_instance.format
        self.raw_text = self.printy_instance.get_formatted_text

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

    def test_no_linux_platform_return_cleaned_value(self):
        """
        Tests that if printy is used on platforms other than Linux it still
        returns the cleaned value
        """
        sample_text = "[rBH]Sample@ [y]Text@"
        sample_text_expected = "Sample Text"
        # Changes platform to Windows
        self.printy_instance.platform = WINDOWS
        result_one = self.raw_text(sample_text)
        # Changes platform to Darwin
        self.printy_instance.platform = OSX
        result_two = self.raw_text(sample_text)

        self.assertTrue(result_one == result_two == sample_text_expected)


class TestInputy(unittest.TestCase):
    """
    Test case for inputy functionality

    Here, it is not necessary to test whether the prompted message has the
    correct format because it uses the methods already tested in the Printy
    test cases
    """

    def setUp(self):
        self.inputy = Printy().format_input

    str_valid_test = "Valid String"
    int_valid_test = 23
    float_valid_test = 45.6
    bool_valid_test = False

    @mock.patch('builtins.input', return_value=str_valid_test)
    def test_passing_no_parameters_returns_a_value_str(self, mock_input):
        """ Testing 'inputy' as a normal 'input()' function """
        result_str = self.inputy()
        self.assertEqual(result_str, self.str_valid_test)

    @mock.patch('builtins.input', return_value=int_valid_test)
    def test_passing_no_parameters_returns_a_value_str_from_int(self, mock_input):
        """ Testing 'inputy' as a normal 'input()' function """
        result_str_from_int = self.inputy()
        self.assertEqual(result_str_from_int, str(self.int_valid_test))

    @mock.patch('builtins.input', side_effect=[str_valid_test, bool_valid_test, float_valid_test, None, int_valid_test])
    def test_passed_invalid_when_requested_int(self, mock_input):
        """
        Test that, when specifying the users has to enter an integer,
        the message is prompted until a valid number is passed
        """
        result_valid_int = self.inputy(type='int')

        self.assertEqual(result_valid_int, self.int_valid_test)

    @mock.patch('builtins.input', side_effect=[None, str_valid_test, bool_valid_test, float_valid_test])
    def test_passed_invalid_when_requested_float(self, mock_input):
        """
        Test that, when specifying the users has to enter a number,
        the message is prompted until a valid number is passed
        """
        result_valid_int = self.inputy(type='float')

        self.assertEqual(result_valid_int, self.float_valid_test)

    @mock.patch('builtins.input', side_effect=[str_valid_test, None, int_valid_test, bool_valid_test])
    def test_passed_invalid_when_requested_boolean(self, mock_input):
        """
        Test that, when specifying the user has to enter a boolean
        the message is prompted until a boolean is passed
        """
        result_valid_boolean = self.inputy(type='bool')

        self.assertEqual(result_valid_boolean, self.bool_valid_test)

    @mock.patch('builtins.input', side_effect=[str_valid_test, None, int_valid_test, 'true'])
    def test_passed_invalid_when_requested_boolean_str(self, mock_input):
        """
        Test that, when specifying the user has to enter a boolean
        the message is prompted until a test case insensitive with the name of
        one of the boolean values is passed
        """
        result_valid_boolean = self.inputy(type='bool')

        self.assertEqual(result_valid_boolean, True)

    @mock.patch('builtins.input', return_value=str_valid_test)
    def test_passing_and_invalid_input_type(self, mock_input):
        """
        Tests that passing and invalid input type raises an InvalidInputType
        exception. We mock the input() just in case the tests reaches that section
        """
        invalid_input_type = 'not_int_nor_float'
        with self.assertRaises(InvalidInputType) as e:
            self.inputy(type=invalid_input_type)
        self.assertEqual(e.exception.input_type, invalid_input_type)
