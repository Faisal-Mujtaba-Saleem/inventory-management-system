from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register-user'),
    path('list/', views.listUsers, name='list-users'),
    path('retrieve/', views.retrieveUser, name='retrieve-user'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('update/', views.updateUser, name='update'),
    path('delete/', views.deleteUser, name='delete'),
    path("refresh-authkey/", views.refreshAuthKey, name="refresh-authkey"),
    ]
