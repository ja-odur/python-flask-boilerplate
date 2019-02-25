"""Model for Base Model"""

# Third-party imports
from flask_sqlalchemy.model import DefaultMeta

# Models
from ..database import db
from .model_operations import ModelOperations

from .abstract_model import UniqueFields


class CombinedMeta(DefaultMeta, UniqueFields):
    pass


class BaseModel(db.Model, ModelOperations, metaclass=CombinedMeta):
    """base model for all database models"""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
