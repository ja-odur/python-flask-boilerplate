"""Module for auditable base model"""

# System libraries
from datetime import datetime

# Models
from ..database import db
from .base_model import BaseModel


class AuditableBaseModel(BaseModel):
    """Auditable base model"""

    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)
    deleted_by = db.Column(db.String, nullable=True)
