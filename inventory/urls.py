from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.list_items, name='list_items'),
    path('items/<int:id>/', views.retrieve_item, name='retrieve_item'),
    path('items/<int:id>/update/', views.update_item, name='update_item'),
    path('items/<int:id>/delete/', views.delete_item, name='delete_item'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/search/', views.search_items, name='search_items'),
    path('items/<int:id>/stock/', views.get_item_stock, name='get_item_stock'),
    path('items/<int:id>/stock/update/',
         views.update_item_stock, name='update_item_stock'),
    path('categories/', views.list_categories, name='list_categories'),
]
