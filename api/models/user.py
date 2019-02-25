"""Module for User model."""

# System imports
import enum

# Models
from .base.auditable_model import AuditableBaseModel

# Database
from .database import db

class Status(enum.Enum):
    disabled = 'disabled'
    enabled = 'enabled'


class User(AuditableBaseModel):
    """Class for user db table."""

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
