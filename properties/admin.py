from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo

# Define inline classes for related images and videos
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 5

class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 5

# Define PropertyAdmin with the inlines
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, PropertyVideoInline]
    
    # Define which fields to display on the admin list view
    list_display = ('title', 'location', 'status', 'date_closed', 'price')
    
    # Add filters for status and property type
    list_filter = ('status', 'type')
    
    # Add a search bar to search by title or location
    search_fields = ('title', 'location')
    
    # Specify which fields to include in the form
    fields = ('title', 'location', 'description', 'type', 'price', 'square_footage', 'status', 'date_closed')
    
    # Specify that created_at and updated_at should be read-only fields
    readonly_fields = ('created_at', 'updated_at')
