"""Module for generic model operations mixin."""

# System libraries
import re

# Third-Party libraries
from flask import request
from sqlalchemy.exc import IntegrityError

# models
from ..database import db
from .base_model_exception import BaseModelException

# middlewares
from api.middlewares.base_validator import ValidationError

# Validators
from api.middlewares.validate_delete import validate_delete

# Utililties
from api.utilities.sql_queries import EXISTS

# messages
from api.utilities.messages.error_messages import database_errors

# Abstract_model
from .abstract_model import UniqueFields


class ModelOperations(metaclass=UniqueFields):

    def save(self):
        """Save a model instance"""

        try:
            db.session.add(self)
            db.session.commit()

        except IntegrityError as error:

            db.session.rollback()
            unique_field = self.__class__.unique_fields[0]
            raise BaseModelException(
                'Integrity error',
                dict(
                    message=f"{self.__class__.__name__} with {unique_field} "
                            f"'{self.__dict__[unique_field]}' already exists"
                )
            ) from error

        return self

    def update_(self, **kwargs):
        """update entries"""

        for field, value in kwargs.items():
            setattr(self, field, value)
        if request and request.decoded_token:
            self.updated_by = request.decoded_token['UserInfo']['name']
        db.session.commit()

    @classmethod
    def get(cls, id):
        """return entries by id"""

        return cls.query.filter_by(id=id, deleted=False).first()

    @classmethod
    def get_or_404(cls, id):
        """return entries by id"""

        record = cls.get(id)

        if not record or record.deleted:
            raise ValidationError(
                {
                    'message':
                        f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'

                },
                404)

        return record

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has.
        This is used to ascertain if a model has relationship(s) or
        not when validating delete operation.
        It must be overridden in subclasses and takes no argument.
        :return None if there are no child relationships.
        A tuple of all child relationships eg (self.relationship_field1,
        self.relationship_field2)
        """

        raise NotImplementedError(
            "The get_relationships method must be overridden in all child model classes"
        )  # noqa

    def set_deleted_by(self, decoded_token):
        """Sets deleted_by property.

        If the request object has a decoded token, set the deleted_by
        property to the name of the user in the decoded token

        Args:
            decoded_token (dict): The decoded token

        """
        if decoded_token:
            self.deleted_by = request.decoded_token['UserInfo']['name']

    def delete(self):
        """
        Soft delete a model instance.
        """
        relationships = self.get_child_relationships()
        if validate_delete(relationships):
            self.deleted = True
            self.set_deleted_by(request.decoded_token)
            db.session.add(self)
            db.session.commit()
        else:
            relationship_names = []
            for relationship in relationships:
                relationship_names.append(
                    f'{relationship.first().__class__.__name__}(s)')
            raise ValidationError(
                dict(message=database_errors['model_delete_children'].format(
                    self.__class__.__name__, ', '.join(relationship_names))),
                status_code=403)


    @classmethod
    def query_(cls, filter_condition=None):
        """
        Returns filtered database entries. It takes model class and
        filter_condition and returns database entries based on the filter
        condition, eg, User.query_('name,like,john'). Apart from 'like', other
        comparators are eq(equal to), ne(not equal to), lt(less than),
        le(less than or equal to) gt(greater than), ge(greater than or equal to)
        :param filter_condition:
        :return: an array of filtered records
        """

        # if filter_condition:
        #     sort = cls.sorting_helper(filter_condition)
        #     dynamic_filter = DynamicFilter(cls)
        #     return dynamic_filter.filter_query(filter_condition).order_by(sort)

        # sort = cls.sorting_helper()
        return cls.query.filter_by(deleted=False)

    @classmethod
    def count(cls):
        """Returns total entries in the database"""

        return cls.query.count()

    @classmethod
    def find_or_create(cls, data, **kwargs):
        """Finds a model instance or creates it"""
        instance = cls.query.filter_by(**kwargs, deleted=False).first()
        if not instance:
            instance = cls(**data).save()
        return instance

    @classmethod
    def bulk_create(cls, raw_list):
        """
        Save raw list of records to database

        Parameters:
            raw_list(list): List of records to be saved to database
        """
        resource_list = [cls(**item) for item in raw_list]
        db.session.add_all(resource_list)
        db.session.commit()

        return resource_list

    @classmethod
    def exists(cls, value, column='id'):
        """Verifies whether the specified id exists in the database

        This method uses an SQL statement which returns no row data to check
        whether a record exists. It is therefore more efficient than the
        `Model.get` method when verifying existence is all that is required.

        Examples:
            Asset.exists(asset_id)
            User.exists(token_id, 'token_id')

        Args:
            column (str): The column to check. Defaults to 'id'
            value (str): The value to verify

        Returns:
            bool: True if the value exists, False otherwise
        """
        query = EXISTS.format(
            table=cls.__table__.name, column=column, value=value)
        result = db.engine.execute(query).scalar()
        if result:
            return True
        return False
