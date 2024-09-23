from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
import json

# Create your views here.


@csrf_exempt
def register_user(request):
    try:
        if request.method == "POST":
            req_body = json.loads(request.body)

            username = req_body.get('username', '')
            password = req_body.get('password', '')
            email = req_body.get('email', '')

            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return JsonResponse({"error": f"username or email already exists"}, status=400)

            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            user.save()

            user = serialize("json", [user])
            user = json.loads(user)[0]

            return JsonResponse(
                {
                    "status": "success",
                    "message": "User created successfully",
                    "user": user
                }, status=201
            )

        return JsonResponse({"error": f"Invalid request method {request.method}"}, status=405)

    except Exception as e:
        print(str(e))
        return JsonResponse(
            {
                "status": "failed",
                "message": "An error occured while registering. Please try again.",
            }, status=500,
        )


@csrf_exempt
def login_user(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body)

            username = req_body.get('username', '')
            password = req_body.get('password', '')

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Login successful",
                    },
                    status=200
                )

            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Invalid credentials",
                },
                status=401
            )

        return JsonResponse({"error": f"Invalid request method {request.method}"}, status=405)

    except Exception as e:
        print(str(e))
        return JsonResponse(
            {
                "status": "failed",
                "message": "An error occured while logging in. Please try again."
            },
            status=500
        )


@csrf_exempt
@login_required
def logout_user(request):
    try:
        if request.method == 'POST':
            logout(request)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Logout successful",
                },
                status=200
            )

        return JsonResponse({"error": f"Invalid request method {request.method}"}, status=405)

    except Exception as e:
        print(str(e))
        return JsonResponse(
            {
                "status": "failed",
                "message": 'An error occured while logging out. Please try again.',
            },
            status=500
        )


@csrf_exempt
@login_required
def update_user(request):
    try:
        if request.method == 'PUT' or request.method == 'PATCH':
            body = json.loads(request.body)
            user = request.user

            user.username = body.get('username', user.username)
            user.email = body.get('email', user.email)

            if 'password' in body:
                user.set_password(body['password'])
                # Keep the user authenticated/Logged in after password change
                update_session_auth_hash(request, user)

            user.save()

            user = serialize("json", [user])
            user = json.loads(user)[0]

            return JsonResponse(
                {
                    "status": "success",
                    "message": "User updated successfully",
                    "user": user
                },
                status=200
            )

        return JsonResponse({"error": f"Invalid request method {request.method}"}, status=405)

    except Exception as e:
        print(str(e))
        return JsonResponse(
            {
                "status": "failed",
                "message": 'An error occured while updating the user. Please try again.',
            },
            status=500
        )


@login_required
@csrf_exempt
def delete_user(request):
    try:
        if request.method == 'DELETE':
            user = request.user
            user.delete()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "User deleted successfully",
                },
                status=200
            )

        return JsonResponse({"error": f"Invalid request method {request.method}"}, status=405)

    except Exception as e:
        print(str(e))
        return JsonResponse(
            {
                "status": "failed",
                "message": 'An error occured while deleting the user. Please try again.',
            },
            status=500
        )
