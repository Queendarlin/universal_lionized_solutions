"""
URL configuration for universal_lionized_solutions project.

The `urlpatterns` list routes URLs to views. 
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('properties.urls')),
    # path('bonuses/', include('bonuses.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
