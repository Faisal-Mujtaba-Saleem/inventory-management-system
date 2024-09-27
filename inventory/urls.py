from django.urls import path
from inventory.views import item_views, stock_views, category_views, subcategory_views, search_filter_views

urlpatterns = [
    # Items Enpoints.

    path(
        'items/',
        view=item_views.listItems,
        name='list-items'  # Listing all items
    ),

    path(
        'items/create/',
        view=item_views.createItem,
        name='create-item'  # Creating a new item
    ),

    path(
        'items/retrieve/<str:item_slug>/',
        view=item_views.retrieveItem,
        name='retrieve-item'  # Retrieve an item by slug
    ),

    path(
        'items/update/<str:item_slug>/',
        view=item_views.updateItem,
        name='update-item'  # Update an item by slug
    ),

    path(
        'items/delete/<str:item_slug>/',
        view=item_views.deleteItem,
        name='delete-item'  # Delete an item by slug
    ),

    # Filter Endpoints

    path(
        'items/category/<str:category_slug>/',
        view=search_filter_views.listItemsByCategory,
        name='list-items-by-category'  # List items by category
    ),

    path(
        'items/sub-category/<str:sub_category_slug>/',
        view=search_filter_views.listItemsBySubCategory,
        name='list-items-by-subcategory'  # List items by sub-category
    ),

    path(
        'items/min-price/<int:min_price>/',
        view=search_filter_views.listItemsByMinPrice,
        name='list-items-by-min-price'  # List items by min price
    ),

    path(
        'items/max-price/<int:max_price>/',
        view=search_filter_views.listItemsByMaxPrice,
        name='list-items-by-max-price'  # List items by max price
    ),

    path(
        'items/min-qty/<int:min_qty>/',
        view=search_filter_views.listItemsByMinQty,
        name='list-items-by-min-quantity'  # List items by minimum quantity
    ),

    path(
        'items/max-qty/<int:max_qty>/',
        view=search_filter_views.listItemsByMinQty,
        name='list-items-by-max-quantity'  # List items by maximum quantity
    ),

    path(
        'items/price-min-max/<int:min_price>/<int:max_price>/',
        view=search_filter_views.listItemsFromMinToMaxPrice,
        name='list-items-between-min-max-price'  # List items within a price range
    ),

    path(
        'items/price-max-min/<int:max_price>/<int:min_price>/',
        view=search_filter_views.listItemsFromMaxToMinPrice,
        name='list-items-between-max-min-price'  # List items within a price range
    ),

    path(
        'stocks/qty-range-min-max/<int:min_qty>/<int:max_qty>/',
        view=search_filter_views.listStocksFromMinToMaxQty,
        name='list-items-between-qty-range'  # List items within a quantity range
    ),

    path(
        'stocks/qty-range-max-min/<int:max_qty>/<int:min_qty>/',
        view=search_filter_views.listStocksFromMaxToMinQty,
        name='list-items-between-qty-range'  # List items within a quantity range
    ),

    # Search Endpoint

    path(
        'items/search/',
        view=search_filter_views.searchItems,
        name='search-items'  # Search items
    ),

    # Category Endpoints

    path(
        'categories/',
        view=category_views.listCategories,
        name='list-categories'  # List all categories
    ),

    path(
        'categories/retrieve/<str:category_slug>/',
        view=category_views.retrieveCategory,
        name='retrieve-category'  # Retrieve category by slug
    ),

    path(
        "categories/update/<str:category_slug>/",
        view=category_views.updateCategory,
        name="update-category"  # Update category by slug
    ),

    path(
        "categories/delete/<str:category_slug>/",
        view=category_views.deleteCategory,
        name="delete-category"  # Delete category by slug
    ),

    # Sub-Category Endpoints

    path(
        'subcategories/',
        view=subcategory_views.listSubCategories,
        name='list-subcategories'  # List all sub-categories
    ),

    path(
        'subcategories/retrieve/<str:sub_category_slug>/',
        view=subcategory_views.retrieveSubCategory,
        name='retrieve-subcategory'  # Retrieve sub-category by slug
    ),

    path(
        "subcategories/update/<str:sub_category_slug>/",
        view=subcategory_views.updateSubCategory,
        name="update-subcategory"  # Update sub-category by slug
    ),

    path(
        "subcategories/delete/<str:sub_category_slug>/",
        view=subcategory_views.deleteSubCategory,
        name="delete-subcategory"  # Delete sub-category by slug
    ),

    # Stock Endpoints

    path(
        'stocks/',
        view=stock_views.listStocks,
        name='list-stocks'  # List all stocks
    ),

    path(
        'stocks/retrieve/<str:item_slug>/',
        view=stock_views.retrieveStock,
        name='retrieve-stock'  # Retrieve stock by item slug
    ),

    path(
        'stocks/update/<str:item_slug>/',
        view=stock_views.updateStock,
        name='update-stock'  # Update stock by item slug
    )
]
