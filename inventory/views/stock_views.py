from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from users.myutils import validateToken, api_login_required
from inventory.models import Item, Stock
from inventory.myutils import populateRelationalFields
import json


# Stock views

@api_login_required
@validateToken
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

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(stock_queryset, pagesize)
        page_object = paginator.get_page(page)

        stocks_list = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(stocks_list, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks",
                "page": page,
                "pagesize": pagesize,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "stocks": stocks_list
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
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

        populateRelationalFields(stock_retrieved, ['item'], [Item])

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



@api_login_required
@validateToken
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

        populateRelationalFields(stock_updated, ['item'], [Item])

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
