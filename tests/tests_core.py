import unittest
from unittest import mock
from printy.exceptions import (
    InvalidFlag, InvalidInputType, BoolOptionsNotValid,
    IntOptionsNotValid, FloatOptionsNotValid
)
from printy.core import Printy, WINDOWS
from printy.flags import Flags


class TestGlobalFlagsPrinty(unittest.TestCase):
    """ Test case for formatting with a global set of flags specified """

    def setUp(self):
        self.sample_text = "Some Text To Print Out"
        self.printy = Printy()
        self.raw_text = self.printy.get_formatted_text

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


class TestInlineFlagsPrinty(unittest.TestCase):
    """ Test case for inline formatting """

    def setUp(self):
        self.printy = Printy()
        self.raw_text = self.printy.get_formatted_text

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


class TestInputy(unittest.TestCase):
    """
    Test case for inputy functionality

    Here, it is not necessary to test whether the prompted message has the
    correct format because it uses the methods already tested in the Printy
    test cases
    """

    def setUp(self):
        self.inputy = Printy()

    str_valid_test = "Valid String"
    int_valid_test = 23
    float_valid_test = 45.6
    bool_valid_test = False

    def test_get_bool_options_case_insensitive(self):
        """
        Tests returning True for the insensitive value if 'i' is passed as
        the first character of the 'options' parameter
        """
        options = 'i{y/n}'
        insensitive, true_option, false_option = self.inputy.get_bool_options(options)

        self.assertTrue(insensitive)
        self.assertEqual(true_option, 'y')
        self.assertEqual(false_option, 'n')

    def test_get_bool_options_case_sensitive(self):
        """
        Tests returning True for the insensitive value if no 'i' is passed as
        the first character of the 'options' parameter
        """
        options = 'y/n'
        insensitive, true_option, false_option = self.inputy.get_bool_options(options)

        self.assertFalse(insensitive)
        self.assertEqual(true_option, 'y')
        self.assertEqual(false_option, 'n')

    def test_default_value_options(self):
        """
        Tests return the default 'True' and 'False' and case insensitive if no
        options are passed
        """
        options = ''
        insensitive, true_option, false_option = self.inputy.get_bool_options(options)

        self.assertTrue(insensitive)
        self.assertTrue(true_option)
        self.assertFalse(false_option)

    def test_passing_wrong_flag_for_case_insensitive(self):
        """
        Tests that passing a value different than 'i' for the insensitive
        flag in in 'options' parameter when the type is bool, raises an exception
        """
        options = 'f{y/n}'
        with self.assertRaises(BoolOptionsNotValid) as e:
            self.inputy.get_bool_options(options)
        self.assertEqual(e.exception.options, options)

    def test_passing_invalid_options_to_bool_type(self):
        """
        Tests that passing an invalid option value to the parameter 'options'
        raises an BoolOptionsNotValid
        """
        invalid_options = "jgnlf"
        with self.assertRaises(BoolOptionsNotValid) as e:
            self.inputy.get_bool_options(invalid_options)
        self.assertEqual(e.exception.options, invalid_options)

    def test_get_int_options(self):
        """ Test returning valid options"""
        positive = '+'
        negative = '-'
        int_options_positive = self.inputy.get_int_options(positive)
        int_options_negative = self.inputy.get_int_options(negative)

        self.assertEqual(positive, int_options_positive)
        self.assertEqual(negative, int_options_negative)

    def test_passing_long_character_as_int_options(self):
        """
        Tests that passing more than one character (only + or - are allowed)
        raises an exception
        """
        long_int_options_one = '+-'
        long_int_options_two = 'plus'

        with self.assertRaises(IntOptionsNotValid) as e_one:
            self.inputy.get_int_options(long_int_options_one)
        with self.assertRaises(IntOptionsNotValid) as e_two:
            self.inputy.get_int_options(long_int_options_two)
        self.assertEqual(e_one.exception.options, long_int_options_one)
        self.assertEqual(e_two.exception.options, long_int_options_two)

    def test_check_boolean_case_sensitive_returns_value_converted(self):
        """
        tests that passing a value (according to the options) to a type='bool'
        returns a converted value (True or False)
        """
        options = 'y/n'
        value_true = 'y'
        value_false = 'n'
        returned_value_true, valid_value_true = self.inputy.check_boolean(value_true, options)
        returned_value_false, valid_value_false = self.inputy.check_boolean(value_false, options)

        self.assertEqual(returned_value_true, True)
        self.assertEqual(returned_value_false, False)
        self.assertTrue(valid_value_true)
        self.assertTrue(valid_value_false)

    def test_check_boolean_case_insensitive_returns_value_converted(self):
        """
        tests that passing a value with different case (according to the options
        as case insensitive) to a type='bool' returns a converted value (True or False)
        """
        options = 'i{y/n}'
        value_true = 'Y'
        value_false = 'N'
        returned_value_true, valid_value_true = self.inputy.check_boolean(value_true, options)
        returned_value_false, valid_value_false = self.inputy.check_boolean(value_false, options)

        self.assertEqual(returned_value_true, True)
        self.assertEqual(returned_value_false, False)
        self.assertTrue(valid_value_true)
        self.assertTrue(valid_value_false)

    def test_check_boolean_invalid_value(self):
        """
        tests passing an invalid value to check_bool returns False as the value
        and also False as 'valid_value'
        """
        options = 'i{y/n}'
        value_true = 'Yes'
        value_false = 'No'
        returned_value_true, valid_value_true = self.inputy.check_boolean(value_true, options)
        returned_value_false, valid_value_false = self.inputy.check_boolean(value_false, options)

        self.assertEqual(returned_value_true, False)
        self.assertEqual(returned_value_false, False)
        self.assertFalse(valid_value_true)
        self.assertFalse(valid_value_false)

    def test_check_integer_returns_converted_value(self):
        """ tests that check_integer returns the value converted as integer"""
        value = 34
        returned_value, valid_value = self.inputy.check_integer(value)

        self.assertTrue(isinstance(returned_value, int))
        self.assertEqual(returned_value, value)
        self.assertTrue(valid_value)

    def test_check_integer_with_positive_option(self):
        """
        Tests that passing '+' as options for type='int' returns the converted
        value and valid_value as False if it is not a positive number
        """
        opts_positive = '+'
        valid_int = 34
        invalid_int = -34
        return_valid_int, valid_value_valid_int = self.inputy.check_integer(valid_int, opts_positive)
        return_invalid_int, valid_value_invalid_int = self.inputy.check_integer(invalid_int, opts_positive)

        self.assertTrue(isinstance(return_valid_int, int))
        self.assertEqual(return_valid_int, valid_int)
        self.assertTrue(valid_value_valid_int)

        self.assertTrue(isinstance(return_invalid_int, int))
        self.assertEqual(return_invalid_int, invalid_int)
        self.assertFalse(valid_value_invalid_int)

    def test_check_integer_with_negative_option(self):
        """
        Tests that passing '-' as options for type='int' returns the converted
        value and valid_value as False if it is not a negative number
        """
        opts_positive = '-'
        valid_int = -34
        invalid_int = 34
        return_valid_int, valid_value_valid_int = self.inputy.check_integer(valid_int, opts_positive)
        return_invalid_int, valid_value_invalid_int = self.inputy.check_integer(invalid_int, opts_positive)

        self.assertTrue(isinstance(return_valid_int, int))
        self.assertEqual(return_valid_int, valid_int)
        self.assertTrue(valid_value_valid_int)

        self.assertTrue(isinstance(return_invalid_int, int))
        self.assertEqual(return_invalid_int, invalid_int)
        self.assertFalse(valid_value_invalid_int)

    def test_check_float_returns_converted_value(self):
        """ tests that check_float returns the value converted as float"""
        value = 34.5
        returned_value, valid_value = self.inputy.check_float(value)

        self.assertTrue(isinstance(returned_value, float))
        self.assertEqual(returned_value, value)
        self.assertTrue(valid_value)

    def test_check_float_with_positive_option(self):
        """
        Tests that passing '+' as options for type='float' returns the converted
        value and valid_value as False if it is not a positive number
        """
        opts_positive = '+'
        valid_int = 34.5
        invalid_int = -34.5
        return_valid_int, valid_value_valid_int = self.inputy.check_float(valid_int, opts_positive)
        return_invalid_int, valid_value_invalid_int = self.inputy.check_float(invalid_int, opts_positive)

        self.assertTrue(isinstance(return_valid_int, float))
        self.assertEqual(return_valid_int, valid_int)
        self.assertTrue(valid_value_valid_int)

        self.assertTrue(isinstance(return_invalid_int, float))
        self.assertEqual(return_invalid_int, invalid_int)
        self.assertFalse(valid_value_invalid_int)

    def test_check_float_with_negative_option(self):
        """
        Tests that passing '-' as options for type='float' returns the converted
        value and valid_value as False if it is not a negative number
        """
        opts_positive = '-'
        valid_int = -34.0
        invalid_int = 34.0
        return_valid_int, valid_value_valid_int = self.inputy.check_float(valid_int, opts_positive)
        return_invalid_int, valid_value_invalid_int = self.inputy.check_float(invalid_int, opts_positive)

        self.assertTrue(isinstance(return_valid_int, float))
        self.assertEqual(return_valid_int, valid_int)
        self.assertTrue(valid_value_valid_int)

        self.assertTrue(isinstance(return_invalid_int, float))
        self.assertEqual(return_invalid_int, invalid_int)
        self.assertFalse(valid_value_invalid_int)

    @mock.patch('builtins.input', return_value=str_valid_test)
    def test_passing_no_parameters_returns_a_value_str(self, mock_input):
        """ Testing 'inputy' as a normal 'input()' function """
        result_str = self.inputy.format_input()
        self.assertEqual(result_str, self.str_valid_test)

    @mock.patch('builtins.input', return_value=int_valid_test)
    def test_passing_no_parameters_returns_a_value_str_from_int(self,
                                                                mock_input):
        """ Testing 'inputy' as a normal 'input()' function """
        result_str_from_int = self.inputy.format_input()
        self.assertEqual(result_str_from_int, str(self.int_valid_test))

    @mock.patch('builtins.input', side_effect=[str_valid_test, bool_valid_test, float_valid_test, None, int_valid_test])
    def test_passed_invalid_when_requested_int(self, mock_input):
        """
        Test that, when specifying the users has to enter an integer,
        the message is prompted until a valid number is passed
        """
        result_valid_int = self.inputy.format_input(type='int')

        self.assertEqual(result_valid_int, self.int_valid_test)

    @mock.patch('builtins.input', side_effect=[None, str_valid_test, bool_valid_test, float_valid_test])
    def test_passed_invalid_when_requested_float(self, mock_input):
        """
        Test that, when specifying the users has to enter a number,
        the message is prompted until a valid number is passed
        """
        result_valid_int = self.inputy.format_input(type='float')

        self.assertEqual(result_valid_int, self.float_valid_test)

    @mock.patch('builtins.input', side_effect=[str_valid_test, None, int_valid_test, bool_valid_test])
    def test_passed_invalid_when_requested_boolean(self, mock_input):
        """
        Test that, when specifying the user has to enter a boolean
        the message is prompted until a boolean is passed
        """
        result_valid_boolean = self.inputy.format_input(type='bool')

        self.assertEqual(result_valid_boolean, self.bool_valid_test)

    @mock.patch('builtins.input', side_effect=[str_valid_test, None, int_valid_test, 'true'])
    def test_passed_invalid_when_requested_boolean_str(self, mock_input):
        """
        Test that, when specifying the user has to enter a boolean
        the message is prompted until a test case insensitive with the name of
        one of the boolean values is passed
        """
        result_valid_boolean = self.inputy.format_input(type='bool')

        self.assertEqual(result_valid_boolean, True)

    @mock.patch('builtins.input', return_value=str_valid_test)
    def test_passing_and_invalid_input_type(self, mock_input):
        """
        Tests that passing and invalid input type raises an InvalidInputType
        exception. We mock the input() just in case the tests reaches that section
        """
        invalid_input_type = 'not_int_nor_float'
        with self.assertRaises(InvalidInputType) as e:
            self.inputy.format_input(type=invalid_input_type)
        self.assertEqual(e.exception.input_type, invalid_input_type)
