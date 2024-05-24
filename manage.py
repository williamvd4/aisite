#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from typing import List, Tuple

def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        error_msg = (
            "Couldn't import Django. Make sure it's installed and available "
            "on your PYTHONPATH environment variable. If you're using a "
            "virtual environment, did you remember to activate it?"
        )
        raise ImportError(error_msg) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

