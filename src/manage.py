"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    from djangobower.management.base import BaseBowerCommand
    BaseBowerCommand.requires_system_checks = []

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
