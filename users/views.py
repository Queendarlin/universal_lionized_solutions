from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import User, UserRole, Referral
from .forms import UserRegistrationForm, LoginForm
from properties.models import Property
from .forms import ProfileUpdateForm


def home(request):
    if request.user.is_authenticated:
        if request.user.role == UserRole.AGENT:
            return redirect('agent_dashboard')
        elif request.user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            return redirect('admin_dashboard')
    return render(request, 'home.html')


def register_page(request):

    referral_code = request.GET.get('referral_code')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            # Generate a referral code for the new user
            user.generate_referral_code()
            
            # Set default role as REGULAR
            user.role = UserRole.REGULAR

            # Check if the user registered with a referral code
            if referral_code:
                try:
                    # Find the referrer by referral code
                    referrer = User.objects.get(referral_code=referral_code)
                    
                    # If the referrer is ADMIN, AGENT, or SUPER_ADMIN, assign the new user as AGENT
                    if referrer.role in [UserRole.ADMIN, UserRole.AGENT, UserRole.SUPER_ADMIN]:
                        user.role = UserRole.AGENT  # Assign role as AGENT

                    user.save()  # Save the user with the assigned role and referral code

                    # Create a Referral record to track this referral
                    Referral.objects.create(referrer=referrer, referred_agent=user)

                except User.DoesNotExist:
                    messages.warning(request, "Invalid referral code.")
                    user.save()  # Save the user with default role if referrer not found
            else:
                user.save()  # Save the user with default role if no referral code

            # Redirect to login page with success message
            messages.success(request, 'Registration successful! Please log in to continue.')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_page(request):
    # Redirect to home if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.')
                    
                    # Redirect based on user role
                    if user.role == UserRole.ADMIN or user.role == UserRole.SUPER_ADMIN:
                        return redirect('admin_dashboard')
                    elif user.role == UserRole.AGENT:
                        return redirect('agent_dashboard')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')  # Changed from login_page to login


@login_required
def agent_dashboard(request):
    # Ensure the user is an agent
    if request.user.role != UserRole.AGENT:
        messages.error(request, "Access denied. You are not an agent.")
        return redirect("home")

    # Fetch referrals and bonuses
    referrals = Referral.objects.filter(referrer=request.user)
    bonuses = request.user.bonuses.all()
    
    # Fetch all properties
    properties = Property.objects.all()
    
    context = {
        "referrals": referrals,
        "bonuses": bonuses,
        "properties": properties,
        'active_properties_count': properties.count(),
        'total_property_value': properties.aggregate(total=Sum('price'))['total'] or 0,
        'recent_updates_count': properties.filter(updated_at__gte=timezone.now() - timedelta(days=7)).count(),
        "referral_link": f"{request.build_absolute_uri(reverse('register'))}?referral_code={request.user.referral_code}",
    }
    return render(request, "agent_dashboard.html", context)


@login_required
def profile_update(request):
    user = request.user  # Current logged-in user
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Handle password change if provided
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)  # Hash and set the new password

            form.save()  # Save other fields

            # Re-authenticate the user if password was changed
            if new_password:
                login(request, user)

            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile_update')  # Redirect to a profile or dashboard page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'profile_update.html', {'form': form})

@login_required
def admin_dashboard(request):
    # Ensure the user is an admin or superadmin
    if request.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return redirect('home')

    users = Paginator(User.objects.all(), 10).get_page(request.GET.get('page', 1))  # List all users and paginate
    
    # Fetch all agents
    agents = User.objects.filter(role=UserRole.AGENT)
    
    # Fetch referrals and bonuses
    referrals = Referral.objects.filter(referrer=request.user)
    bonuses = request.user.bonuses.all()
    
    # Fetch all properties
    properties = Property.objects.all()

    context = {
        'users': users,
        'agents': agents,
        'referrals': referrals,
        'bonuses': bonuses,
        'properties': properties,
        'active_properties_count': properties.count(),
        'total_property_value': properties.aggregate(total=Sum('price'))['total'] or 0,
        'recent_updates_count': properties.filter(updated_at__gte=timezone.now() - timedelta(days=7)).count(),
        'referral_link': f"{request.build_absolute_uri(reverse('register'))}?referral_code={request.user.referral_code}",
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
def promote_to_agent(request, user_id):
    if request.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        messages.error(request, "You do not have permission to promote users.")
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)
    if user.role == UserRole.REGULAR:
        user.role = UserRole.AGENT
        user.save()
        messages.success(request, f"{user.get_full_name()} has been promoted to Agent.")
    else:
        messages.error(request, "Invalid action.")
    return redirect('admin_dashboard')


@login_required
def promote_to_admin(request, user_id):
    if request.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        messages.error(request, "You do not have permission to promote users.")
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)
    if user.role in [UserRole.REGULAR, UserRole.AGENT]:
        user.role = UserRole.ADMIN
        user.save()
        messages.success(request, f"{user.get_full_name()} has been promoted to Admin.")
    else:
        messages.error(request, "Invalid action.")
    return redirect('admin_dashboard')


@login_required
def demote_to_regular(request, user_id):
    if request.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        messages.error(request, "You do not have permission to demote users.")
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)
    if user.role == UserRole.AGENT:
        user.role = UserRole.REGULAR
        user.save()
        messages.success(request, f"{user.get_full_name()} has been demoted to Regular User.")
    else:
        messages.error(request, "Invalid action.")
    return redirect('admin_dashboard')


@login_required
def demote_to_agent(request, user_id):
    if request.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        messages.error(request, "You do not have permission to demote users.")
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)
    if user.role == UserRole.ADMIN:
        user.role = UserRole.AGENT
        user.save()
        messages.success(request, f"{user.get_full_name()} has been demoted to Agent.")
    else:
        messages.error(request, "Invalid action.")
    return redirect('admin_dashboard')


@login_required
def delete_user(request, user_id):
    if request.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        messages.error(request, "You do not have permission to delete users.")
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, "Super Admin cannot be deleted.")
    else:
        user.delete()
        messages.success(request, f"{user.get_full_name()} has been deleted.")
    return redirect('admin_dashboard')