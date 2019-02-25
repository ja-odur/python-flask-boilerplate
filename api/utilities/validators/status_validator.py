""" Module for validating the status field of a user"""

# Third-Party imports
from marshmallow import ValidationError

# Error messages
from ..messages.error_messages import validation_errors


def status_validator(status):
    """
    Used to validate status field in user schema to be either
    'enabled' or 'disabled'

    Arguments:
        status (string): field to be validated

    Raises:
        ValidationError: Used to raise exception if status field is
        neither 'enabled' nor 'disabled'
    """

    if status.lower() not in ['enabled', 'disabled']:
        raise ValidationError(validation_errors['invalid_status'])
