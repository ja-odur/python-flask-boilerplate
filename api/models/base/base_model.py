"""Model for Base Model"""

# Models
from ..database import db
from .model_operations import ModelOperations


class BaseModel(db.Model, ModelOperations):
    """base model for all database models"""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    deleted = db.Column(db.Boolean, default=False)

    # @classmethod
    # def get_fields(cls, keys=None):
    #     fields = {}
    #     if not keys:
    #         for column in cls.__table__.columns:
    #             fields.__setitem__(column.name, column)
    #         return fields
    #
    #     for column in cls.__table__.columns:
    #         fields.__setitem__(column.name, column) if column.name in keys else None
    #
    #     return fields
