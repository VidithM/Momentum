"""Resolver for EmailAddress scalar."""
from ariadne import ScalarType

datetime_scalar = ScalarType("EmailAddress")

@datetime_scalar.serializer
def serialize_datetime(value):
    """Resolver for EmailAddress scalar."""
    return value
