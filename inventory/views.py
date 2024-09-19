from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Stock, Category
import json

# Create your views here.


# Item views

def list_items(request):
    """
    Retrieves a list of item from the inventory.

    Returns:
        JsonResponse: A JSON response containing a list of item.

    Raises:
        Exception: If there is an error with the database query.
    """
    if request.method == 'GET':
        try:
            # Retrieve all item
            all_items = []
            take = Item.objects.all()
            for item in take:
                all_items.append({
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "category": item.category,
                    "sub_category": item.sub_category,
                    "recordedAt": item.recordedAt
                })
            return JsonResponse({"List_of_all_items":all_items})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
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
            
            item = Item(
                name=name,
                description=description,
                sku=sku,
                price=price,
                category=category,
                sub_category=sub_category,
            )
            item.save()

            stock = Stock(item=item, name=item.name,
                  sku=item.sku, qty_in_stock=qty_in_stock)
            
            stock.save()

            
            if Category.objects.filter(name=category).exists():
                return JsonResponse({"Message":"The item has been added"})
            
            category = Category(name=item.category, description=item.description)
            category.save()

            return JsonResponse({"Message":"The item has been added"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def retrieve_item(request, id):
    """
    Retrieves an item from the inventory by id.

    Args:
        id (int): The id of the item to retrieve

    Returns:
        JsonResponse: A JSON response containing the item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve item by id
        item = Item.objects.get(id=id)
        all_records = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "sub_category": item.sub_category,
                "recordedAt": item.recordedAt
        }
        return JsonResponse({f"The record of item {id} is":all_records})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def update_item(request, id):
    """
    Updates an item in the inventory by id.

    Args:
        id (int): The id of the item to update

    Returns:
        JsonResponse: A JSON response containing the updated item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Incomplete
        # Update item by id
        item = Item.objects.get(id=id)
        data = json.loads(request.body)
        name = data.get('name', '')
        sku = data.get('sku', '')
        price = data.get('price', 0)
        description = data.get('description', '')
        qty_in_stock = data.get('qty_in_stock', '')
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def delete_item(request, id):
    """
    Deletes an item from the inventory by id.

    Args:
        id (int): The id of the item to delete

    Returns:
        JsonResponse: A JSON response containing a success message

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Delete item by id
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# List/Retrieve -or- Searching views

def list_items_by_category(request, category):
    """
    Retrieves a list of item from the inventory filtered by category.

    Args:
        category (str): The category to filter the item by

    Returns:
        JsonResponse: A JSON response containing a list of item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve all item filtered by category
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def list_items_by_sub_category(request, sub_category):
    """
    Retrieves a list of item from the inventory filtered by sub-category.

    Args:
        sub_category (str): The sub-category to filter the item by

    Returns:
        JsonResponse: A JSON response containing a list of item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve all item filtered by sub-category
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def list_items_by_price(request, price):
    """
    Retrieves a list of item from the inventory filtered by price range.

    Args:
        min_price (int): The minimum price to filter the item by
        max_price (int): The maximum price to filter the item by

    Returns:
        JsonResponse: A JSON response containing a list of item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve all item filtered by price range
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def list_items_by_quantity(request, qty):
    """
    Retrieves a list of item from the inventory filtered by quantity range.

    Args:
        min_qty (int): The minimum quantity to filter the item by
        max_qty (int): The maximum quantity to filter the item by

    Returns:
        JsonResponse: A JSON response containing a list of item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve all item filtered by quantity range
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieve_item_by_name(request, name):
    """
    Retrieves an item from the inventory by name.

    Args:
        name (str): The name to filter the item by

    Returns:
        JsonResponse: A JSON response containing the item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve item by name
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieve_item_by_sku(request, sku):
    """
    Retrieves an item from the inventory by sku.

    Args:
        sku (str): The sku to filter the item by

    Returns:
        JsonResponse: A JSON response containing the item

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Retrieve item by sku
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
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieve_category(request, id):
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
        # Retrieve category by id
        return JsonResponse({})
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
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieve_stock(request, item):
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
        # Retrieve stock by id
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def update_stock(request, item):
    """
    Updates a stock in the inventory by id.

    Args:
        id (int): The id of the stock to update

    Returns:
        JsonResponse: A JSON response containing the updated stock

    Raises:
        Exception: If there is an error with the database query
    """
    try:
        # Update stock by id
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
