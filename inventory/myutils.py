from django.http import JsonResponse
from django.http import HttpResponseForbidden, Http404
from functools import wraps


def restrict_cors(view_fn):  # cors => cross origin resource sharing
    ALLOWED_ORIGINS = set(
        ['http://127.0.0.1:8000', 'http://localhost:8000']
    )

    @wraps(view_fn)
    def modified_view(request, *args, **kwargs):
        req_origin = request.headers.get('Origin')

        if req_origin is not None and req_origin in list(ALLOWED_ORIGINS):
            if isinstance(response, JsonResponse):
                response = view_fn()
                return response

        else:
            return HttpResponseForbidden('Cross-origin request forbidden')

    return modified_view
