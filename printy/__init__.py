"""

Printy extends the capabilities of the builtin print(), allowing
us to add some colors and formats to the text, either globally or inline with
a friendly and intuitive syntax

"""

from __future__ import annotations

import warnings
from importlib.metadata import version
from typing import Any

from .core import Printy
from .flags import Flags

try:
    __version__ = version("printy")
except Exception:  # pragma: no cover
    __version__ = "unknown"  # Fallback for development

__all__ = ["raw", "raw_format", "printy", "inputy", "escape", "COLORS", "FORMATS"]

printy_instance = Printy()

# If user just want to get the formatted text with the ANSI escape sequences
raw = printy_instance.get_formatted_text


# Backward compatibility alias - will be deprecated in future versions
def _deprecated_raw_format(*args: Any, **kwargs: Any) -> str:
    """Deprecated alias for raw(). Use raw() instead."""
    warnings.warn(
        "raw_format() is deprecated and will be removed in version 4.0. "
        "Use raw() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return raw(*args, **kwargs)


raw_format = _deprecated_raw_format


# Backward compatibility wrapper for removed inputy() function
def _deprecated_inputy(*args: Any, **kwargs: Any) -> str:
    """
    Deprecated wrapper for inputy() which was removed in version 3.0.0.
    Use standard input() with printy formatting instead.
    """
    warnings.warn(
        "inputy() was removed in version 3.0.0 and this compatibility wrapper will be "
        "removed in version 4.0. Use the standard input() function with printy "
        "formatting instead. Example: input(raw('[y]Enter name: @'))",
        DeprecationWarning,
        stacklevel=2,
    )
    # Only pass the first positional argument (prompt text) to input()
    # All other parameters (type, options, render_options, default, condition,
    # max_digits, max_decimals) are ignored as they're not supported by built-in input()
    # Apply raw() formatting to maintain backward compatibility with formatted prompts
    prompt = args[0] if args else ""
    return input(raw(prompt))


inputy = _deprecated_inputy

# Main function to extend print() functionality
printy = printy_instance.format

# Escaping function for untrusted sources
escape = printy_instance.escape

# shortcut to get a list of the available flags and formats
available_flags = Flags.get_flags().keys()
COLORS = list(filter(lambda c: c.islower(), available_flags))
FORMATS = list(filter(lambda f: f.isupper(), available_flags))
