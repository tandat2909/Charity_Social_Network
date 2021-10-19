from graphene import *
from ..graphene_types import *

class PostQuery:
    posts = List(PostObjectType)
    post = Field(PostObjectType, post_id=ID(required=True))
    auction_item = Field(AuctionItemObjectType, post_id=ID(required=True))

    def resolve_posts(self, info, **kwargs):
        queryset = NewsPost.objects.filter(active=True, is_show=True).order_by("-created_date")
        return queryset

    def resolve_auction_item(self, info, post_id):
        # print(self)
        # print(info)
        # print(post_id)
        return AuctionItem.objects.get(post_id=post_id)

    def resolve_post(self, info, post_id, **kwargs):
        return NewsPost.objects.get(active=True, is_show=True, pk=post_id)
