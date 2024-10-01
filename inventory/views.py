from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from inventory.models import Item, Category, SubCategory, Stock
from inventory.myutils2 import poulateRelatedFields
import json


# Filter & Searching views

@csrf_exempt
def listItemsByCategory(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)

        page_number = request.GET.get('page_num', 0)
        category_retrieve = request.GET.get('total_category', 0)

        page_number = int(page_number)
        category_retrieve = int(category_retrieve)

        if page_number <= 0 or category_retrieve <= 0:
            return JsonResponse({
                "Error": "Invalid page or page-size."
            })
        
        items_queryset = category.item_set.all().order_by('name')
        paginator = Paginator(items_queryset, category_retrieve)
        sub_category_list_page = paginator.get_page(page_number)
        category_list = json.loads(
            serialize('json', sub_category_list_page.object_list)
        )
        poulateRelatedFields(category_list, 'item', Item)
        return JsonResponse(
            {
                "message": f"Successfully retrieved all items",
                "items_count": paginator.count,
                "number_page": paginator.num_pages,
                "current_page": sub_category_list_page.number,
                "next_page": sub_category_list_page.has_next(),
                "previous_page": sub_category_list_page.has_previous(),
                "items": category_list
            },
            status=200
        )
    # return JsonResponse({"Error": "Item does'not exists with the given minimum price"})

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
    try:
        sub_category = SubCategory.objects.get(slug=sub_category_slug)

        page_number = request.GET.get('page_num', 0)
        sub_category_retrieve = request.GET.get('total_sub_category', 0)

        page_number = int(page_number)
        sub_category_retrieve = int(sub_category_retrieve)

        if page_number <= 0 or sub_category_retrieve <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        items_queryset = sub_category.item_set.all().order_by('name')
        paginator = Paginator(items_queryset, sub_category_retrieve)
        sub_category_list_page = paginator.get_page(page_number)
      
        sub_category_list = json.loads(
            serialize('json', sub_category_list_page.object_list)
        )
        poulateRelatedFields(sub_category_list, 'item', Item)
    
        return JsonResponse(
            {
                "message": f"Successfully retrieved all items",
                "items_count": paginator.count,
                "number_page": paginator.num_pages,
                "current_page": sub_category_list_page.number,
                "next_page": sub_category_list_page.has_next(),
                "previous_page": sub_category_list_page.has_previous(),
                "items": sub_category_list
            },
            status=200
        )

    except SubCategory.DoesNotExist:
        return JsonResponse({"error": f"SubCategory with slug {sub_category_slug} Doesn't Exists"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listItemsByMinPrice(request, min_price):
    try:
        min_price_related_items = Item.objects.filter(price__gte=min_price).order_by("price")

        page_number = request.GET.get('page_num', 0)
        item_retrieve = request.GET.get('total_items', 0)

        page_number = int(page_number)
        item_retrieve = int(item_retrieve)

        if page_number <= 0 or item_retrieve <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if min_price_related_items.exists():
            paginator = Paginator(min_price_related_items, item_retrieve)
            items_list_page = paginator.get_page(page_number)

            items_list = json.loads(
                serialize('json', items_list_page.object_list)
            )
            poulateRelatedFields(items_list, 'category', Category)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": items_list_page.number,
                    "next_page": items_list_page.has_next(),
                    "previous_page": items_list_page.has_previous(),
                    "items": items_list
                },
                status=200
            )
    
        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listItemsByMaxPrice(request, max_price):
    try:
        max_price_related_items = Item.objects.filter(price__lte=max_price).order_by("price")
        page_number = request.GET.get('page_num', 0)
        item_retrieve = request.GET.get('total_items', 0)

        page_number = int(page_number)
        item_retrieve = int(item_retrieve)

        if page_number <= 0 or item_retrieve <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if max_price_related_items.exists():
            paginator = Paginator(max_price_related_items, item_retrieve)
            items_list_page = paginator.get_page(page_number)

            items_list = json.loads(
                serialize('json', items_list_page.object_list)
            )
            poulateRelatedFields(items_list, 'category', Category)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": items_list_page.number,
                    "next_page": items_list_page.has_next(),
                    "previous_page": items_list_page.has_previous(),
                    "items": items_list
                },
                status=200
            )
    
        return JsonResponse({"Message": "Item does'not exists with the given maximum price"})
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listStocksByMinQty(request, min_qty):
    try:
        min_qty_stocks = Stock.objects.filter(qty_in_stock__gte=min_qty).order_by('-qty_in_stock')

        page = request.GET.get('page', 0)
        page = int(page)

        page_size = request.GET.get('page_size', 0)
        page_size = int(page_size)

        if page <= 0 or page_size <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if min_qty_stocks.exists():
            paginator = Paginator(min_qty_stocks, page_size)
            min_qty_stocks_list_page = paginator.get_page(page)

            min_qty_stocks_list = json.loads(
                serialize('json', min_qty_stocks_list_page.object_list)
            )
            poulateRelatedFields(min_qty_stocks_list, 'item', Item)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": page,
                    "next_page": min_qty_stocks_list_page.has_next(),
                    "previous_page": min_qty_stocks_list_page.has_previous(),
                    "items": min_qty_stocks_list
                },
                status=200
            )

        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def listStocksByMaxQty(request, max_qty):
    try:
        max_qty_stocks = Stock.objects.filter(qty_in_stock__lte=max_qty).order_by('qty_in_stock')

        page = request.GET.get('page', 0)
        page = int(page)

        page_size = request.GET.get('page_size', 0)
        page_size = int(page_size)

        if page <= 0 or page_size <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if max_qty_stocks.exists():
            paginator = Paginator(max_qty_stocks, page_size)
            max_qty_stocks_list_page = paginator.get_page(page)

            max_qty_stocks_list = json.loads(
                serialize('json', max_qty_stocks_list_page.object_list)
            )
            poulateRelatedFields(max_qty_stocks_list, 'item', Item)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": page,
                    "next_page": max_qty_stocks_list_page.has_next(),
                    "previous_page": max_qty_stocks_list_page.has_previous(),
                    "items": max_qty_stocks_list
                },
                status=200
            )

        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listItemsFromMinToMaxPrice(request, min_price, max_price):
    try:
        items_from_min_to_max_price = Item.objects.filter(
            price__gte=min_price,
            price__lte=max_price
        ).order_by('price')  # Order filtered items by price

        page = request.GET.get('page', 0)
        page = int(page)

        page_size = request.GET.get('page_size', 0)
        page_size = int(page_size)

        if page <= 0 or page_size <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if items_from_min_to_max_price.exists():
            paginator = Paginator(items_from_min_to_max_price, page_size)
            items_from_min_to_max_price_list_page = paginator.get_page(page)

            items_from_min_to_max_price_list = json.loads(
                serialize('json', items_from_min_to_max_price_list_page.object_list)
            )
            poulateRelatedFields(items_from_min_to_max_price_list, 'item', Item)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": page,
                    "next_page": items_from_min_to_max_price_list_page.has_next(),
                    "previous_page": items_from_min_to_max_price_list_page.has_previous(),
                    "items": items_from_min_to_max_price_list
                },
                status=200
            )
        
        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listItemsFromMaxToMinPrice(request, max_price, min_price):
    try:
        items_from_max_to_min_price = Item.objects.filter(
            price__lte=max_price,
            price__gte=min_price
        ).order_by('-price')

        page = request.GET.get('page', 0)
        page = int(page)

        page_size = request.GET.get('page_size', 0)
        page_size = int(page_size)

        if page <= 0 or page_size <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if items_from_max_to_min_price.exists():
            paginator = Paginator(items_from_max_to_min_price, page_size)
            items_from_max_to_min_price_list_page = paginator.get_page(page)

            items_from_max_to_min_price_list = json.loads(
                serialize('json', items_from_max_to_min_price_list_page.object_list)
            )
            poulateRelatedFields(items_from_max_to_min_price_list, 'item', Item)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": page,
                    "next_page": items_from_max_to_min_price_list_page.has_next(),
                    "previous_page": items_from_max_to_min_price_list_page.has_previous(),
                    "items": items_from_max_to_min_price_list
                },
                status=200
            )
        
        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listStocksFromMaxToMinQty(request, max_qty, min_qty):
    try:
        stocks_from_max_to_min_qty = Stock.objects.filter(
            qty_in_stock__lte=max_qty,
            qty_in_stock__gte=min_qty,
        ).order_by('-qty_in_stock')

        page = request.GET.get('page', 0)
        page = int(page)

        page_size = request.GET.get('page_size', 0)
        page_size = int(page_size)

        if page <= 0 or page_size <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if stocks_from_max_to_min_qty.exists():
            paginator = Paginator(stocks_from_max_to_min_qty, page_size)
            stocks_from_max_to_min_qty_list_page = paginator.get_page(page)

            stocks_from_max_to_min_qty_list = json.loads(
                serialize('json', stocks_from_max_to_min_qty_list_page.object_list)
            )
            poulateRelatedFields(stocks_from_max_to_min_qty_list, 'item', Item)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": page,
                    "next_page": stocks_from_max_to_min_qty_list_page.has_next(),
                    "previous_page": stocks_from_max_to_min_qty_list_page.has_previous(),
                    "items": stocks_from_max_to_min_qty_list
                },
                status=200
            )
        
        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})
    
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
        page = int(page)

        page_size = request.GET.get('page_size', 0)
        page_size = int(page_size)

        if page <= 0 or page_size <= 0:
            return JsonResponse({
                "Error": "Ensure page_num and total_items are positive integers."
            })
        
        if stocks_from_min_to_max_qty.exists():
            paginator = Paginator(stocks_from_min_to_max_qty, page_size)
            stocks_from_min_to_max_qty_list_page = paginator.get_page(page)

            stocks_from_min_to_max_qty_list = json.loads(
                serialize('json', stocks_from_min_to_max_qty_list_page.object_list)
            )
            poulateRelatedFields(stocks_from_min_to_max_qty_list, 'item', Item)

            return JsonResponse(
                {
                    "message": f"Successfully retrieved all items",
                    "items_count": paginator.count,
                    "number_page": paginator.num_pages,
                    "current_page": page,
                    "next_page": stocks_from_min_to_max_qty_list_page.has_next(),
                    "previous_page": stocks_from_min_to_max_qty_list_page.has_previous(),
                    "items": stocks_from_min_to_max_qty_list
                },
                status=200
            )
        
        return JsonResponse({"Error": "Item does'not exists with the given minimum price"})
    
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

        poulateRelatedFields(items, 'category', Category)

        return JsonResponse({"name": items})

    except Category.DoesNotExist:
        return JsonResponse({"error": "Category does not exist"}, status=404)

    except SubCategory.DoesNotExist:
        return JsonResponse({"error": "SubCategory does not exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.serializers import serialize
# from django.shortcuts import get_object_or_404
# from django.utils.text import slugify
# from django.http import Http404
# from .models import Item, Stock, Category
# # from .myutils import restrict_cors
# import json


# # Views here.


# # # Item views

# # @restrict_cors
# def list_items(request):
#     """
#     Retrieves a list of item from the inventory.

#     Returns:
#         JsonResponse: A JSON response containing a list of item.

#     Raises:
#         Exception: If there is an error with the database query.
#     """
#     try:
#         # Retrieve all item
#         items_queryset = Item.objects.all()

#         items_list = json.loads(
#             serialize('json', items_queryset)
#         )

#         return JsonResponse({"items": items_list})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# # @restrict_cors
# def retrieve_item(request, slug):
#     """
#     Retrieves an item from the inventory by slug.

#     Args:
#         slug (str): The slug of the item to retrieve

#     Returns:
#         JsonResponse: A JSON response containing the item

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     try:
#         # Retrieve item by slug
#         item_retrieved = get_object_or_404(Item, slug=slug)

#         item_retrieved = json.loads(
#             serialize('json', [item_retrieved])
#         )[0]

#         return JsonResponse(
#             {
#                 "message": f"Successfully retrieved the item with slug {slug}",
#                 "item": item_retrieved
#             }
#         )

#     except Http404:
#         return JsonResponse({"error": f"Item with slug {slug} not found"}, status=404)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# @csrf_exempt
# # @restrict_cors
# def create_item(request):
#     """
#     Creates a new item in the inventory.

#     Returns:
#         JsonResponse: A JSON response containing the created item

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'POST':
#         try:
#             # Create item
#             data = json.loads(request.body)

#             name = data.get('name', '')
#             sku = data.get('sku', '')
#             price = data.get('price', 0)
#             description = data.get('description', '')
#             category = data.get('category', '')
#             sub_category = data.get('sub_category', '')
#             qty_in_stock = data.get('qty_in_stock', '')

#             if Category.objects.filter(name=category).exists():
#                 category = Category.objects.get(name=category)

#             else:
#                 category = Category(
#                     name=item.category,
#                     description=item.description
#                 )
#                 category.save()

#             item = Item(
#                 name=name,
#                 description=description,
#                 sku=sku,
#                 price=price,
#                 category=category,
#                 sub_category=sub_category,
#             )
#             item.save()

#             item_created = json.loads(
#                 serialize('json', [item])
#             )[0]

#             stock = Stock(item=item, name=item.name,
#                           sku=item.sku, qty_in_stock=qty_in_stock)

#             stock.save()

#             return JsonResponse({
#                 "Message": "Successfully added the item",
#                 "item": item_created
#             })

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": f"Request method {request.method} not allowed, use POST"}, status=405)


# @csrf_exempt
# # @restrict_cors
# def update_item(request, slug):
#     """
#     Updates an item in the inventory by slug.

#     Args:
#         slug (str): The slug of the item to update

#     Returns:
#         JsonResponse: A JSON response containing the updated item

#     Raises:
#         Exception: If there is an error with the database query
#     """

#     if request.method == 'PUT' or request.method == 'PATCH':
#         try:
#             # Update item by slug

#             item = Item.objects.get(slug=slug)
#             data = json.loads(request.body)

#             if isinstance(data, dict):
#                 for field in data:
#                     if field != 'slug':
#                         print(field)
#                         if field == 'sku':
#                             item.sku = data[field]
#                             item.slug = slugify(item.sku)
#                             continue

#                         item.__setattr__(field, data[field])
#                     else:
#                         return JsonResponse({"error": "Updating slug not allowed"}, status=400)

#                 item.save()
#             else:
#                 return JsonResponse({"error": "Invalid data format. Please provide a dictionary"}, status=400)

#             item_updated = json.loads(
#                 serialize('json', [item])
#             )[0]

#             return JsonResponse({
#                 "Message": f"The item with slug {slug} has been updated succesfully",
#                 "item": item_updated
#             })
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)


# @csrf_exempt
# # @restrict_cors
# def delete_item(request, slug):
#     """
#     Deletes an item from the inventory by slug.

#     Args:
#         slug (str): The slug of the item to delete

#     Returns:
#         JsonResponse: A JSON response containing a success message

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'DELETE':
#         try:
#             # Delete item by slug
#             item_to_delete = Item.objects.get(slug=slug)
#             item_to_delete.delete()

#             return JsonResponse({"Message": f"The item with slug {slug} has been deleted succesfully"})

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": f"Request method {request.method} not allowed, use DELETE"}, status=405)


# # Filter & Searching views

# def list_items_by_category(request, category):
#     """
#     Retrieves a list of items from the inventory filtered by category.

#     Args:
#         category (str): The category to filter the items by

#     Returns:
#         JsonResponse: A JSON response containing a list of items

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'GET':
#         try:
#             # Retrieve all items filtered by category
#             category_related_items = Item.objects.filter(category=category)
#             serialized_items = json.loads(
#                 serialize('json', category_related_items)
#             )

#             return JsonResponse({f"List of all items of category {category}":serialized_items})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

# def list_items_by_sub_category(request, sub_category):
#     """
#     Retrieves a list of items from the inventory filtered by sub-category.

#     Args:
#         sub_category (str): The sub-category to filter the items by

#     Returns:
#         JsonResponse: A JSON response containing a list of items

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'GET':
#         try:
#             # Retrieve all items filtered by sub-category
#             sub_category_related_items = Item.objects.filter(sub_category=sub_category)

#             serialized_items = json.loads(
#                 serialize('json', sub_category_related_items)
#             )

#             return JsonResponse({f"List of all items of category {sub_category}":serialized_items})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# def list_items_by_max_price(request, max_price):
#     """
#     Retrieves a list of items from the inventory filtered by price range.

#     Args:
#         min_price (int): The minimum price to filter the items by
#         max_price (int): The maximum price to filter the items by

#     Returns:
#         JsonResponse: A JSON response containing a list of items

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'GET':
#         try:
#             # Retrieve all items filtered by price range
#             max_price_related_items = Item.objects.filter(price__lte=max_price)

#             a = json.loads(serialize('json', max_price_related_items))

#             return JsonResponse({f"The items of max price {max_price} is":a})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# def list_items_by_max_quantity(request, max_qty):
#     """
#     Retrieves a list of items from the inventory filtered by quantity range.

#     Args:
#         min_qty (int): The minimum quantity to filter the items by
#         max_qty (int): The maximum quantity to filter the items by

#     Returns:
#         JsonResponse: A JSON response containing a list of items

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'GET':
#         try:
#             # Retrieve all items filtered by quantity range

#             max_qty_related_items = Stock.objects.filter(qty_in_stock__lte=max_qty)

#             serialized_items = json.loads(serialize('json', max_qty_related_items))

#             return JsonResponse({f"The items of max price {max_qty} is":serialized_items})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# def search_items(request):
#     """
#     Retrieves an item from the inventory by name.

#     Args:
#         name (str): The name to filter the items by

#     Returns:
#         JsonResponse: A JSON response containing the item

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     try:
#         name = request.GET.get('name', '')
#         sku = request.GET.get('sku', '')
#         qty = request.GET.get('qty', '')
#         category = request.GET.get('category', '')
#         sub_category = request.GET.get('sub_category', '')
#         price = request.GET.get('price', '')

#         return JsonResponse({})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# # Category views

# def list_categories(request):
#     """
#     Retrieves a list of all categories in the inventory.

#     Returns:
#         JsonResponse: A JSON response containing a list of categories

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     try:
#         # Retrieve all categories
#         all_categories = Category.objects.all()
#         item_retrieved = json.loads(
#             serialize('json', all_categories)
#         )
#         return JsonResponse({"All Categories": item_retrieved})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# def retrieve_category(request, slug):
#     """
#     Retrieves a category from the inventory by id.

#     Args:
#         id (int): The id of the category to retrieve

#     Returns:
#         JsonResponse: A JSON response containing the category

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     try:
#         # Retrieve category by slug
#         category_retrieve = get_object_or_404(Category, slug=slug)

#         category = json.loads(
#             serialize(
#                 'json',
#                 [category_retrieve]
#             )
#         )

#         return JsonResponse({f"The category of slug {slug} is":category})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# # Stock views

# def list_stocks(request):
#     """
#     Retrieves a list of all stocks in the inventory.

#     Returns:
#         JsonResponse: A JSON response containing a list of stocks

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     try:
#         # Retrieve all stocks
#         all_stocks = Stock.objects.all()

#         item_retrieved = json.loads(
#             serialize('json', all_stocks)
#         )
        
#         return JsonResponse({"All stocks": item_retrieved})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


# def retrieve_stock(request, slug):
#     """
#     Retrieves a stock from the inventory by id.

#     Args:
#         id (int): The id of the stock to retrieve

#     Returns:
#         JsonResponse: A JSON response containing the stock

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     try:
#         # Retrieve item by id
#         item_retrieved = get_object_or_404(Stock, slug=slug)

#         item_retrieved = json.loads(
#             serialize('json', [item_retrieved])
#         )[0]

#         return JsonResponse(
#             {
#                 "message": f"Successfully retrieved the item with id {slug}",
#                 "item": item_retrieved
#             }
#         )

#     except Http404:
#         return JsonResponse({"error": f"Item with id {id} not found"}, status=404)
    
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

# @csrf_exempt
# def update_stock(request, slug):
#     """
#     Updates a stock in the inventory by id.

#     Args:
#         id (int): The id of the stock to update

#     Returns:
#         JsonResponse: A JSON response containing the updated stock

#     Raises:
#         Exception: If there is an error with the database query
#     """
#     if request.method == 'PUT' or request.method == 'PATCH':
#         try:
#             # Update item by id
#             stock = Stock.objects.get(slug=slug)

#             data = json.loads(request.body)

#             if isinstance(data, dict):
#                 for particular in data:
#                     if data[particular] != '':
#                         stock.__setattr__(particular, data[particular])

#             else:
#                 return JsonResponse({"error": "Invalid data format"}, status=400)

#             stock_updated = json.loads(
#                 serialize('json', [stock])
#             )[0]

#             stock.save()
            
#             return JsonResponse({
#                 "Message": f"The item with id {id} has been updated succesfully",
#                 "item": stock_updated
#             })
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)
