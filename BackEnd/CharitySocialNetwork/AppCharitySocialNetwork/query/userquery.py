import graphene
from django.db.models import QuerySet
from graphene import List
from graphql import GraphQLError

from ..graphene_types import *


class UserQuery:
    queryset = User.objects.filter(is_active=True)

    accounts = graphene.Field(AccountObjectType)
    notifications = List(NotificationObjectsType)

    def resolve_notifications(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user.notifications.filter(active=True)
        raise GraphQLError("You do not have permission to perform this query")

    def resolve_accounts(self, info, **kwargs):
        """
            self không có tác dụng gọi hàm hoặc các biến trong class
        """
        if info.context.user.is_authenticated:
            return User.objects.get(pk=info.context.user.id)
        raise GraphQLError("You do not have permission to perform this query")
