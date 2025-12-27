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

__all__ = ["raw", "raw_format", "printy", "escape", "COLORS", "FORMATS"]

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

# Main function to extend print() functionality
printy = printy_instance.format

# Escaping function for untrusted sources
escape = printy_instance.escape

# shortcut to get a list of the available flags and formats
available_flags = Flags.get_flags().keys()
COLORS = list(filter(lambda c: c.islower(), available_flags))
FORMATS = list(filter(lambda f: f.isupper(), available_flags))
