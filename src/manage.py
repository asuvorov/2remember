"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except IndexError:
        command = "help"

    if command == "test":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    from djangobower.management.base import BaseBowerCommand
    BaseBowerCommand.requires_system_checks = []

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
