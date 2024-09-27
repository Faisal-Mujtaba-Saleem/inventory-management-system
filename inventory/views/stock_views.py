from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from inventory.models import Item, Stock
import json


# Stock views

def listStocks(request):
    """
    Retrieves a list of all stocks in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        stock_queryset = Stock.objects.all()
        stocks_list = json.loads(
            serialize('json', stock_queryset)
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks",
                "stocks": stocks_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveStock(request, item_slug):
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
        item = Item.objects.get(slug=item_slug)
        item_stock = item.stock

        stock_retrieved = json.loads(
            serialize('json', [item_stock])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the stock of the item with slug {item_slug}",
                "item_stock": stock_retrieved
            },
            status=200
        )

    except Item.DoesNotExist:
        return JsonResponse({"error": f"Item with slug {item_slug} Doesn't Exists"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateStock(request, item_slug):
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

        item = Item.objects.get(slug=item_slug)
        item_stock = item.stock

        data = json.loads(request.body)

        qty_in_stock = data.get('qty_in_stock', item_stock.qty_in_stock)
        item_stock.qty_in_stock = qty_in_stock

        item_stock.save()

        stock_updated = json.loads(

            serialize('json', [item_stock])

        )[0]

        return JsonResponse(
            {
                "message": f"Successfully updated the stock of the item with slug {item_slug}",
                "item_stock": stock_updated
            },
            status=200
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )
