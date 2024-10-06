import os
import django
import json
import logging


# Set up Django environment
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'inventory_management_system.settings'
)
django.setup()  # Initialize Django settings and application registry

# Import the Item model from the inventory app
from inventory.models import Item, Stock, Category, SubCategory, Supplier, Supply

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# upload_data_to_db
def upload_data_to_db(name, sku, description, price, qty_in_stock, qty_supplied, category, sub_category, _supplier):
    # Check if category exists in the database
    category = Category.objects.get_or_create(name=category)[0]

    # Check if sub_category exists in the database
    sub_category = SubCategory.objects.get_or_create(
        name=sub_category, category=category)[0]

    item, is_item_created = Item.objects.get_or_create(
        sku=sku,
        defaults={
            "name": name,
            "sku": sku,
            "price": price,
            "description": description,
            "category": category,
            "sub_category": sub_category,
        }
    )

    # Check if item exists in the database
    if not is_item_created:
        item.name = name
        item.description = description
        item.sku = sku
        item.price = price
        item.category = category
        item.sub_category = sub_category
        item.save()  # Update the item in the database

    # Get the existing Stock instance
    stock, is_stock_created = Stock.objects.get_or_create(
        item=item,
        defaults={
            "qty_in_stock": qty_in_stock
        }
    )

    # Check if stock exists in the database
    if not is_stock_created:
        stock.qty_in_stock = qty_in_stock
        stock.save()  # Update the stock in the database


    # Get the existing Supply instance
    supplier, is_supplier_created = Supplier.objects.get_or_create(
        email=_supplier['email'],
        defaults=_supplier
    )

    # Check if supplier exists in the database
    if not is_supplier_created:
        for field in _supplier:
            if field in supplier.__dict__.keys():
                supplier.field = _supplier[field]
        
        supplier.save()  # Update the supplier in the database

    # Get the existing Supply instance
    supply, is_supply_created = Supply.objects.get_or_create(
        item=item,
        supplier=supplier,
        defaults={
            "item": item,
            "supplier": supplier,
            "qty_supplied": qty_supplied
        }
    )

    # Check if supply exists in the database
    if not is_supply_created:
        supply.qty_supplied = qty_supplied
        supply.save()  # Update the supply in the database
        
    logger.info(
        f' Successfully uploaded item: {name} of category: {category} and sub_category: {sub_category} with quantity in stock: {qty_in_stock} out of quantity supplied: {qty_supplied}'
    )


if __name__ == "__main__":
    try:
        # Open and read the JSON file containing item data
        with open('db_.json') as json_file:
            items_categories = json.load(json_file).get('items_categories', [])

            # Iterate through each item in the JSON data
            for item_category in items_categories:
                category = item_category.get('category', '')
                sub_category = item_category.get('sub_category', '')
                supplier = item_category.get('supplier', '')

                # Process each item in the 'items' list
                for item_to_upload in item_category.get('items', []):
                    logger.info(' Processing item')

                    # Skip items that do not have a SKU
                    if 'sku' not in item_to_upload:
                        logger.warning(f' Missing SKU in item: {
                                       item_to_upload}')
                        continue

                    # Upload the item to the database
                    upload_data_to_db(
                        category=category, sub_category=sub_category, _supplier=supplier, **item_to_upload
                    )

    except Exception as e:
        # Print any exceptions that occur during processing
        logger.error(f' Error: {e}')

    finally:
        logger.info(' Done!')  # Indicate that processing is complete
