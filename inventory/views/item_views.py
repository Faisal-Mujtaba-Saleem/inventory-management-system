from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.myutils import validateToken, api_login_required
from inventory.models import Item, Category, SubCategory, Stock
from inventory.myutils import populateRelationalFields
import json


# # Item views
@api_login_required
@validateToken
def listItems(request):
    """
    Return a list of all items in the database.

    Returns:
        JsonResponse: A list of all items in the database
    """
    try:
        items_queryset = Item.objects.all().order_by('pk')

        page = request.GET.get('page', 0)
        pagesize = request.GET.get('pagesize', 0)

        page = int(page)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {"error": "Invalid page or pagesize."}, status=400
            )

        paginator = Paginator(items_queryset, pagesize)
        page_object = paginator.get_page(page)

        items_list = json.loads(
            serialize('json', page_object.object_list)
        )

        populateRelationalFields(
            items_list, ['category', 'sub_category'],
            [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": "Successfully retrieved all items",
                "page": page,
                "pagesize": pagesize,
                'total_pages': paginator.num_pages,
                "total_results": paginator.count,
                "items": items_list
            },
            status=200
        )
    
    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )

@api_login_required
@validateToken
def retrieveItem(request, item_slug):
    """
    Retrieve a specific item by slug.

    Args:
        request: The request object
        item_slug: The slug of the item to retrieve

    Returns:
        JsonResponse: The item with the matching slug

    Raises:
        Item.DoesNotExist: If item with slug doesn't exist
        Exception: If any other exception occurs
    """
    try:
        item_retrieved = Item.objects.get(slug=item_slug)
        item_retrieved = json.loads(
            serialize('json', [item_retrieved])
        )[0]

        populateRelationalFields(
            item_retrieved, ['category', 'sub_category'],
            [Category, SubCategory]
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved the item with slug {item_slug}",
                "item": item_retrieved
            },
            status=200
        )

    except Item.DoesNotExist:
        return JsonResponse(
            {"error": f"Item with slug {item_slug} Doesn't Exists"}, status=404
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )


@api_login_required
@validateToken
@csrf_exempt
def createItem(request):
    """
    Create an item.

    Args:
        request: The request object

    Returns:
        JsonResponse: The created item

    Raises:
        Exception: If any exception occurs
    """
    try:
        if request.method == 'POST':
            data = json.loads(request.body)

            name = data.get('name', '')
            sku = data.get('sku', '')
            price = data.get('price', 0)
            description = data.get('description', '')
            category = data.get('category', '')
            sub_category = data.get('sub_category', '')
            qty_in_stock = data.get('qty_in_stock', '')

            category = Category.objects.get_or_create(
                name=category,
            )[0]

            sub_category = SubCategory.objects.get_or_create(
                name=sub_category,
                category=category
            )[0]

            item = Item.objects.create(
                name=name,
                description=description,
                sku=sku,
                price=price,
                category=category,
                sub_category=sub_category,
            )

            Stock.objects.create(
                item=item, qty_in_stock=qty_in_stock
            )

            item_created = json.loads(
                serialize('json', [item])
            )[0]

            populateRelationalFields(
                item_created, ['category', 'sub_category'],
                [Category, SubCategory]
            )

            return JsonResponse(
                {
                    "message": "Successfully added the item",
                    "item": item_created
                },
                status=201
            )

        return JsonResponse(
            {"error": f"Request method {request.method} not allowed, use POST"}, status=405
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )


@api_login_required
@validateToken
@csrf_exempt
def updateItem(request, item_slug):
    """
    Update an item by slug.

    Args:
        request: The request object
        item_slug: The slug of the item to update

    Returns:
        JsonResponse: The updated item

    Raises:
        Item.DoesNotExist: If item with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        if not request.method in ['PUT', 'PATCH']:
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405
            )

        item = Item.objects.get(slug=item_slug)

        data = json.loads(request.body)

        if isinstance(data, dict):
            for field in data:
                if field == 'slug':
                    continue
                elif field in item.__dict__.keys():
                    setattr(item, field, data[field])

            item.save()

            item_updated = json.loads(
                serialize('json', [item])
            )[0]

            populateRelationalFields(
                item_updated, ['category', 'sub_category'],
                [Category, SubCategory]
            )

            return JsonResponse(
                {
                    "message": f"Succesfully updated the item with slug, {item_slug}.",
                    "item": item_updated
                },
                status=200
            )

        else:
            return JsonResponse(
                {"error": "Invalid data format. Please provide a dictionary"}, status=400
            )

    except Item.DoesNotExist:
        return JsonResponse(
            {"error": f"Item with slug {item_slug} Doesn't Exists"}, status=404
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )


@api_login_required
@validateToken
@csrf_exempt
def deleteItem(request, item_slug):
    """
    Delete an item by slug.

    Args:
        request: The request object
        item_slug: The slug of the item to delete

    Returns:
        JsonResponse: The deleted item

    Raises:
        Item.DoesNotExist: If item with slug doesn't exist
        Exception: If any exception occurs
    """
    try:
        if not request.method == 'DELETE':
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use DELETE"}, status=405
            )

        Item.objects.get(slug=item_slug).delete()

        return JsonResponse(
            {"message": f"The item with slug {item_slug} has been deleted succesfully"}, status=204
        )

    except Item.DoesNotExist:
        return JsonResponse(
            {"error": f"Item with slug {item_slug} Doesn't Exists"}, status=404
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)}, status=500
        )
