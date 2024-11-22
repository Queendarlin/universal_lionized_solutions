import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Defines custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.SUPER_ADMIN)  # Explicitly set role

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


# Enumerations for User roles
class UserRole(models.TextChoices):
    REGULAR = 'REGULAR', 'Regular User'
    AGENT = 'AGENT', 'Agent'
    ADMIN = 'ADMIN', 'Admin'
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'


# User model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    referral_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.REGULAR)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Define that 'username' is used for login instead of 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Email is required, but not for login
    
    # Attach the custom manager
    objects = CustomUserManager()    

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    def generate_referral_code(self):
        if not self.referral_code:
            self.referral_code = f"{self.username}-{uuid.uuid4().hex[:6]}"
            self.save(update_fields=['referral_code'])

    def set_role(self, new_role):
        """Allows only admins or superusers to change the user's role."""
        if not self.can_change_roles():
            raise PermissionError("Only admins can change roles.")
        if new_role not in [role.value for role in UserRole]:
            raise ValueError("Invalid role assignment.")
        
        self.role = new_role
        self.save()
    
    def can_change_roles(self):
        """Checks if the user has permission to change roles."""
        return self.is_superuser or self.is_staff

    def upgrade_to_super_admin(self):
        self.role = UserRole.SUPER_ADMIN
        self.generate_referral_code()  # Optional: Generate a referral code for Super Admin
        self.save()

    def upgrade_to_admin(self):
        self.role = UserRole.ADMIN
        self.generate_referral_code()
        self.save()

    def upgrade_to_agent(self):
        self.role = UserRole.AGENT
        self.generate_referral_code()
        self.save()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['first_name']

# Referral model
class Referral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referred_agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_agents')
    referred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral from {self.referrer} to {self.referred_agent}"

    class Meta:
        unique_together = ('referrer', 'referred_agent')  # Ensures a user cannot refer the same user more than once
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"

# Signal handler for automatic referral code generation
@receiver(post_save, sender=User)
def create_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.generate_referral_code()
