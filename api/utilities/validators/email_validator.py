""" Module with email validator. """

# System Imports
import re

# Third-party imports
from marshmallow import ValidationError

# Error messages
from ..messages.error_messages import validation_errors

EMAIL_REGEX = re.compile(
    r"^[\-a-zA-Z0-9_]+(\.[\-a-zA-Z0-9_]+)*@[a-z]+\.com\Z", re.I | re.UNICODE)


def email_validator(data):
    """
    Checks if given string is at least 1 character and only contains characters
    that make a valid andela email.
    """

    data = data.lower()

    # Check if email pattern is matched
    if not EMAIL_REGEX.match(data):
        return validation_errors['email_syntax']
