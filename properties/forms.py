from django import forms
from .models import Property, PropertyImage, PropertyVideo, PropertyType, PropertyStatus

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'location', 'description', 'type', 'price', 'square_footage', 'status', 'date_closed']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter property title', 
                'required': 'required',
                'class': 'form-input'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'City, State, Country', 
                'required': 'required',
                'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Provide detailed property description (amenities, features, etc.)', 
                'required': 'required',
                'class': 'form-textarea',
                'rows': 4
            }),
            'type': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter property price', 
                'required': 'required',
                'class': 'form-input',
                'min': 0
            }),
            'square_footage': forms.NumberInput(attrs={
                'placeholder': 'Total livable area in sq ft',
                'class': 'form-input',
                'min': 0
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'date_closed': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            })
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive number")
        return price

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*',
            })
        }

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = ['video']
        widgets = {
            'video': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'video/*',
            })
        }