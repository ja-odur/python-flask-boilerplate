"""Module for marshmallow User schema"""

#Third-party imports
from marshmallow import ValidationError, fields, post_load, validates_schema
from werkzeug.security import generate_password_hash

# model serializers
from .base_schema import AuditableBaseSchema

# Validators
from ..validators import (name_validator, string_length_validator,
                          email_validator, url_validator, status_validator,
                          passwords_validator)

# Error Messages
from ..messages.error_messages import validation_errors


class UserSchema(AuditableBaseSchema):
    """User model schema"""

    first_name = fields.String(
        required=True,
        error_messages={'required': validation_errors['field_required']},
        validate=(string_length_validator(60), name_validator),
        load_from='firstName',
        dump_to='firstName'
    )

    last_name = fields.String(
        required=True,
        error_messages={'required': validation_errors['field_required']},
        validate=(string_length_validator(60), name_validator),
        load_from='lastName',
        dump_to='lastName'
    )
    email = fields.String(
        required=True,
        error_messages={'required': validation_errors['field_required']},
        validate=(email_validator, )
    )

    image_url = fields.String(
        validate=(url_validator, ),
        load_from='imageUrl',
        dump_to='imageUrl'
    )

    status = fields.String(
        load_only=True,
        validate=(status_validator, )
    )

    password = fields.String(
        required=True,
        load_only=True,
        error_messages={'required': validation_errors['field_required']},
    )

    password_confirm = fields.String(
        required=True,
        load_only=True,
        error_messages={'required': validation_errors['field_required']},
        load_from='passwordConfirm',
    )

    @validates_schema
    def validate_match(self, data):

        if data['password'] != data['password_confirm']:
            raise ValidationError(
                validation_errors['password_match'].format(
                    data['password'],
                    data['password_confirm']
                ),
                field_names=['password_confirm']
            )

    @staticmethod
    def generate_password_hash(password):
        """Method for generating password hash"""

        return generate_password_hash(password, salt_length=10)

    @post_load
    def add_extras(self, data):

        password_hash = UserSchema.generate_password_hash(data['password'])

        data.pop('password'), data.pop('password_confirm')
        data.__setitem__('password_hash', password_hash)



