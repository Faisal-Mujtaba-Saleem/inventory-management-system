from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from users.myutils import validateToken, api_login_required
from inventory.models import Category, SubCategory
from inventory.myutils import populateRelationalFields
import json


# Sub-Category Views

@api_login_required
@validateToken
def listSubCategories(request):
    """
    Retrieves a list of all sub-categories in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of sub-categories

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        sub_categories_queryset = SubCategory.objects.all().order_by('pk')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(sub_categories_queryset, pagesize)
        page_object = paginator.get_page(page)

        sub_categories_list = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(
            sub_categories_list, ['category'], [Category])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all sub-categories",
                "page": page,
                "pagesize": pagesize,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "sub-categories": sub_categories_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def retrieveSubCategory(request, sub_category_slug):
    """
    Retrieves a specific sub-category by its slug.

    Args:
        request (django.http.request.HttpRequest): The request object
        sub_category_slug (str): The slug of the sub-category to retrieve

    Returns:
        JsonResponse: A JSON response containing the retrieved sub-category

    Raises:
        SubCategory.DoesNotExist: If the sub-category does not exist
        Exception: If there is an error with the database query
    """
    try:
        sub_category_retrieved = SubCategory.objects.get(
            slug=sub_category_slug
        )
        sub_category_retrieved = json.loads(
            serialize('json', [sub_category_retrieved])
        )[0]

        populateRelationalFields(
            sub_category_retrieved, ['category'], [Category]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved the sub_category with slug {sub_category_slug}",
                "sub_category": sub_category_retrieved
            },
            status=200
        )

    except SubCategory.DoesNotExist:
        return JsonResponse({"error": "SubCategory Not Found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




@api_login_required
@validateToken
def updateSubCategory(request, sub_category_slug):
    """
    Updates a sub-category with given slug.

    Args:
        request: The request object
        sub_category_slug: The slug of the sub-category to update

    Returns:
        JsonResponse: The updated sub-category

    Raises:
        SubCategory.DoesNotExist: If sub-category with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        if not request.method in ['PUT', 'PATCH']:
            return JsonResponse(
                {
                    "error": f"Request method {request.method} not allowed, use PUT or PATCH"
                },
                status=405
            )

        sub_category = SubCategory.objects.get(slug=sub_category_slug)

        data = json.loads(request.body)
        category_name = data.get('name', sub_category.name)

        sub_category.name = category_name
        sub_category.save()

        sub_category_updated = json.loads(
            serialize('json', [sub_category])
        )[0]

        populateRelationalFields(
            sub_category_updated, ['category'], [Category]
        )

        return JsonResponse(
            {
                "message": f"Successfully updated the sub_category with slug {sub_category_slug}",
                "sub_category": sub_category_updated
            },
            status=200
        )

    except SubCategory.DoesNotExist:
        return JsonResponse(
            {
                "error": "SubCategory Not Found"
            },
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            }, status=500
        )




@api_login_required
@validateToken
def deleteSubCategory(request, sub_category_slug):
    """
    Deletes a sub_category by slug.

    Args:
        request (HttpRequest): The request object
        sub_category_slug (str): The slug of the sub_category to delete

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

        SubCategory.objects.get(slug=sub_category_slug).delete()

        return JsonResponse(
            {
                "message": f"The sub_category with slug {sub_category_slug} has been deleted successfully"
            },
            status=204
        )

    except SubCategory.DoesNotExist:
        return JsonResponse(
            {
                "error": "SubCategory Not Found"
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
