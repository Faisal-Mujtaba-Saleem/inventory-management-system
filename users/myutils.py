from .models import Token
from functools import wraps
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound
from django.http import JsonResponse


def api_login_required(view_fn):
    @wraps(view_fn)
    def modified_view(request, *args, **kwargs):
        try:
            if request.user.is_authenticated or not request.user.is_anonymous:
                return view_fn(request, *args, **kwargs)
            
            return JsonResponse({"status": "failed", "message": "Unauthorized"}, status=401)

        except Exception as e:
            print(str(e))
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Something went wrong"
                },
                status=500
            )

    return modified_view


def validateToken(view_fn):
    @wraps(view_fn)
    def modified_view(request, *args, **kwargs):
        try:
            authkey = request.headers.get('Authorization', None)

            if authkey is not None and authkey.startswith('Bearer '):
                authkey = authkey.split(' ')[1]
                token = get_object_or_404(Token, key=authkey)

                if isinstance(request.user, AnonymousUser):
                    # Unauthorized user because of AnonymousUser, not logged in
                    return HttpResponseForbidden('Unauthorized User')

                user = request.user

                if token.user.id == user.id and user.token.key == token.key:
                    response = view_fn(request, *args, **kwargs)
                    return response

                # Unauthorized user because of invalid token
                return HttpResponseForbidden('Unauthorized User')

            # Unauthorized authkey because of invalid authkey, its None or not start with Bearer
            return HttpResponseForbidden('Unauthorized AuthKey or AuthKey not provided')

        except Http404:
            # Unauthorized AuthKey because of invalid authkey, not found any token associated with authkey
            return HttpResponseNotFound('Unauthorized AuthKey')

        except Exception as e:
            print(str(e))
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Something went wrong"
                },
                status=500
            )

    return modified_view
