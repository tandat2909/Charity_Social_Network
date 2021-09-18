import graphene
import rest_framework.exceptions
from django.db.models import QuerySet
from graphene_django.debug import DjangoDebug
from graphql import ResolveInfo

from .query import *


class Query(graphene.ObjectType, UserQuery, PostQuery):
    hi = graphene.String()
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_hi(self, info, **kwargs):
        return "Hello, Welcome to the project Charity Social Network"


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
