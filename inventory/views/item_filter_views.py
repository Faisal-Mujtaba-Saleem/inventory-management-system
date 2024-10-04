from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from inventory.models import Item, Category, SubCategory, Stock
from inventory.myutils import populateRelationalFields
import json


# Item-Filter Views.

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
        category_related_items = category.item_set.all().order_by('category')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(category_related_items, pagesize)
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
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
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
        sub_category_related_items = sub_category.item_set.all().order_by('sub_category')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(sub_category_related_items, pagesize)
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
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "items": sub_category_related_items
            },
            status=200
        )

    except SubCategory.DoesNotExist:
        return JsonResponse({"error": f"SubCategory with slug {sub_category_slug} Doesn't Exists"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
        min_price_related_items = Item.objects.filter(price__gte=min_price).order_by('price')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(min_price_related_items, page, pagesize)
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
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "items": min_price_related_items
            },
            status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
        max_price_related_items = Item.objects.filter(price__lte=max_price).order_by('price')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(max_price_related_items, pagesize)
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
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "items": max_price_related_items
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

        paginator = Paginator(items_from_min_to_max_price, pagesize)
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
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
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

        paginator = Paginator(items_from_max_to_min_price, pagesize)
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
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "Items": items_from_max_to_min_price
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
            'stock__qty_in_stock': request.GET.get('qty_in_stock', ''),
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
