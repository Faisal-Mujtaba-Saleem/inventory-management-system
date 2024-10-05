from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from users.myutils import validateToken, api_login_required
from inventory.models import Item, Supply, Supplier
from inventory.myutils import populateRelationalFields
import json


# supply views

@api_login_required
@validateToken
def listSupply(request):
    """
    Retrieves a list of all supply in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        supply_queryset = Supply.objects.all().order_by('pk')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {
                    "error": "Invalid page or pagesize."
                },
                status=400
            )
        
        paginator = Paginator(supply_queryset, pagesize)
        page_object = paginator.get_page(page)


        page = request.GET.get('page', 0)
        page = int(page)

        pagesize = request.GET.get('pagesize', 0)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {
                    "error": "Invalid page or pagesize."
                },
                status=400
            )
        
        paginator = Paginator(supply_queryset, pagesize)
        page_object = paginator.get_page(page)

        supply_list = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(
            supply_list, ["item", "supplier"], [Item, Supplier]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all supplies",
                "page": page,
                "pagesize": pagesize,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "supplies": supply_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def retrieveSupply(request, pk):
    """
    Retrieves a supply by id.

    Args:
        request: The request object
        pk: The id of the supply to retrieve

    Returns:
        JsonResponse: A JSON response containing the supply object or error message

    Raises:
        Exception: If there is an error with the database query
    """

    try:
        supply_retrieved = Supply.objects.get(pk=pk)
        supply_retrieved = json.loads(
            serialize('json', [supply_retrieved])
        )[0]

        populateRelationalFields(
            supply_retrieved, ["item", "supplier"], [Item, Supplier]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved the supply with id {pk}",
                "supply": supply_retrieved
            },
            status=200
        )

    except Supply.DoesNotExist:
        return JsonResponse(
            {"error": f"Supply with id {pk} does not exists"}, status=404
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@api_login_required
@validateToken
@csrf_exempt
def updateSupply(request, pk):
    """
    Updates a supply by id.

    Args:
        request: The request object
        pk: The id of the supply to update

    Returns:
        JsonResponse: A JSON response containing the updated supply object or error message

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        if not request.method in ['PUT', 'PATCH']:
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405
            )

        supply = Supply.objects.get(pk=pk)

        data = json.loads(request.body)
        qty_supplied = data.get('qty_supplied', supply.qty_supplied)

        supply.qty_supplied = qty_supplied
        supply.save()

        supply_updated = json.loads(
            serialize('json', [supply])
        )[0]

        populateRelationalFields(
            supply_updated, ["item", "supplier"], [Item, Supplier]
        )

        return JsonResponse(
            {
                "message": f"Successfully updated the supply with id {pk}",
                "item_supply": supply_updated
            },
            status=200
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )



@api_login_required
@validateToken
@csrf_exempt
def deleteSupply(request, pk):
    """
    Deletes a supply by id.

    Args:
        request: The request object
        pk: The id of the supply to delete

    Returns:
        JsonResponse: A JSON response containing the success message or error message

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        if request.method != 'DELETE':
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use DELETE"}, status=405
            )

        Supply.objects.get(pk=pk).delete()

        return JsonResponse(
            {
                "message": f"Successfully deleted the supply with id {pk}"
            },
            status=200
        )

    except Supply.DoesNotExist:
        return JsonResponse(
            {"error": f"Supply with id {pk} does not exists"}, status=404
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)