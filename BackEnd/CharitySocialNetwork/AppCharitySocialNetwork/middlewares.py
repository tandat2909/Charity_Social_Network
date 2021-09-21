from collections import OrderedDict

from django.contrib.auth.middleware import AuthenticationMiddleware
from django.http import QueryDict, Http404, HttpResponse, JsonResponse
from django.middleware.security import SecurityMiddleware
from django.utils.deprecation import MiddlewareMixin
from oauth2_provider.backends import OAuthLibCore
from django.contrib.auth import login
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.middleware import OAuth2TokenMiddleware
from oauth2_provider.oauth2_backends import get_oauthlib_core
from oauth2_provider.models import Application
from django.conf import settings


class GraphQLOAuth2TokenMiddleware(MiddlewareMixin):
    """
        Middleware chứng thực người dùng cho url graphql sử dụng oauth2
    """
    def __init__(self, get_response):
        super().__init__(get_response)
        try:
            self.url = settings.GRAPHENE_URL
        except AttributeError as ex:
            raise Exception("GraphQL OAuth2Token Middleware require param 'GRAPHENE_URL' in settings file\n"
                            "GRAPHENE_URL is url your call api Graphql")

    def process_request(self, request):
        # if hasattr(self, 'process_request'):
        print("debug:GraphQLOAuth2TokenMiddleware: ", request.path_info, "-", request.content_type, "-", request.method)
        # kiểm tra link request có phải là /api/graphql/ và method POST không
        if request.path_info.__eq__(self.url) and request.method.__eq__("POST"):
            # kiểm tra request có gửi thông tin chứng thực lên hay không
            if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer") \
                    and not hasattr(request, "user") or request.user.is_anonymous:
                valid, r = get_oauthlib_core().verify_request(request, scopes=[])
                # print(r.user)
                if valid and r.user.is_active:
                    request.user = r.user
        return self.get_response(request)


class LoginByClientIdMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print(request.path_info, request.content_type, request.method)
        # print(request.method.__eq__("POST"),request.content_type.__eq__("application/x-www-form-urlencoded"),request.path_info.__eq__("/o/token/"))
        if request.method.__eq__("POST") and request.content_type.__eq__("application/x-www-form-urlencoded") \
                and request.path_info.__eq__("/o/token/"):
            # print(request.path_info, request.content_type, request.method)
            request_post = request.POST.copy()
            grant_type = request_post.get("grant_type", "password")
            # client_secret = request_post.get("client_secret", None)
            client_id = request_post.get("client_id", None)
            if client_id is not None:
                client_secret = request_post.get("client_secret",
                                                 Application.objects.filter(client_id=client_id).first().client_secret)
                request_post.__setitem__("grant_type", grant_type)
                request_post.__setitem__("client_secret", client_secret)
                request.POST = request_post
        # print(request.POST)
        return self.get_response(request)
