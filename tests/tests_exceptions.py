import unittest
from printy.exceptions import InvalidFlag


class TestExceptions(unittest.TestCase):
    """ Test Case for exceptions """

    def setUp(self):
        self.invalid_flag = "l"
        self.invalid_flag_error = "'%s' is not a valid flag" % self.invalid_flag

    def test_invalid_flag_str(self):
        """ test that the exception InvalidFlag returns the expected text """
        error = InvalidFlag(self.invalid_flag)

        self.assertEqual(str(error), self.invalid_flag_error)
