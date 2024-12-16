from django import forms 
from .models import User, UserRole
from django.contrib.auth.forms import AuthenticationForm
import re


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirm']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")
        if not re.search(r'[a-z]', password):
            self.add_error('password', "Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            self.add_error('password', "Password must contain at least one number.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    

class RoleUpgradeForm(forms.Form):
    target_role = forms.ChoiceField(
        choices=[
            (UserRole.REGULAR, "Regular User"),
            (UserRole.AGENT, "Agent"),
            (UserRole.ADMIN, "Admin"),
            (UserRole.SUPER_ADMIN, "Super Admin"),
        ],
        label="Select Target Role",
        required=True,
    )


class ProfileUpdateForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password',
            'autocomplete': 'off'
        }),
        required=True,
        help_text="Enter your current password to confirm changes."
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password (optional)'
        }),
        required=False
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        # Validate current password
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("The current password is incorrect.")

        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        # Skip validation if no new password is provided
        if not new_password:
            return new_password

        # Password length validation
        if len(new_password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        # At least one lowercase letter
        if not re.search(r'[a-z]', new_password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")

        # At least one number
        if not re.search(r'[0-9]', new_password):
            raise forms.ValidationError("Password must contain at least one number.")
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        # Check if new passwords match
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError("The new passwords do not match.")

        return cleaned_data
