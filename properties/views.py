import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Property, PropertyImage, PropertyVideo
from .forms import PropertyForm, PropertyImageForm, PropertyVideoForm
from users.models import UserRole


# Check if user is an admin
def can_manage_properties(user):
    """Check if user is active and has permission to manage properties"""
    return user.is_active and user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]


@login_required
def add_property(request):
    if not can_manage_properties(request.user):
        raise PermissionDenied("You don't have permission to add properties.")
    
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        image_form = PropertyImageForm(request.POST, request.FILES)
        video_form = PropertyVideoForm(request.POST, request.FILES)

        # Validate all forms before saving
        if property_form.is_valid():
            try:
                # Save property first
                property_instance = property_form.save()
                
                # Handle images with dynamic file validation
                images = request.FILES.getlist('image')
                for image in images:
                    # Validate image format
                    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
                    ext = os.path.splitext(image.name)[1].lower()
                    if ext not in valid_extensions:
                        messages.error(request, f'Invalid image format for {image.name}. Accepted formats are: {", ".join(valid_extensions)}')
                        property_instance.delete()  # Remove the property if invalid files
                        return render(request, 'add_property.html', {
                            'property_form': property_form,
                            'image_form': image_form,
                            'video_form': video_form
                        })
                    
                    # Validate file size (5MB max)
                    if image.size > 5 * 1024 * 1024:
                        messages.error(request, f'Image {image.name} exceeds 5MB limit')
                        property_instance.delete()
                        return render(request, 'add_property.html', {
                            'property_form': property_form,
                            'image_form': image_form,
                            'video_form': video_form
                        })
                    
                    PropertyImage.objects.create(property=property_instance, image=image)
                
                # Handle videos with dynamic file validation
                videos = request.FILES.getlist('video')
                for video in videos:
                    # Validate video format
                    valid_extensions = ['.mp4', '.mov']
                    ext = os.path.splitext(video.name)[1].lower()
                    if ext not in valid_extensions:
                        messages.error(request, f'Invalid video format for {video.name}. Accepted formats are: {", ".join(valid_extensions)}')
                        property_instance.delete()
                        return render(request, 'add_property.html', {
                            'property_form': property_form,
                            'image_form': image_form,
                            'video_form': video_form
                        })
                    
                    # Validate file size (50MB max)
                    if video.size > 50 * 1024 * 1024:
                        messages.error(request, f'Video {video.name} exceeds 50MB limit')
                        property_instance.delete()
                        return render(request, 'add_property.html', {
                            'property_form': property_form,
                            'image_form': image_form,
                            'video_form': video_form
                        })
                    
                    PropertyVideo.objects.create(property=property_instance, video=video)
                
                messages.success(request, 'Property added successfully!')
                return redirect('property_detail', pk=property_instance.pk)
            
            except Exception as e:
                # Log the error and show a user-friendly message
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # If property form is invalid, show error messages
            messages.error(request, 'Please correct the errors in the form.')
    else:
        # Initialize blank forms for GET request
        property_form = PropertyForm()
        image_form = PropertyImageForm()
        video_form = PropertyVideoForm()
    
    return render(request, 'add_property.html', {
        'property_form': property_form,
        'image_form': image_form,
        'video_form': video_form
    })

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})

def property_detail(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    images = PropertyImage.objects.filter(property=property_instance)
    videos = PropertyVideo.objects.filter(property=property_instance)
    return render(request, 'property_detail.html', {
        'property': property_instance,
        'images': images,
        'videos': videos
    })
    
@login_required
def edit_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)

    if not can_manage_properties(request.user):
        raise PermissionDenied("You don't have permission to edit this property.")

    if request.method == 'POST':
        property_form = PropertyForm(request.POST, instance=property_instance)
        if property_form.is_valid():
            property_form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', pk=property_instance.pk)
    else:
        property_form = PropertyForm(instance=property_instance)

    return render(request, 'edit_property.html', {'property_form': property_form})

@login_required
def delete_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)

    if not can_manage_properties(request.user):
        raise PermissionDenied("You don't have permission to delete this property.")

    property_instance.delete()
    messages.success(request, 'Property deleted successfully!')
    return redirect('admin_dashboard')
