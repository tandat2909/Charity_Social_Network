from graphene import *
from ..graphene_types import *


# class HashtagQuery:
#     hashtags = List(HashtagObjectType)
#
#     def resolve_hashtags(self, info, **kwargs):
#         return Hashtag.objects.filter(active=True)


class PostQuery:
    posts = List(PostObjectType)
    # auction_item = Field(AuctionItemObjectType)
    # history_auction = List(HistoryAuction)

    def resolve_posts(self, info, **kwargs):
        queryset = NewsPost.objects.filter(active=True, is_show=True).order_by("-created_date")
        return queryset
