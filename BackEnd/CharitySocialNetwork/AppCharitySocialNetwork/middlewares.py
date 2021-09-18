from collections import OrderedDict

from django.http import QueryDict, Http404, HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from oauth2_provider.backends import OAuthLibCore
from django.contrib.auth import login
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.oauth2_backends import get_oauthlib_core
from oauth2_provider.models import Application


# class AuthorizationMiddleware(MiddlewareMixin):
class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        # if hasattr(self, 'process_request'):
        print(request.path_info, request.content_type, request.method)
        if request.path_info.__eq__("/api/graphql/") and request.method.__eq__("POST"):
            oauthlib_core = get_oauthlib_core()
            valid, r = oauthlib_core.verify_request(request, scopes=[])
            # print(r.user)
            if valid and r.user.is_active:
                request.user = r.user
        return self.get_response(request)


class LoginByClientIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
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
