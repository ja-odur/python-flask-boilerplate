

class UniqueFields(type):

    def __call__(cls, *args, **kwargs):

        if not hasattr(cls, 'unique_fields'):
            raise AttributeError(f'{cls} has no attribute unique_fields')

        return super().__call__(*args, **kwargs)
