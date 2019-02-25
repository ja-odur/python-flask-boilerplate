""" Module for base marshmallow schema. """

# Third-Party imports
from marshmallow import Schema, fields

# Middlewares
from ...middlewares.base_validator import ValidationError

class BaseSchema(Schema):
    """Base schema to handle common attributes"""

    id = fields.String(dump_only=True)
    deleted = fields.Boolean(dump_only=True)

    def load_json_into_schema(self, data):
        """Helper function to load raw json into schema

            Args:
                data (json): json object to be loaded into schema

            Raises:
                ValidationError when a serialization error occurs
        """

        data, errors = self.loads(data)

        if errors:
            self.raise_validation_error(
                errors=errors, message='An error occurred'
            )

        return data

    def load_object_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema

        Args:
            data (Object): Python object)
            partial (Boolean): Indicator of whether to load partial data or not

        Raises:
            ValidationError when a serialization error occurs
        """

        data, errors = self.load(data, partial=partial)

        if errors:
            # self.raise_validation_error(
            #     errors=errors, message='An error occurred'
            # )
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400
            )

        return data

    def raise_validation_error(self, errors, message, status_code=400):
        """Helper function to raise validation error

        Args:
            errors: serialization errors
            message (string): error message
            status_code (int): the error status code

        Raises:
            ValidationError when a serialization error occurs
        """

        raise ValidationError(
            dict(errors=errors, message=message), status_code
        )


class AuditableBaseSchema(BaseSchema):
    """ Base marshmallow schema for auditable models"""

    created_at = fields.DateTime(dump_only=True, dump_to='createdAt')
    updated_at = fields.DateTime(dump_only=True, dump_to='updatedAt')
    deleted_at = fields.DateTime(dump_only=True, dump_to='deletedAt')
    created_by = fields.String(dump_only=True, dump_to='createdBy')
    updated_by = fields.String(dump_only=True, dump_to='updatedBy')
    deleted_by = fields.String(dump_only=True, dump_to='deletedBy')


