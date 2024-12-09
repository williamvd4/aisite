#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from typing import List, Tuple, Optional
from django.core.management import execute_from_command_line
from django.core.exceptions import ImproperlyConfigured

def main(argv: Tuple[str]) -> None:
    """Run administrative tasks."""
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        import django  # noqa: F401
    except ImproperlyConfigured as e:
        error_msg = (
            "Django settings module not found. Make sure it's installed and "
            "configured correctly. Error: {}"
        ).format(e)
        raise ImproperlyConfigured(error_msg)
    except ImportError as e:
        error_msg = (
            "Couldn't import Django. Make sure it's installed and available "
            "on your PYTHONPATH environment variable. If you're using a "
            "virtual environment, did you remember to activate it?"
        )
        raise ImportError(error_msg) from e

    try:
        execute_from_command_line(argv)
    except Exception as e:  # pylint: disable=broad-except
        error_msg = (
            "An error occurred while executing the command. Error: {}"
        ).format(e)
        raise Exception(error_msg) from e
