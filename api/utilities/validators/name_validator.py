""" Module with string generic validator. """

# System imports
import re

# Third-party imports
from marshmallow import ValidationError

# Error messages
from ..messages.error_messages import validation_errors

string_regex = re.compile(r"^[a-zA-Z]+(([' .-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$")


def name_validator(name):
    """Validates name

    Args:
        name (str): the name to be validated

    Raises:
        ValidationError if name contains consecutive fullstops, hyphens,
         spaces and apostrophes.
    """

    if not re.match(string_regex, name):
        raise ValidationError(validation_errors['string_characters'])
