from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from inventory.models import Category
import json


# Category views

@csrf_exempt
def listCategories(request):
    """
    Retrieves a list of all categories in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of categories

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        categories_queryset = Category.objects.all()

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."},
                status=400
            )

        paginator = Paginator(categories_queryset, pagesize)
        page_object = paginator.get_page(page)

        categories_list = json.loads(
            serialize('json', page_object.object_list)
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all categories",
                "page": page,
                "pagesize": pagesize,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "categories": categories_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def retrieveCategory(request, category_slug):
    """
    Retrieves a category from the inventory by slug.

    Args:
        request (HttpRequest): The request object
        category_slug (str): The slug of the category to retrieve

    Returns:
        JsonResponse: The category with the matching slug

    Raises:
        Category.DoesNotExist: If category with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        category_retrieved = Category.objects.get(slug=category_slug)
        category_retrieved = json.loads(
            serialize('json', [category_retrieved])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the category with slug {category_slug}",
                "category": category_retrieved
            },
            status=200
        )

    except Category.DoesNotExist:
        return JsonResponse({"error": "Category Not Found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateCategory(request, category_slug):
    """
    Updates a category from the inventory by slug.

    Args:
        request (HttpRequest): The request object
        category_slug (str): The slug of the category to update

    Returns:
        JsonResponse: A JSON response containing the updated category

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        if not request.method in ['PUT', 'PATCH']:
            return JsonResponse(
                {
                    "error": f"Request method {request.method} not allowed, use PUT or PATCH"
                },
                status=405
            )

        category = Category.objects.get(slug=category_slug)

        data = json.loads(request.body)
        category_name = data.get('name', category.name)

        category.name = category_name
        category.save()

        category_updated = json.loads(
            serialize('json', [category])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully updated the category with slug {category_slug}",
                "Category": category_updated
            },
            status=200
        )

    except Category.DoesNotExist:
        return JsonResponse(
            {
                "error": "Category Not Found"
            },
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            }, status=500
        )


@csrf_exempt
def deleteCategory(request, category_slug):
    """
    Deletes a category by slug.

    Args:
        request (HttpRequest): The request object
        category_slug (str): The slug of the category to delete

    Returns:
        JsonResponse: A JSON response containing the deletion message

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        if not request.method == 'DELETE':
            return JsonResponse(
                {
                    "error": f"Request method {request.method} not allowed, use DELETE"
                },
                status=405
            )

        category = Category.objects.get(slug=category_slug)
        category.delete()

        return JsonResponse(
            {
                "message": f"The category with slug {category_slug} has been deleted successfully"
            },
            status=204
        )

    except Category.DoesNotExist:
        return JsonResponse(
            {
                "error": "Category Not Found"
            },
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )
