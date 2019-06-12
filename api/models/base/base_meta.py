from itertools import chain
# Metas
from flask_sqlalchemy.model import DefaultMeta
from .abstract_model import UniqueFields

# Types
from sqlalchemy.sql import sqltypes

# Validators
from api.middlewares.base_validator import ValidationError


class FieldValidationError(Exception):
    pass


class ValidationMeta(type):

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        meta = namespace.get('Meta')

        if not meta:
            raise AttributeError(f"{cls} has no attribute 'Meta'")

        validate_fields = getattr(meta, 'validate_fields')

        if not validate_fields:
            raise AttributeError(f"{meta} has no attribute 'validate_fields'")

        extra_validator_class = getattr(meta, 'extra_validator_class', False)

        cls.__validatekeys__ = validate_fields
        cls.__extravalidations__ = extra_validator_class

        return cls

    def model_schema(cls, model_input_values, partial=False):
        errors = {}

        keys = set(list(cls.__validatekeys__) + list(model_input_values.keys()))

        if partial:
            keys = [key for key in model_input_values if key in keys]

        model_column = cls._get_fields(keys)

        errors = cls._validate_model_fields(keys, model_input_values, partial=partial, errors=errors)

        errors = cls._extra_validations(keys, model_input_values, errors=errors)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400
            )

        cls._generate_values(model_input_values)

        for key in model_input_values.copy().keys():
            if key not in model_column:
                del model_input_values[key]




    def _validate_model_fields(cls, keys, values, errors=None, model_columns=None, partial=False):

        errors = errors if errors else {}

        model_columns = model_columns if model_columns else cls._get_fields(keys)

        for key, value in model_columns.items():

            key_value = values.get(key)

            if not key_value:
                msg = [f'This field is required']
                errors.__setitem__(key, msg)

            elif issubclass(type(value.type), sqltypes.Enum):
                if key_value not in value.type.enums:
                    msg = [f'key {key_value} not in enum values {value.type.enums}']
                    errors.__setitem__(key, msg)

            elif issubclass(type(value.type), sqltypes.Integer):
                try:
                    int(key_value)
                except FieldValidationError:
                    msg = [f'{key_value} is not a valid integer']
                    errors.__setitem__(key, msg)

            elif issubclass(type(value.type), sqltypes.String):
                if len(key_value) > value.type.length:
                    msg = [f'{key_value} exceeds the max character length of {value.type.length}']
                    errors.__setitem__(key, msg)

            else:
                raise FieldValidationError(
                    f'The SQLAlchemy field type {type(value.type)} is not handled'
                )

        print('first errors', errors)
        return errors

    def _extra_validations(cls, fields, values, errors=None):

        errors = errors if errors else {}

        for field in fields:
            validate_method = getattr(cls.__extravalidations__, 'validate_' + field, None)

            error_msg = validate_method(cls.__extravalidations__(), values, values.get(field)) if validate_method else None

            if error_msg:
                errors.__setitem__(field, error_msg)

        print('errors before returning', errors)
        return errors

    def _generate_values(cls, values):

        validation_klass = cls.__extravalidations__.__dict__

        for key in validation_klass.keys():

            if key.startswith('generate_'):
                _, field_name = key.split('_')
                generate_method = getattr(cls.__extravalidations__, key)
                values.__setitem__(field_name, generate_method(cls.__extravalidations__(), values))






    def __call__(cls, *args, **kwargs):

        cls.model_schema(kwargs)
        # cls._validate_model_fields(kwargs)
        # cls._extra_validations(kwargs)

        return super().__call__(*args, **kwargs)





class SqlAlchemyValidationMeta(DefaultMeta, ValidationMeta, UniqueFields):
    pass
