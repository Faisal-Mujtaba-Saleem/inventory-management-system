from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from inventory.models import Item, Supply
from inventory.myutils import populateRelationalFields
import json


# Stock views

def listSupply(request):
    """
    Retrieves a list of all stocks in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        supply_queryset = Supply.objects.all()

        supply_list = json.loads(
            serialize('json', supply_queryset)
        )
        # populateRelationalFields(supply_list, 'item', Item)

        return JsonResponse(
            {
                "message": f"Successfully retrieved all supplies",
                "supplies": supply_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveSupply(request, item_slug):
    """
    Retrieves a stock from the inventory by item-slug.

    Args:
        item-slug (str): The slug of the item whose stock to retrieve

    Returns:
        JsonResponse: A JSON response containing the retrieved stock

    Raises:
        Item.DoesNotExist: If item with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        item = Supply.objects.get(slug=item_slug)
        item_supply = item.supply

        supply_retrieved = json.loads(
            serialize('json', [item_supply])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the supplies of the item with slug {item_slug}",
                "item_supply": supply_retrieved
            },
            status=200
        )

    except Item.DoesNotExist:
        return JsonResponse({"error": f"Item with slug {item_slug} Doesn't Exists"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateSupply(request, item_slug):
    """
    Updates a stock from the inventory by item-slug.

    Args:
        item-slug (str): The slug of the item whose stock to update

    Returns:
        JsonResponse: A JSON response containing the updated stock

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        if not request.method in ['PUT', 'PATCH']:
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405
            )

        item = Supply.objects.get(slug=item_slug)
        item_stock = item.supply

        data = json.loads(request.body)

        qty_supplied = data.get('qty_supplied', item_stock.qty_supplied)
        item_stock.qty_isupplied = qty_supplied

        item_stock.save()

        supply_updated = json.loads(

            serialize('json', [item_stock])

        )[0]

        return JsonResponse(
            {
                "message": f"Successfully updated the supply of the item with slug {item_slug}",
                "item_supply": supply_updated
            },
            status=200
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )
