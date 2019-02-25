""" Module with url validator. """

# System Imports
import re

# Third-Party imports
from marshmallow import ValidationError

# Error messages
from ..messages.error_messages import validation_errors

URL_REGEX = re.compile(r"^(http(s)?:\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]"
                       r"{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$")

def url_validator(data):
    """
    Checks if given string is at least 1 character and only contains characters
    that make a valid url.
    Raises validation error otherwise.
    """

    if not re.match(URL_REGEX, data):
        raise ValidationError(validation_errors['url_syntax'].format(data))
