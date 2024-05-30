#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from typing import List, Tuple
from django.core.management import execute_from_command_line

def main(argv: Tuple[str]) -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        execute_from_command_line(argv)
    except ImportError as exc:
        error_msg = (
            "Couldn't import Django. Make sure it's installed and available "
            "on your PYTHONPATH environment variable. If you're using a "
            "virtual environment, did you remember to activate it?"
        )
        raise ImportError(error_msg) from exc

