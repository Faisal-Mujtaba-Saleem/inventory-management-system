from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from inventory.models import Item, Category, SubCategory, Stock
from inventory.myutils import populateRelationalFields
import json


# Filter & Searching views

@csrf_exempt
def listItemsByCategory(request, category_slug):
    """
    List all items filtered by category.

    Args:
        request: The request object
        category_slug: The slug of the category

    Returns:
        JsonResponse: The list of items filtered by category

    Raises:
        Category.DoesNotExist: If category with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        category = Category.objects.get(slug=category_slug)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(category.item_set.all(), pagesize)
        page_object = paginator.get_page(page)

        category_related_items = json.loads(
            serialize(
                'json', page_object.object_list
            )
        )

        populateRelationalFields(category_related_items, [
            'category', 'sub_category'], [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of category {category}",
                "items_count": len(category_related_items),
                "items": category_related_items
            },
            status=200
        )

    except Category.DoesNotExist:
        return JsonResponse(
            {"error": f"Category with slug {category_slug} Doesn't Exists"}, status=404
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )


@csrf_exempt
def listItemsBySubCategory(request, sub_category_slug):
    """
    List all items filtered by sub-category.

    Args:
        request: The request object
        sub_category_slug: The slug of the sub-category

    Returns:
        JsonResponse: The list of items filtered by sub-category

    Raises:
        SubCategory.DoesNotExist: If sub-category with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        sub_category = SubCategory.objects.get(slug=sub_category_slug)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(sub_category.item_set.all(), pagesize)
        page_object = paginator.get_page(page)

        sub_category_related_items = json.loads(
            serialize(
                'json', page_object.object_list
            )
        )

        populateRelationalFields(sub_category_related_items, [
            'category', 'sub_category'], [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of sub-category {sub_category}",
                "items_count": len(sub_category_related_items),
                "items": sub_category_related_items
            },
            status=200
        )

    except SubCategory.DoesNotExist:
        return JsonResponse({"error": f"SubCategory with slug {sub_category_slug} Doesn't Exists"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listItemsByMinPrice(request, min_price):
    """
    Retrieves a list of items from the inventory filtered by min price.

    Args:
        min_price (int): The minimum price to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        min_price_related_items = Item.objects.filter(price__gte=min_price)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(min_price_related_items)
        page_object = paginator.get_page(page)

        min_price_related_items = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(min_price_related_items, [
            'category', 'sub_category'], [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of max price {min_price}",
                "items_count": len(min_price_related_items),
                "items": min_price_related_items
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listItemsByMaxPrice(request, max_price):
    """
    Retrieves a list of items from the inventory filtered by max price.

    Args:
        max_price (int): The maximum price to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        max_price_related_items = Item.objects.filter(price__lte=max_price)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(max_price_related_items)
        page_object = paginator.get_page(page)

        max_price_related_items = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(max_price_related_items, [
            'category', 'sub_category'], [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of max price {max_price}",
                "items_count": len(max_price_related_items),
                "items": max_price_related_items
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listStocksByMinQty(request, min_qty):
    """
    Retrieves a list of items from the inventory filtered by minimum quantity.

    Args:
        min_qty (int): The minimum quantity to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        min_qty_stocks = Stock.objects.filter(qty_in_stock__gte=min_qty)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(min_qty_stocks)
        page_object = paginator.get_page(page)

        min_qty_stocks = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(min_qty_stocks, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of min quantity {min_qty}",
                "items_count": len(min_qty_stocks),
                "items": min_qty_stocks
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listStocksByMaxQty(request, max_qty):
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
        max_qty_stocks = Stock.objects.filter(qty_in_stock__lte=max_qty)

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(max_qty_stocks)
        page_object = paginator.get_page(page)

        max_qty_stocks = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(max_qty_stocks, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items of max quantity {max_qty}",
                "items_count": len(max_qty_stocks),
                "items": max_qty_stocks
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listItemsFromMinToMaxPrice(request, min_price, max_price):
    try:
        items_from_min_to_max_price = Item.objects.filter(
            price__gte=min_price,
            price__lte=max_price
        ).order_by('price')  # Order filtered items by price

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(items_from_min_to_max_price)
        page_object = paginator.get_page(page)

        items_from_min_to_max_price = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(items_from_min_to_max_price, [
            'category', 'sub_category'], [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items between price {min_price} and {max_price}",
                "items_count": len(items_from_min_to_max_price),
                "Items": items_from_min_to_max_price
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listItemsFromMaxToMinPrice(request, max_price, min_price):
    try:
        items_from_max_to_min_price = Item.objects.filter(
            price__lte=max_price,
            price__gte=min_price
        ).order_by('-price')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(items_from_max_to_min_price)
        page_object = paginator.get_page(page)

        items_from_max_to_min_price = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(items_from_max_to_min_price, [
            'category', 'sub_category'], [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all items between price {max_price} and {min_price}",
                "items_count": len(items_from_max_to_min_price),
                "Items": items_from_max_to_min_price
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listStocksFromMaxToMinQty(request, max_qty, min_qty):
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

        paginator = Paginator(stocks_from_min_to_max_qty)
        page_object = paginator.get_page(page)

        stocks_from_min_to_max_qty = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(stocks_from_min_to_max_qty, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks between quantity {min_qty} and {max_qty}",
                "stocks": len(stocks_from_min_to_max_qty),
                "Items": stocks_from_min_to_max_qty
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )


def listStocksFromMinToMaxQty(request, min_qty, max_qty):
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

        paginator = Paginator(stocks_from_min_to_max_qty)
        page_object = paginator.get_page(page)

        stocks_from_min_to_max_qty = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(stocks_from_min_to_max_qty, ['item'], [Item])

        return JsonResponse(
            {
                "message": f"Successfully retrieved all stocks between quantity {min_qty} and {max_qty}",
                "stocks_count": len(stocks_from_min_to_max_qty),
                "Items": stocks_from_min_to_max_qty
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )


@csrf_exempt
def searchItems(request):
    """
    Retrieves an item from the inventory by name.

    Args:
        name (str): The name to filter the items by

    Returns:
        JsonResponse: A JSON response containing the item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        category = request.GET.get('category', '')
        sub_category = request.GET.get('sub_category', '')

        if category != '':
            category = Category.objects.get(name__iexact=category)
            category = category.id

        if sub_category != '':
            sub_category = SubCategory.objects.get(name__iexact=sub_category)
            sub_category = sub_category.id

        queries = {
            'name__icontains': request.GET.get('name', ''),
            'stock__qty_in_stock': request.GET.get('qty', ''),
            'category': category,
            'sub_category': sub_category,
            'price': request.GET.get('price', ''),
        }
        queries = {key: value for key, value in queries.items() if value != ''}

        items = Item.objects.filter(**queries)
        items = json.loads(serialize('json', items))

        populateRelationalFields(items, ['category', 'sub_category'], [
            Category, SubCategory]
        )

        return JsonResponse({"name": items})

    except Category.DoesNotExist:
        return JsonResponse({"error": "Category does not exist"}, status=404)

    except SubCategory.DoesNotExist:
        return JsonResponse({"error": "SubCategory does not exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
