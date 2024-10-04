from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from inventory.models import Item, Supply, Supplier
from inventory.myutils import populateRelationalFields
import json


# Supply Filter views

def listSupplyByMinQty(request, min_qty):
    """
    Retrieves a list of items from the inventory filtered by min quantity.

    Args:
        min_qty (int): The minimum quantity to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        min_qty_supplies = Supply.objects.filter(qty_supplied__gte=min_qty).order_by('qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(min_qty_supplies, pagesize)
        page_object = paginator.get_page(page)

        min_qty_supplies = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(min_qty_supplies, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply of min quantity {min_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": min_qty_supplies
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listSupplyByMaxQty(request, max_qty):
    """
    Retrieves a list of items from the inventory filtered by quantity range.

    Args:
        max_qty (int): The maximum quantity to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        max_qty_supplies = Supply.objects.filter(qty_supplied__lte=max_qty).order_by('qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(max_qty_supplies, pagesize)
        page_object = paginator.get_page(page)
        max_qty_supplies = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(max_qty_supplies, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply of max quantity {max_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "items": max_qty_supplies
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listSupplyFromMaxToMinQty(request, max_qty, min_qty):
    try:
        supply_from_min_to_max_qty = Supply.objects.filter(
            qty_supplied__lte=max_qty,
            qty_supplied__gte=min_qty,
        ).order_by('-qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(supply_from_min_to_max_qty, pagesize)
        page_object = paginator.get_page(page)

        supply_from_min_to_max_qty = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(supply_from_min_to_max_qty, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply between quantity {min_qty} and {max_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": supply_from_min_to_max_qty
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )


def listSupplyFromMinToMaxQty(request, min_qty, max_qty):
    try:
        supply_from_min_to_max_qty = Supply.objects.filter(
            qty_supplied__gte=min_qty,
            qty_supplied__lte=max_qty
        ).order_by('qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(supply_from_min_to_max_qty, pagesize)
        page_object = paginator.get_page(page)

        supply_from_min_to_max_qty = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(supply_from_min_to_max_qty, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply between quantity {min_qty} and {max_qty}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": supply_from_min_to_max_qty
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )