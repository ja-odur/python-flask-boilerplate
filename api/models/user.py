"""Module for User model."""

# System imports
import enum

# Third party
from werkzeug.security import generate_password_hash

# Models
from .base.auditable_model import AuditableBaseModel

# Database
from .database import db

# Metas
from .base.base_meta import SqlAlchemyValidationMeta

# Validators
from api.utilities.validators import (email_validator, passwords_validator)


class Status(enum.Enum):
    disabled = 'disabled'
    enabled = 'enabled'


class ValidateUser:

    remove_keys = ('password', 'confirm_password')

    def validate_email(self, input_dict, email):
        return email_validator(email)

    def validate_password(self, input_dict, password):
        return passwords_validator(password, input_dict.get('confirm_password'))

    def generate_hash(self, input_dict):
        return generate_password_hash(input_dict.get('password'), salt_length=10)


class User(AuditableBaseModel, metaclass=SqlAlchemyValidationMeta):
    """Class for user db table."""

    class Meta:
        validate_fields = ('first_name', 'last_name', 'email', 'image_url', 'status')

        extra_validator_class = ValidateUser

    __tablename__ = 'users'

    unique_fields = ('email', )

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    image_url = db.Column(db.String)
    status = db.Column(db.Enum(Status), nullable=False, default='enabled')
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

