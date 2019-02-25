# Third Party Libraries
from sqlalchemy import event

# Models
from .user import User

# Model helpers
from .helpers import PushID


def model_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    target.id = push_id.next_id()


tables = (User,)

for table in tables:
    event.listen(table, 'before_insert', model_id_generator)

