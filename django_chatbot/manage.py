#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chatbot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__': # "manage.py" will only run if the script is ran directly and not when it's imported as a module
    # __name__ is a special python variable that holds the name of the current module
    # The purpose of this block is to encapsulate the actual execution of your script's main logic within the main() function, 
    # and then only execute that logic when the script is run directly as the main program. This allows you to reuse the same 
    # script as a module in other programs without the unintended side effects of running the main logic from the imported module. 
    # This separation ensures that the main logic is only executed when you intend to run the script as the main program.
    main()
