from django.urls import path
from inventory.views import item_views, stock_views, category_views, subcategory_views, supplier_views, supply_views, item_filter_views, stock_filter_views, supply_filter_views

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
    ),

    # Supplier Endpoints

    path(
        'supplier/',
        view=supplier_views.listSupplier,
        name='list-items'  # List all items
    ),
    path(
        'supplier/create/<str:item_slug>/',
        view=supplier_views.createSupplier,
        name='create-supplier'  # Create a new supplier
    ),
    path(
        'supplier/retrieve/<int:pk>/',
        view=supplier_views.retrieveSupplierById,
        name='retrieve-item'  # Retrieve a supplier by id
    ),
    path(
        'supplier/retrieve/email/<str:email>/',
        view=supplier_views.retrieveSupplierByEmail,
        name='retrieve-item'  # Retrieve a supplier by email
    ),
    path(
        'supplier/retrieve/phone/<str:phone>/',
        view=supplier_views.retrieveSupplierByPhone,
        name='retrieve-item'  # Retrieve a supplier by phone
    ),
    path(
        'supplier/update/<int:pk>/',
        view=supplier_views.updateSupplierById,
        name='update-supplier'  # Update a supplier by id
    ),
    path(
        'supplier/update/email/<str:email>/',
        view=supplier_views.updateSupplierByEmail,
        name='update-supplier-by-email'  # Update a supplier by email
    ),
    path(
        'supplier/update/phone/<str:phone>/',
        view=supplier_views.updateSupplierByPhone,
        name='update-supplier-by-phone'  # Update a supplier by phone
    ),
    path(
        'supplier/delete/<int:pk>/',
        view=supplier_views.deleteSupplierById,
        name='delete-supplier'  # Delete a supplier by id
    ),
    path(
        'supplier/delete/email/<str:email>/',
        view=supplier_views.deleteSupplierByEmail,
        name='delete-supplier-by-email'  # Delete a supplier by email
    ),
    path(
        'supplier/delete/phone/<str:phone>/',
        view=supplier_views.deleteSupplierByPhone,
        name='delete-supplier-by-phone'  # Delete a supplier by phone
    ),

    # Supply Endpoints

    path(
        'supply/',
        view=supply_views.listSupply,
        name='list-supplies'  # List all supplies
    ),
    path(
        'supply/retrieve/<int:pk>/',
        view=supply_views.retrieveSupply,
        name='retrieve-supply'  # Retrieve supply
    ),
    path(
        'supply/update/<int:pk>/',
        view=supply_views.updateSupply,
        name='update-supply'  # Update supply
    ),
    path(
        'supply/delete/<int:pk>/',
        view=supply_views.deleteSupply,
        name='delete-supply'  # Delete supply
    ),

    
    # Filter Endpoints

    # Item Filters

    path(
        'items/category/<str:category_slug>/',
        view=item_filter_views.listItemsByCategory,
        name='list-items-by-category'  # List items by category
    ),
    path(
        'items/sub-category/<str:sub_category_slug>/',
        view=item_filter_views.listItemsBySubCategory,
        name='list-items-by-subcategory'  # List items by sub-category
    ),
    path(
        'items/min-price/<int:min_price>/',
        view=item_filter_views.listItemsByMinPrice,
        name='list-items-by-min-price'  # List items by min price
    ),
    path(
        'items/max-price/<int:max_price>/',
        view=item_filter_views.listItemsByMaxPrice,
        name='list-items-by-max-price'  # List items by max price
    ),
    path(
        'items/price-min-max/<int:min_price>/<int:max_price>/',
        view=item_filter_views.listItemsFromMinToMaxPrice,
        name='list-items-between-min-max-price'  # List items within a price range
    ),
    path(
        'items/price-max-min/<int:max_price>/<int:min_price>/',
        view=item_filter_views.listItemsFromMaxToMinPrice,
        name='list-items-between-max-min-price'  # List items within a price range
    ),

    # Stock Filters

    path(
        'stocks/min-qty/<int:min_qty>/',
        view=stock_filter_views.listStocksByMinQty,
        name='list-stocks-by-min-quantity'  # List stocks by minimum quantity
    ),
    path(
        'stocks/max-qty/<int:max_qty>/',
        view=stock_filter_views.listStocksByMaxQty,
        name='list-stocks-by-max-quantity'  # List stocks by maximum quantity
    ),
    path(
        'stocks/qty-range-min-max/<int:min_qty>/<int:max_qty>/',
        view=stock_filter_views.listStocksFromMinToMaxQty,
        name='list-items-between-qty-range'  # List items within a quantity range
    ),
    path(
        'stocks/qty-range-max-min/<int:max_qty>/<int:min_qty>/',
        view=stock_filter_views.listStocksFromMaxToMinQty,
        name='list-items-between-qty-range'  # List items within a quantity range
    ),

    # Supply Filters

    path(
        'supply/item/<slug:item_slug>/',
        view=supply_filter_views.listSupplyByItem, 
        name='list-supplys-by-item'
    ),
    path(
        "supply/supplier/<int:supplier_id>/", 
        view=supply_filter_views.listSupplyBySupplierId, 
        name="list-supplys-by-supplier-id"
    ),
    path(
        "supply/supplier-email/<str:supplier_email>/", 
        view=supply_filter_views.listSupplyBySupplierEmail, 
        name="list-supplys-by-supplier-email"
    ),
    path(
        "supply/supplier-phone/<str:supplier_phone>/", 
        view=supply_filter_views.listSupplyBySupplierPhone, 
        name="list-supplys-by-supplier-phone"
    ),
    path(
        'supply/min-qty/<int:min_qty>/',
        view=supply_filter_views.listSupplyByMinQty,
        name='list-supplies-by-min-quantity'  # List supplies by minimum quantity
    ),
    path(
        'supply/max-qty/<int:max_qty>/',
        view=supply_filter_views.listSupplyByMaxQty,
        name='list-supplies-by-max-quantity'  # List supplies by maximum quantity
    ),
    path(
        'supply/qty-range-min-max/<int:min_qty>/<int:max_qty>/',
        view=supply_filter_views.listSupplyFromMinToMaxQty,
        name='list-items-between-qty-range'  # List items within a quantity range
    ),
    path(
        'supply/qty-range-max-min/<int:max_qty>/<int:min_qty>/',
        view=supply_filter_views.listSupplyFromMaxToMinQty,
        name='list-items-between-qty-range'  # List items within a quantity range
    ),

    # Search Endpoint

    path(
        'items/search/',
        view=item_filter_views.searchItems,
        name='search-items'  # Search items
    )
]
