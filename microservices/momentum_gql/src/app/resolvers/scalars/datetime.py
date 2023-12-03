"""Resolver for datetime scalar."""
from ariadne import ScalarType

datetime_scalar = ScalarType("Datetime")

@datetime_scalar.serializer
def serialize_datetime(value):
    """Resolver for datetime scalar."""
    return value.isoformat()
