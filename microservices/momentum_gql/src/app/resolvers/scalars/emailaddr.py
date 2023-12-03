"""Resolver for EmailAddress scalar."""
from ariadne import ScalarType

email_scalar = ScalarType("EmailAddress")

@email_scalar.serializer
def serialize_email(value):
    """Resolver for EmailAddress scalar."""
    return value
