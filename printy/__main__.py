"""
renders the helper text that shows some of the available functions
by running python -m printy
"""

from __future__ import annotations

from . import printy

if __name__ == "__main__":
    from .helpme import helpme

    printy(helpme)
