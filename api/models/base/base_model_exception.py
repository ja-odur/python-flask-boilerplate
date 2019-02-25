"""Base model exception that is handled by flask restplus"""


class BaseModelException(Exception):

    def __init__(self, message, errors, status_code=400):
        super().__init__(message)
        self.__errors = errors
        self.__status_code = status_code

    @property
    def errors(self):
        return {'status': 'error', 'errors': self.__errors,}

    @property
    def status_code(self):
        return self.__status_code


