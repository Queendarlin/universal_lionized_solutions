from django.urls import path
from . import views

urlpatterns = [
    path('property_list/', views.property_list, name='property_list'),
    path('<uuid:pk>/', views.property_detail, name='property_detail'),
    path('add_property/', views.add_property, name='add_property'),
    path('property/<uuid:pk>/edit/', views.edit_property, name='edit_property'),
    path('property/<uuid:pk>/delete/', views.delete_property, name='delete_property'),
]
