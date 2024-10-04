from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.paginator import Paginator
from inventory.models import Item, Supply, Supplier, Stock
import json


# Supplier Views

def listSupplier(request):
    try:
        suppliers = Supplier.objects.all()

        page = request.GET.get('page', 0)
        page = int(page)

        pagesize = request.GET.get('pagesize', 0)
        pagesize = int(pagesize)

        if page <= 0 or pagesize <= 0:
            return JsonResponse(
                {
                    "error": "Invalid page or pagesize."
                },
                status=400
            )
        
        paginator = Paginator(suppliers, pagesize)
        page_object = paginator.get_page(page)

        supplier_list = json.loads(
            serialize(
                'json', page_object.object_list
            )
        )

        return JsonResponse(
            {
                "message": f"Successfully retrieved all suppliers",
                "page": page,
                "pagesize": pagesize,
                "total_pages": paginator.num_pages,
                "total_results": paginator.count,
                "categories": supplier_list
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveSupplierById(request, pk):
    """
    Retrieves a supplier by id.

    Args:
        request: The request object
        pk: The id of the supplier to retrieve

    Returns:
        JsonResponse: A JSON response containing the supplier object or error message
    """
    try:
        supplier = Supplier.objects.get(pk=pk)
        supplier = json.loads(
            serialize(
                'json', [supplier]
            )
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the supplier with id, {pk}",
                "supplier": supplier
            },
            status=200
        )


    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"Supplier with id {pk} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveSupplierByEmail(request, email):
    try:
        supplier = Supplier.objects.get(email=email)
        supplier = json.loads(
            serialize(
                'json', [supplier]
            )
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the supplier with email, {email}",
                "supplier": supplier
            },
            status=200
        )

    except Supplier.DoesNotExist:
        return JsonResponse(
            {"error": f"Supplier with email {email} doesn't exist"}, status=404
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveSupplierByPhone(request, phone):
    try:
        supplier = Supplier.objects.get(phone=phone)
        supplier = json.loads(
            serialize(
                'json', [supplier]
            )
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the supplier with phone {phone}",
                "supplier": supplier
            },
            status=200
        )

    except Supplier.DoesNotExist:
        return JsonResponse(
            {"error": f"Supplier with phone {phone} doesn't exist"}, status=404
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def createSupplier(request, item_slug):
    try:
        if request.method != 'POST':
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use POST"}, status=405
            )

        data = json.loads(request.body)

        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        qty_supplied = data.get('qty_supplied', '')

        # Retrieve the related item by slug

        item = Item.objects.get(slug=item_slug)

        # Check if a supplier with the same person name and item already exists

        supplier, is_supplier_created = Supplier.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "email": email,
                "phone": phone,
            }
        )

        if not is_supplier_created:
            return JsonResponse(
                {
                    "message": "Supplier already exists."
                },
                status=409
            )

        # Create supply record

        Supply.objects.create(
            item=item,
            supplier=supplier,
            qty_supplied=qty_supplied
        )

        return JsonResponse(
            {
                "message": "Successfully created the supplier.",
                "supplier": json.loads(
                    serialize('json', [supplier])
                )[0]
            },
            status=201
        )

    except Item.DoesNotExist:
        return JsonResponse({"error": "Item with the given slug doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateSupplierById(request, pk):
    try:
        if request.method not in ['PUT', 'PATCH']:
            return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)

        supplier = Supplier.objects.get(pk=pk)

        data = json.loads(request.body)

        if isinstance(data, dict):
            for field, value in data.items():
                if field in supplier.__dict__.keys():
                    setattr(supplier, field, value)

            supplier.save()

            updated_supplier = json.loads(
                serialize('json', [supplier])
            )[0]

            return JsonResponse(
                {
                    "message": f"Successfully updated the supplier with id, {pk}",
                    "supplier": updated_supplier
                },
                status=200
            )

        return JsonResponse({"error": "Invalid data format. Please provide a dictionary"}, status=400)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"supplier with id, {pk} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateSupplierByEmail(request, email):
    try:
        if request.method not in ['PUT', 'PATCH']:
            return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)

        supplier = Supplier.objects.get(email=email)

        data = json.loads(request.body)

        if isinstance(data, dict):
            for field, value in data.items():
                if field in supplier.__dict__.keys():
                    setattr(supplier, field, value)

            supplier.save()

            updated_supplier = json.loads(
                serialize('json', [supplier])
            )[0]

            return JsonResponse(
                {
                    "message": f"Successfully updated the supplier with id, {email}",
                    "supplier": updated_supplier
                },
                status=200
            )

        return JsonResponse({"error": "Invalid data format. Please provide a dictionary"}, status=400)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"supplier with id, {email} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def updateSupplierByPhone(request, phone):
    try:
        if request.method not in ['PUT', 'PATCH']:
            return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)

        supplier = Supplier.objects.get(phone=phone)

        data = json.loads(request.body)

        if isinstance(data, dict):
            for field, value in data.items():
                if field in supplier.__dict__.keys():
                    setattr(supplier, field, value)

            supplier.save()

            updated_supplier = json.loads(
                serialize('json', [supplier])
            )[0]

            return JsonResponse(
                {
                    "message": f"Successfully updated the supplier with id, {phone}",
                    "supplier": updated_supplier
                },
                status=200
            )

        return JsonResponse({"error": "Invalid data format. Please provide a dictionary"}, status=400)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"supplier with id, {phone} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def deleteSupplierById(request, pk):
    """
    Delete a supplier by slug.

    Args:
        request: The request object
        supplier_slug: The slug of the supplier to delete

    Returns:
        JsonResponse: A success message if deleted, or error message if not found
    """
    try:
        if request.method != 'DELETE':
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use DELETE"}, status=405
            )

        Supplier.objects.get(pk=pk).delete()

        return JsonResponse({"message": f"supplier with id, {pk} has been deleted successfully"}, status=204)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"supplier with id, {pk} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def deleteSupplierByEmail(request, email):
    """
    Delete a supplier by slug.

    Args:
        request: The request object
        supplier_slug: The slug of the supplier to delete

    Returns:
        JsonResponse: A success message if deleted, or error message if not found
    """
    try:
        if request.method != 'DELETE':
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use DELETE"}, status=405
            )

        Supplier.objects.get(email=email).delete()

        return JsonResponse({"message": f"supplier with id, {email} has been deleted successfully"}, status=204)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"supplier with id, {email} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def deleteSupplierByPhone(request, phone):
    """
    Delete a supplier by slug.

    Args:
        request: The request object
        supplier_slug: The slug of the supplier to delete

    Returns:
        JsonResponse: A success message if deleted, or error message if not found
    """
    try:
        if request.method != 'DELETE':
            return JsonResponse(
                {"error": f"Request method {request.method} not allowed, use DELETE"}, status=405
            )

        Supplier.objects.get(phone=phone).delete()

        return JsonResponse({"message": f"supplier with id, {phone} has been deleted successfully"}, status=204)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"supplier with id, {phone} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)