from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from users.myutils import validateToken,api_login_required
from inventory.models import Item, Stock
from inventory.myutils import populateRelationalFields
import json


# Stock Filter views

@api_login_required
@validateToken
def listStocksByMinQty(request, min_qty):        
    """
    Retrieves a list of all stocks in the inventory filtered by min quantity.

    Args:
        min_qty (int): The minimum quantity to filter the stocks by

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        min_qty_stocks = Stock.objects.filter(qty_in_stock__gte=min_qty).order_by('qty_in_stock')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(min_qty_stocks, pagesize)
        page_object = paginator.get_page(page)

        min_qty_stocks = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(min_qty_stocks, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of min quantity {min_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "stocks": min_qty_stocks
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def listStocksByMaxQty(request, max_qty):
    """
    Retrieves a list of all stocks in the inventory filtered by max quantity.

    Args:
        max_qty (int): The maximum quantity to filter the stocks by

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        max_qty_stocks = Stock.objects.filter(qty_in_stock__lte=max_qty).order_by('qty_in_stock')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(max_qty_stocks, pagesize)
        page_object = paginator.get_page(page)

        max_qty_stocks = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(max_qty_stocks, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of max quantity {max_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "stocks": max_qty_stocks
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def listStocksFromMaxToMinQty(request, max_qty, min_qty):
    """
        Retrieves a list of all stocks in the inventory filtered by min and max quantity.

        Args:
            min_qty (int): The minimum quantity to filter the stocks by
            max_qty (int): The maximum quantity to filter the stocks by

        Returns:
            JsonResponse: A JSON response containing a list of stocks

        Raises:
            Exception: If there is an error with the database query
    """        
    try:
        stocks_from_min_to_max_qty = Stock.objects.filter(
            qty_in_stock__lte=max_qty,
            qty_in_stock__gte=min_qty,
        ).order_by('-qty_in_stock')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(stocks_from_min_to_max_qty, pagesize)
        page_object = paginator.get_page(page)

        stocks_from_min_to_max_qty = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(stocks_from_min_to_max_qty, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks between quantity {min_qty} and {max_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "stocks": stocks_from_min_to_max_qty
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )


@api_login_required
@validateToken
def listStocksFromMinToMaxQty(request, min_qty, max_qty):
    """
    Retrieves a list of all stocks in the inventory filtered by min and max quantity.

    Args:
        min_qty (int): The minimum quantity to filter the stocks by
        max_qty (int): The maximum quantity to filter the stocks by

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        stocks_from_min_to_max_qty = Stock.objects.filter(
            qty_in_stock__gte=min_qty,
            qty_in_stock__lte=max_qty
        ).order_by('qty_in_stock')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(stocks_from_min_to_max_qty, pagesize)
        page_object = paginator.get_page(page)

        stocks_from_min_to_max_qty = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(stocks_from_min_to_max_qty, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks between quantity {min_qty} and {max_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "stocks": stocks_from_min_to_max_qty
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )