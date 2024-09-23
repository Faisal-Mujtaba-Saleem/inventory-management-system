import os
import django
import json
import logging
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'inventory_management_system.settings')
django.setup()  # Initialize Django settings and application registry

# Import the Item model from the inventory app
from inventory.models import Item, Stock, Category

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# upload_data_to_db
def upload_data_to_db(name, sku, description, price, qty_in_stock, category, sub_category):
    # Generate a slug for item & stock
    item_stock_slug = slugify(sku)

    # Check if category exists in the database
    if not Category.objects.filter(name=category).exists():
        # Create a new Category instance with the provided data if it doesn't exist
        category = Category(name=category, slug=slugify(category))
        category.save()  # Save the new category to the database

    else:
        # Get the existing Category instance
        category = Category.objects.get(name=category)

    # Check if item exists in the database
    if Item.objects.filter(sku=sku).exists():
        # Get the existing Item instance
        item = Item.objects.get(sku=sku)

        # Update the existing item with the provided data
        item.name = name
        item.description = description
        item.sku = sku
        item.slug = item_stock_slug
        item.price = price
        item.category = category
        item.sub_category = sub_category

        item.save()  # Save the updated item to the database

        # Get the existing Stock instance
        stock = Stock.objects.get(item=item)

        # Update the existing stock with the provided data
        stock.item = item
        stock.name = item.name
        stock.sku = item.sku
        stock.slug = item_stock_slug
        stock.qty_in_stock = qty_in_stock

        stock.save()  # Save the updated stock to the database

        logger.info(
            f'Item {item.name} of category {
                category.name} updated successfully with stock of {stock.qty_in_stock}!'
        )
    else:
        # Create a new Item instance with the provided data
        item = Item(
            name=name,
            description=description,
            sku=sku,
            slug=item_stock_slug,
            price=price,
            category=category,
            sub_category=sub_category,
        )
        item.save()  # Save the new item to the database

        # Create a new Stock instance of the created item with the provided data
        stock = Stock(
            item=item,
            name=item.name,
            sku=item.sku,
            slug=item_stock_slug,
            qty_in_stock=qty_in_stock
        )
        stock.save()  # Save the new stock to the database

        # Inform the user that the item was uploaded successfully with stock
        logger.info(
            f'Item {item.name} of category {
                category.name
            } uploaded successfully with stock of {stock.qty_in_stock}!'
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

                # Process each item in the 'items' list
                for item_to_upload in item_category.get('items', []):
                    logger.info('Processing item')

                    # Skip items that do not have a SKU
                    if 'sku' not in item_to_upload:
                        logger.warning(f'Missing SKU in item: {
                                       item_to_upload}')
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
