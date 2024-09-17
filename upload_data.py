import os
import django
import json
import logging

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'inventory_management_system.settings')
django.setup()  # Initialize Django settings and application registry

# Import the Item model from the inventory app
from inventory.models import Item, Stock, Category

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_data_to_db(name, sku, description, price, qty_in_stock, category, sub_category):
    # Check if item exists in the database
    if Item.objects.filter(sku=sku).exists():
        logger.info(f'Item with SKU {sku} already exists')
        return

    # Create a new Item instance with the provided data
    item = Item(
        name=name,
        description=description,
        sku=sku,
        price=price,
        category=category,
        sub_category=sub_category,
    )
    item.save()  # Save the new item to the database
    # logger.info(f'Item {name} uploaded successfully!')

    stock = Stock(item=item, name=name, sku=sku, qty_in_stock=qty_in_stock)
    stock.save()

    if Category.objects.filter(name=category).exists():
        logger.info(f'Category {category} already exists')
        return

    category = Category(name=category, description=description)
    category.save()

    logger.info(
        f'Item {item.name} of category {
            category.name
        } uploaded successfully with stock of {stock.qty_in_stock}!'
    )


if __name__ == "__main__":
    try:
        # Open and read the JSON file containing item data
        with open('db_items.json') as json_file:
            items_categories = json.load(json_file).get('items_categories', [])

            # Iterate through each item in the JSON data
            for category in items_categories:
                category = category.get('category', '')
                sub_category = category.get('sub_category', '')

                # Process each item in the 'items' list
                for item_to_upload in category.get('items', []):
                    logger.info('Processing item')

                    # Skip items that do not have a SKU
                    if 'sku' not in item_to_upload:
                        logger.warning(f'Missing SKU in item: {item_to_upload}')
                        continue

                    # Upload the item to the database
                    upload_data_to_db(
                        category=category, sub_category=sub_category, **item_to_upload
                    )

    except Exception as e:
        # Print any exceptions that occur during processing
        logger.error(f'Error: {e}')

    finally:
        logger.info('Done!')  # Indicate that processing is complete
