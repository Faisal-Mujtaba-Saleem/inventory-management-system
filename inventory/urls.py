from django.urls import path
from . import views

urlpatterns = [

    # Items Enpoints.

    path('items/', views.list_items, name='list_items'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/retrieve/<int:id>/', views.retrieve_item, name='retrieve_item'),
    path('items/update/<int:id>/', views.update_item, name='update_item'),
    path('items/delete/<int:id>/', views.delete_item, name='delete_item'),


    # Filter Endpoints

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
        'items/price/<int:maxprice>/',
        views.list_items_by_max_price,
        name='list_items_by_price'
    ),
    path(
        'items/quantity/<int:max_qty>/',
        views.list_items_by_max_quantity,
        name='list_items_by_quantity'
    ),


    # Search Endpoint

    path('items/search/',
         views.search_items, name='search_items'),


    # Category Endpoints

    path('categories/', views.list_categories, name='list_categories'),
    path('categories/retrieve/<int:id>/',
         views.retrieve_category, name='retrieve_category'),


    # Stock Endpoints

    path('stocks/', views.list_stocks, name='list_stocks'),
    path('stocks/retrieve/<int:item>/',
         views.retrieve_stock, name='retrieve_stock'),
    path('stocks/update/<int:item>/', views.update_stock, name='update_stock'),
]
