from .models import Token
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, Http404
from django.http import JsonResponse


def validateToken(view_fn):
    @wraps(view_fn)
    def modified_view(request, *args, **kwargs):
        try:
            authkey = request.headers.get('Authorization', None)

            if authkey is not None and authkey.startswith('Bearer '):
                authkey = authkey.split(' ')[1]
                token = get_object_or_404(Token, key=authkey)
                user = getattr(request, 'user', None)

                if user and token.user.id == user.id and user.token.key == token.key:
                    response = view_fn(request, *args, **kwargs)
                    return response

                return HttpResponseForbidden('Unauthorized User')

            return HttpResponseForbidden('Unauthorized AuthKey')

        except Http404:
            return HttpResponseForbidden('Unauthorized AuthKey')

        except Exception as e:
            print(
                str(e)
            )
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Something went wrong"
                },
                status=500
            )

    return modified_view
