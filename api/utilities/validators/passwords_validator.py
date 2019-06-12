""" Module for validating the password fields of a user"""

# Third-Party imports
from marshmallow import ValidationError

# Error messages
from ..messages.error_messages import validation_errors


def passwords_validator(password, confirm_password):
    """Used to validate password fields

    Args:
        password (string): field to be validated
        confirm_password (string): field to be validated

    Raises:
        ValidationError: Used to raise exception if passwords dont match
    """

    if password != confirm_password:
        return validation_errors['password_match'].format(
            password,
            confirm_password
        )

