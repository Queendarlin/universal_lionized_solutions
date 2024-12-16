from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import admin, messages
from .models import User, Referral, UserRole
from .forms import RoleUpgradeForm
import uuid


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'referral_code']
    actions = ['upgrade_user']  # Register the custom action
    list_filter = ['role']  # Add a filter for roles

    def get_urls(self):
        """
        Add custom URLs for admin actions.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                'upgrade-user/',
                self.admin_site.admin_view(self.process_upgrade_user),
                name='upgrade_user',
            ),
        ]
        return custom_urls + urls

    @admin.action(description="Upgrade selected users by role")
    def upgrade_user(self, request, queryset):
        """
        Redirect to a custom view for selecting the target role.
        """
        if queryset.count() == 0:
            self.message_user(request, "Please select at least one user.", messages.WARNING)
            return

        selected = queryset.values_list('id', flat=True)
        return HttpResponseRedirect(
            f"upgrade-user/?ids={','.join(map(str, selected))}"
        )

    def process_upgrade_user(self, request):
        """
        Custom view to handle the role upgrade action with a form.
        """
        user_ids = request.GET.get('ids')
        if not user_ids:
            self.message_user(request, "No users selected.", messages.WARNING)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

        user_ids = [uuid.UUID(id) for id in user_ids.split(',')]
        users = User.objects.filter(id__in=user_ids)

        if request.method == "POST":
            form = RoleUpgradeForm(request.POST)
            if form.is_valid():
                target_role = form.cleaned_data['target_role']
                for user in users:
                    user.role = target_role
                    user.save()

                self.message_user(
                    request,
                    f"Successfully upgraded {len(users)} user(s) to {target_role}.",
                    messages.SUCCESS,
                )
                return HttpResponseRedirect('/admin/')
        else:
            form = RoleUpgradeForm()

        return render(
            request,
            'admin/upgrade_user.html',
            context={'form': form, 'users': users},
        )


# Register the admin
admin.site.register(User, UserAdmin)
admin.site.register(Referral)
