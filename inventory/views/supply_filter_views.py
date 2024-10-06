from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from users.myutils import validateToken, api_login_required
from inventory.models import Item, Supply, Supplier
from inventory.myutils import populateRelationalFields
import json


# Supply Filter views


@api_login_required
@validateToken
def listSupplyByItem(request, item_slug):
    """
    Retrieves a list of supply in the inventory filtered by item slug.

    Args:
        request (HttpRequest): The request object
        item_slug (str): The slug of the item to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        item_supplies = Supply.objects.filter(item__slug=item_slug).order_by('qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(item_supplies, pagesize)
        page_object = paginator.get_page(page)

        item_supplies = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(item_supplies, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply of item with slug {item_slug}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": item_supplies
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def listSupplyBySupplierId(request, supplier_id):
    """
    Retrieves a list of supply in the inventory filtered by supplier id.

    Args:
        request (HttpRequest): The request object
        supplier_id (int): The id of the supplier to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        supplier_supplies = Supply.objects.filter(supplier__id=supplier_id).order_by('qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(supplier_supplies, pagesize)
        page_object = paginator.get_page(page)

        supplier_supplies = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(supplier_supplies, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply of supplier with id {supplier_id}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": supplier_supplies
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def listSupplyBySupplierEmail(request, supplier_email):
    """
    Retrieves a list of supply in the inventory filtered by supplier email.

    Args:
        request (HttpRequest): The request object
        supplier_email (str): The email of the supplier to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        supplier_supplies = Supply.objects.filter(supplier__email=supplier_email).order_by('qty_supplied')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(supplier_supplies, pagesize)
        page_object = paginator.get_page(page)

        supplier_supplies = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(supplier_supplies, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply of supplier with email {supplier_email}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": supplier_supplies
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listSupplyBySupplierPhone(request, supplier_phone):
    """
    Retrieves a list of supply in the inventory filtered by supplier phone.

    Args:
        request (HttpRequest): The request object
        supplier_phone (str): The phone number of the supplier to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        supplier_supplies = Supply.objects.filter(supplier__phone=supplier_phone).order_by('qty_supplied')
        print(supplier_phone)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(supplier_supplies, pagesize)
        page_object = paginator.get_page(page)

        supplier_supplies = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(supplier_supplies, ['item', 'supplier'], [Item, Supplier])

        return JsonResponse(
            {
                "message": f"Successfully retrieved supply of supplier with phone {supplier_phone}",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "supply": supplier_supplies
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_login_required
@validateToken
def listSupplyByMinQty(request, min_qty):
    """
    Retrieves a list of supply in the inventory filtered by minimum quantity.

    Args:
        request (HttpRequest): The request object
        min_qty (int): The minimum quantity to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

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


@api_login_required
@validateToken
def listSupplyByMaxQty(request, max_qty):
    """
    Retrieves a list of supplies from the inventory filtered by max quantity.

    Args:
        max_qty (int): The maximum quantity to filter the supplies by

    Returns:
        JsonResponse: A JSON response containing a list of supplies

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


@api_login_required
@validateToken
def listSupplyFromMaxToMinQty(request, max_qty, min_qty):
    """
    Retrieves a list of supply in the inventory filtered by minimum and maximum quantity.

    Args:
        request (HttpRequest): The request object
        max_qty (int): The maximum quantity to filter the supply by
        min_qty (int): The minimum quantity to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
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


@api_login_required
@validateToken
def listSupplyFromMinToMaxQty(request, min_qty, max_qty):
    """
    Retrieves a list of supply in the inventory filtered by minimum and maximum quantity.

    Args:
        request (HttpRequest): The request object
        min_qty (int): The minimum quantity to filter the supply by
        max_qty (int): The maximum quantity to filter the supply by

    Returns:
        JsonResponse: A JSON response containing a list of supply

    Raises:
        Exception: If there is an error with the database query
    """
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