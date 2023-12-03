"""Resolver util module."""
from ariadne import QueryType, MutationType, ScalarType, ObjectType
from ..resolvers.scalars.datetime import serialize_datetime
from ..resolvers.scalars.emailaddr import serialize_email

from ..resolvers.mutations import (
    create_comment,
    update_comment,
    create_community,
    update_community,
)
from ..resolvers.mutations import create_post, update_post, create_user, update_user


from ..resolvers.queries import (
    search_comments,
    search_communities,
    search_posts,
    search_users,
)
from ..resolvers.types import user as gql_user, post as gql_post
from ..resolvers.types import comment as gql_comment, community as gql_community


def make_resolver_list():
    """Make list of resolvers"""
    mutation = MutationType()
    query = QueryType()
    datetime_scalar = ScalarType("Datetime")
    email_scalar = ScalarType("EmailAddress")
    comment = ObjectType("Comment")
    user = ObjectType("User")
    post = ObjectType("Post")
    community = ObjectType("Community")

    datetime_scalar.serializer(serialize_datetime)
    email_scalar.serializer(serialize_email)

    mutation.set_field("create_comment", create_comment.create_comment)
    mutation.set_field("update_comment", update_comment.update_comment)

    mutation.set_field("create_post", create_post.create_post)
    mutation.set_field("update_post", update_post.update_post)

    mutation.set_field("create_community", create_community.create_community)
    mutation.set_field("update_community", update_community.update_community)

    mutation.set_field("create_user", create_user.create_user)
    mutation.set_field("update_user", update_user.update_user)

    query.set_field("search_users", search_users.search_users)
    query.set_field("search_posts", search_posts.search_posts)
    query.set_field("search_communities", search_communities.search_communities)
    query.set_field("search_comments", search_comments.search_comments)

    user.set_field("communities", gql_user.resolve_communities)
    user.set_field("posts", gql_user.resolve_posts)
    user.set_field("comments", gql_user.resolve_comments)

    post.set_field("community", gql_post.resolve_community)
    post.set_field("user", gql_post.resolve_user)
    post.set_field("comments", gql_post.resolve_comments)

    community.set_field("users", gql_community.resolve_users)
    community.set_field("posts", gql_community.resolve_posts)

    comment.set_field("post", gql_comment.resolve_post)
    comment.set_field("user", gql_comment.resolve_user)
    comment.set_field("comments", gql_comment.resolve_comments)
    comment.set_field("parent", gql_comment.resolve_comment)

    return [
        mutation,
        query,
        datetime_scalar,
        email_scalar,
        comment,
        user,
        post,
        community,
    ]
