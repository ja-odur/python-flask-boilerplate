

class UniqueFields(type):
    pass

    # def __init__(cls, name, bases, namespace):
    #     print('namespace', namespace)
    #     # import pdb; pdb.set_trace()
    #
    #     if not hasattr(cls, 'unique_fields'):
    #         raise AttributeError(f'{cls} has no attribute unique_fields')
    #
    #     super().__init__(cls, name, bases, namespace)

    def __call__(cls, *args, **kwargs):

        if not hasattr(cls, 'unique_fields'):
            raise AttributeError(f'{cls} has no attribute unique_fields')

        return super().__call__(*args, **kwargs)
