#### Printy


class InvalidFlag(Exception):
    """ raised when an invalid flag is passed to the 'printy' object"""

    def __init__(self, flag):
        self.flag = flag

    def __str__(self):
        return "'%s' is not a valid flag" % self.flag


#### Inputy


class InvalidInputType(Exception):
    """ raised when an invalid 'type' is passed to the 'inputy' function"""

    def __init__(self, input_type):
        self.input_type = input_type

    def __str__(self):
        return "'%s' is not a valid type" % self.input_type
