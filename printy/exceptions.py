class InvalidFlag(Exception):
    """Raised when an invalid flag is passed to the 'printy' object"""

    def __init__(self, flag):
        self.flag = flag

    def __str__(self):
        return "'%s' is not a valid flag" % self.flag
