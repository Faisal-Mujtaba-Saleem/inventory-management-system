from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from inventory.models import Item, Supply, Supplier, Stock
import json


# Supplier Views

def listSupplier(request):
    try:
        suppliers = Supplier.objects.all()
        supplier_list = json.loads(serialize('json', suppliers))

        return JsonResponse(
            {
                "message": "Successfully retrieved all suppliers",
                "supplier_count": len(supplier_list),
                "suppliers": supplier_list
            },
            status=200
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def retrieveSupplier(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
        supplier = json.loads(
            serialize(
                'json', supplier
            )
        )[0]

        return JsonResponse(
            {
                "message": f"Successfully retrieved the supplier of pk {pk}",
                "supplier": supplier
            },
            status=200
        )

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"Supplier with id {pk} doesn't exist"}, status=404)

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
                "message": "Successfully created the supply & supplier.",
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
def updateSupplier(request, pk):
    try:
        if request.method not in ['PUT', 'PATCH']:
            return JsonResponse({"error": f"Request method {request.method} not allowed, use PUT or PATCH"}, status=405)

        supplier = Supplier.objects.get(pk=pk)

        data = json.loads(request.body)

        print(supplier.__dict__)

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
                    "message": f"Successfully updated the supplier of pk {pk}",
                    "supplier": updated_supplier
                },
                status=200
            )

        return JsonResponse({"error": "Invalid data format. Please provide a dictionary"}, status=400)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"Supplier of pk {pk} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def deleteSupplier(request, pk):
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

        return JsonResponse({"message": f"Supplier of pk {pk} has been deleted successfully"}, status=204)

    except Supplier.DoesNotExist:
        return JsonResponse({"error": f"Supplier of pk {pk} doesn't exist"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
