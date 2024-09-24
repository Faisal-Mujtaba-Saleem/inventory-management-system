from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.http import Http404
from .models import Item, Stock, Category
# from .myutils import restrict_cors
import json


# Views here.


# # Item views

# @restrict_cors
def list_items(request):
    """
    Retrieves a list of item from the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of item.

    Raises:
        Exception: If there is an error with the database query.
    """
    try:
        # Retrieve all item
        items_queryset = Item.objects.all()

        items_list = json.loads(
            serialize('json', items_queryset)
        )

        return JsonResponse({"items": items_list})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# @restrict_cors
def retrieve_item(request, slug):
    """
    Retrieves an item from the inventory by slug.

    Args:
        slug (str): The slug of the item to retrieve

    Returns:
        JsonResponse: A JSON response containing the item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve item by slug
        item_retrieved = get_object_or_404(Item, slug=slug)

        item_retrieved = json.loads(
            serialize('json', [item_retrieved])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the item with slug {slug}",
                "item": item_retrieved
            }
        )

    except Http404:
        return JsonResponse({"error": f"Item with slug {slug} not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
# @restrict_cors
def create_item(request):
    """
    Creates a new item in the inventory.

    Returns:
        JsonResponse: A JSON response containing the created item

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'POST':
        try:
            # Create item
            data = json.loads(request.body)

            name = data.get('name', '')
            sku = data.get('sku', '')
            price = data.get('price', 0)
            description = data.get('description', '')
            category = data.get('category', '')
            sub_category = data.get('sub_category', '')
            qty_in_stock = data.get('qty_in_stock', '')

            if Category.objects.filter(name=category).exists():
                category = Category.objects.get(name=category)

            else:
                category = Category(
                    name=item.category,
                    description=item.description
                )
                category.save()

            item = Item(
                name=name,
                description=description,
                sku=sku,
                price=price,
                category=category,
                sub_category=sub_category,
            )
            item.save()

            item_created = json.loads(
                serialize('json', [item])
            )[0]

            stock = Stock(item=item, name=item.name,
                          sku=item.sku, qty_in_stock=qty_in_stock)

            stock.save()

            return JsonResponse({
                "Message": "Successfully added the item",
                "item": item_created
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": f"Request method {request.method} not allowed, use POST"}, status=405)


@csrf_exempt
# @restrict_cors
def update_item(request, slug):
    """
    Updates an item in the inventory by slug.

    Args:
        slug (str): The slug of the item to update

    Returns:
        JsonResponse: A JSON response containing the updated item

    Raises:
        Exception: If there is an error with the database query
    """

    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            # Update item by slug

            item = Item.objects.get(slug=slug)
            data = json.loads(request.body)

            if isinstance(data, dict):
                for field in data:
                    if field != 'slug':
                        print(field)
                        if field == 'sku':
                            item.sku = data[field]
                            item.slug = slugify(item.sku)
                            continue

                        item.__setattr__(field, data[field])
                    else:
                        return JsonResponse({"error": "Updating slug not allowed"}, status=400)

                item.save()
            else:
                return JsonResponse({"error": "Invalid data format. Please provide a dictionary"}, status=400)

            item_updated = json.loads(
                serialize('json', [item])
            )[0]

            return JsonResponse({
                "Message": f"The item with slug {slug} has been updated succesfully",
                "item": item_updated
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)


@csrf_exempt
# @restrict_cors
def delete_item(request, slug):
    """
    Deletes an item from the inventory by slug.

    Args:
        slug (str): The slug of the item to delete

    Returns:
        JsonResponse: A JSON response containing a success message

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'DELETE':
        try:
            # Delete item by slug
            item_to_delete = Item.objects.get(slug=slug)
            item_to_delete.delete()

            return JsonResponse({"Message": f"The item with slug {slug} has been deleted succesfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": f"Request method {request.method} not allowed, use DELETE"}, status=405)


# Filter & Searching views

def list_items_by_category(request, category):
    """
    Retrieves a list of items from the inventory filtered by category.

    Args:
        category (str): The category to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'GET':
        try:
            # Retrieve all items filtered by category
            category_related_items = Item.objects.filter(category=category)
            serialized_items = json.loads(
                serialize('json', category_related_items)
            )

            return JsonResponse({f"List of all items of category {category}":serialized_items})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def list_items_by_sub_category(request, sub_category):
    """
    Retrieves a list of items from the inventory filtered by sub-category.

    Args:
        sub_category (str): The sub-category to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'GET':
        try:
            # Retrieve all items filtered by sub-category
            sub_category_related_items = Item.objects.filter(sub_category=sub_category)

            serialized_items = json.loads(
                serialize('json', sub_category_related_items)
            )

            return JsonResponse({f"List of all items of category {sub_category}":serialized_items})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def list_items_by_max_price(request, max_price):
    """
    Retrieves a list of items from the inventory filtered by price range.

    Args:
        min_price (int): The minimum price to filter the items by
        max_price (int): The maximum price to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'GET':
        try:
            # Retrieve all items filtered by price range
            max_price_related_items = Item.objects.filter(price__lte=max_price)

            a = json.loads(serialize('json', max_price_related_items))

            return JsonResponse({f"The items of max price {max_price} is":a})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def list_items_by_max_quantity(request, max_qty):
    """
    Retrieves a list of items from the inventory filtered by quantity range.

    Args:
        min_qty (int): The minimum quantity to filter the items by
        max_qty (int): The maximum quantity to filter the items by

    Returns:
        JsonResponse: A JSON response containing a list of items

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'GET':
        try:
            # Retrieve all items filtered by quantity range

            max_qty_related_items = Stock.objects.filter(qty_in_stock__lte=max_qty)

            serialized_items = json.loads(serialize('json', max_qty_related_items))

            return JsonResponse({f"The items of max price {max_qty} is":serialized_items})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def search_items(request):
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
        name = request.GET.get('name', '')
        sku = request.GET.get('sku', '')
        qty = request.GET.get('qty', '')
        category = request.GET.get('category', '')
        sub_category = request.GET.get('sub_category', '')
        price = request.GET.get('price', '')

        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Category views

def list_categories(request):
    """
    Retrieves a list of all categories in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of categories

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve all categories
        all_categories = Category.objects.all()
        item_retrieved = json.loads(
            serialize('json', all_categories)
        )
        return JsonResponse({"All Categories": item_retrieved})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieve_category(request, slug):
    """
    Retrieves a category from the inventory by id.

    Args:
        id (int): The id of the category to retrieve

    Returns:
        JsonResponse: A JSON response containing the category

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve category by slug
        category_retrieve = get_object_or_404(Category, slug=slug)

        category = json.loads(
            serialize(
                'json',
                [category_retrieve]
            )
        )

        return JsonResponse({f"The category of slug {slug} is":category})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Stock views

def list_stocks(request):
    """
    Retrieves a list of all stocks in the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of stocks

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve all stocks
        all_stocks = Stock.objects.all()

        item_retrieved = json.loads(
            serialize('json', all_stocks)
        )
        
        return JsonResponse({"All stocks": item_retrieved})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieve_stock(request, slug):
    """
    Retrieves a stock from the inventory by id.

    Args:
        id (int): The id of the stock to retrieve

    Returns:
        JsonResponse: A JSON response containing the stock

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve item by id
        item_retrieved = get_object_or_404(Stock, slug=slug)

        item_retrieved = json.loads(
            serialize('json', [item_retrieved])
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the item with id {slug}",
                "item": item_retrieved
            }
        )

    except Http404:
        return JsonResponse({"error": f"Item with id {id} not found"}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_stock(request, slug):
    """
    Updates a stock in the inventory by id.

    Args:
        id (int): The id of the stock to update

    Returns:
        JsonResponse: A JSON response containing the updated stock

    Raises:
        Exception: If there is an error with the database query
    """
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            # Update item by id
            stock = Stock.objects.get(slug=slug)

            data = json.loads(request.body)

            if isinstance(data, dict):
                for particular in data:
                    if data[particular] != '':
                        stock.__setattr__(particular, data[particular])

            else:
                return JsonResponse({"error": "Invalid data format"}, status=400)

            stock_updated = json.loads(
                serialize('json', [stock])
            )[0]

            stock.save()
            
            return JsonResponse({
                "Message": f"The item with id {id} has been updated succesfully",
                "item": stock_updated
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)
