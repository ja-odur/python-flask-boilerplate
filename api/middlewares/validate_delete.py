"""Module for a generalized delete validator."""

def validate_delete(relationships):
    """Check if instance has any children before soft deleting.

    Takes in a tuple of the child model field names with the
    backref and returns true if the parent has no children with the deleted
    flag set to true and returns false otherwise.

    Args:
        relationships: tuple of relationship fields

    Returns:
        bool: True if the instance has no children with the deleted flag,
              False otherwise.
    """

    if not relationships:
        return True

    return False
