import unittest
from printy.exceptions import InvalidFlag, InvalidInputType


class TestExceptions(unittest.TestCase):
    """ Test Case for exceptions """

    def setUp(self):
        self.invalid_flag = "l"
        self.invalid_flag_error = "'%s' is not a valid flag" % self.invalid_flag

        self.invalid_input_type = 'path'
        self.invalid_input_type_error = "'%s' is not a valid type" % self.invalid_input_type

    def test_invalid_flag_str(self):
        """ test that the exception InvalidFlag returns the expected text """
        error = InvalidFlag(self.invalid_flag)

        self.assertEqual(str(error), self.invalid_flag_error)

    def test_invalid_input_type_str(self):
        """ test that the exception InvalidInputType returns the expected text """
        error = InvalidInputType(self.invalid_input_type)

        self.assertEqual(str(error), self.invalid_input_type_error)
