from django.http import JsonResponse

def loginRequiredView(request):
    print("login required view")
    return JsonResponse({"status": "failed", "message": "Unauthorized access"}, status=401)