from django.urls import path
from . import views

urlpatterns = [
    # Items Enpoints.
    path('items/', views.list_items, name='list_items'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/retrieve/<int:id>/', views.retrieve_item, name='retrieve_item'),
    path('items/update/<int:id>/', views.update_item, name='update_item'),
    path('items/delete/<int:id>/', views.delete_item, name='delete_item'),

    # Search Endpoints
    path(
        'items/category/<str:category>/',
        views.list_items_by_category,
        name='list_items_by_category'
    ),
    path(
        'items/sub_category/<str:sub_category>/',
        views.list_items_by_sub_category,
        name='list_items_by_sub_category'
    ),
    path(
        'items/price/<int:price>/',
        views.list_items_by_price,
        name='list_items_by_price'
    ),
    path(
        'items/quantity/<int:qty>/',
        views.list_items_by_quantity,
        name='list_items_by_quantity'
    ),
    path(
        'items/name/<str:name>/',
        views.retrieve_item_by_name,
        name='retrieve_item_by_name'
    ),
    path(
        'items/sku/<str:sku>/',
        views.retrieve_item_by_sku,
        name='retrieve_item_by_sku'
    ),

    # Category Endpoints
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/retrieve/<int:id>/',
         views.retrieve_category, name='retrieve_category'),

    # Stock Endpoints
    path('stocks/', views.list_stocks, name='list_stocks'),
    path('stocks/create/', views.create_stock, name='create_stock'),
    path('stocks/retrieve/<int:item>/',
         views.retrieve_stock, name='retrieve_stock'),
    path('stocks/update/<int:item>/', views.update_stock, name='update_stock'),
    path('stocks/delete/<int:item>/', views.delete_stock, name='delete_stock'),
]
