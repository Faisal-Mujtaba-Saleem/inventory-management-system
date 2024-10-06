from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Token
from .myutils import validateToken, api_login_required


# Views for users


# Register a new user

@csrf_exempt
def registerUser(request):
    try:
        if request.method == "POST":
            req_body = json.loads(request.body)

            # Extract user details
            firstname = req_body['firstname']
            lastname = req_body['lastname']
            username = req_body['username']
            password = req_body['password']
            email = req_body['email']

            # Create user
            user, is_created = User.objects.get_or_create(
                username=username, email=email)

            # Check if the user is created or already exists
            if not is_created:
                return JsonResponse({"status": "failed", "message": "User already exists"}, status=400)

            # Set user details, first name and last name
            user.first_name = firstname
            user.last_name = lastname

            # Set password
            user.set_password(password)
            user.save()

            # Create token on behalf of user created
            token = Token(user=user)
            token.save()

            login(request, user)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "User created successfully",
                    "auth_key": token.key,
                    "user": json.loads(
                        serialize("json", [user])
                    )[0]
                }, status=201
            )

        return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print(str(e))  # Log the exception
        return JsonResponse({"status": "failed", "message": "An error occurred while registering. Please try again."}, status=500)


# List Users

@api_login_required
@validateToken
@csrf_exempt
def listUsers(request):
    try:
        if request.user.is_superuser:
            users = json.loads(
                serialize(
                    'json', User.objects.all()
                )
            )

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Users retrieved successfully",
                    "users": users
                }
            )
        
        return JsonResponse(
            {"status": "failed", "message": "Unauthorized Access."}, status=401
        )

    except Exception as e:
        raise e


# Retrieve user information

@api_login_required
@validateToken
@csrf_exempt
def retrieveUser(request):
    try:
        user = json.loads(
            serialize('json', [request.user])
        )[0]
        return JsonResponse(
            {
                "status": "success",
                "message": "User retrieved successfully",
                "user": user
            }
        )

    except Exception as e:
        print(str(e))  # Log the exception
        return JsonResponse({"status": "failed", "message": "An error occurred while retrieving user. Please try again."}, status=500)


# Login user

@csrf_exempt
def loginUser(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body)

            username = req_body.get('username', '')
            password = req_body.get('password', '')

            user = authenticate(username=username, password=password)
            if user is not None:
                token, is_created = Token.objects.get_or_create(user=user)

                if is_created:
                    login(request, user)
                    token.save()

                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Login successful",
                            "auth_key": token.key
                        },
                        status=200
                    )

                # User already logged in
                return JsonResponse({"status": "failed", "message": "User already logged in"}, status=400)

            # Invalid credentials
            return JsonResponse({"status": "failed", "message": "Invalid credentials"}, status=401)

        # Invalid request method
        return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print(str(e))  # Log the exception
        return JsonResponse({"status": "failed", "message": "An error occurred while logging in. Please try again."}, status=500)


# Logout user

@api_login_required
@validateToken
@csrf_exempt
def logoutUser(request):
    try:
        if request.method == 'POST':
            request.user.token.delete()
            logout(request)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Logout successful"
                },
                status=200
            )

        return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print(str(e))  # Log the exception
        return JsonResponse(
            {
                "status": "failed",
                "message": 'An error occurred while logging out. Please try again.'
            },
            status=500
        )


# Update user details

@api_login_required
@validateToken
@csrf_exempt
def updateUser(request):
    try:
        if request.method in ['PUT', 'PATCH']:
            body = json.loads(request.body)
            user = request.user

            # Update user attributes
            user.username = body.get('username', user.username)
            user.email = body.get('email', user.email)
            user.first_name = body.get('firstname', user.first_name)
            user.last_name = body.get('lastname', user.last_name)

            # Update password if provided
            if 'password' in body:
                user.set_password(body['password'])
                # Keep user logged in after password change
                update_session_auth_hash(request, user)

            user.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "User updated successfully",
                    "user": json.loads(serialize("json", [user]))[0]
                },
                status=200
            )

        return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print(str(e))  # Log the exception
        return JsonResponse(
            {
                "status": "failed",
                "message": 'An error occurred while updating the user. Please try again.'
            },
            status=500
        )


# Delete user account

@api_login_required
@validateToken
@csrf_exempt
def deleteUser(request):
    try:
        if request.method == 'DELETE':
            user = request.user
            user.delete()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "User deleted successfully"
                },
                status=200
            )

        return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print('Exception')  # Log the exception
        return JsonResponse(
            {
                "status": "failed",
                "message": 'An error occurred while deleting the user. Please try again.'
            },
            status=500
        )


# Refresh authentication key

@api_login_required
@validateToken
@csrf_exempt
def refreshAuthKey(request):
    try:
        if request.method == 'POST':
            request.user.token.delete()

            new_token = Token(user=request.user)
            new_token.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Token refreshed successfully",
                    "auth_key": new_token.key
                },
                status=200
            )

        return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print(str(e))  # Log the exception
        return JsonResponse({"status": "failed", "message": 'An error occurred while refreshing token. Please try again.'}, status=500)