from __future__ import annotations


class InvalidFlag(Exception):
    """Raised when an invalid flag is passed to the 'printy' object"""

    def __init__(self, flag: str) -> None:
        self.flag = flag

    def __str__(self) -> str:
        return "'%s' is not a valid flag" % self.flag
