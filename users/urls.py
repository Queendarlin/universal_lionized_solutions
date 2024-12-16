from django.urls import path
from .views import register_page, home, login_page, logout_page, agent_dashboard, profile_update, admin_dashboard, promote_to_admin, promote_to_agent, demote_to_agent, demote_to_regular, delete_user

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('agent_dashboard/', agent_dashboard, name='agent_dashboard'),
    path('profile_update/', profile_update, name='profile_update'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('promote_to_agent/<uuid:user_id>/', promote_to_agent, name='promote_to_agent'),
    path('promote_to_admin/<uuid:user_id>/', promote_to_admin, name='promote_to_admin'),
    path('demote_to_regular/<uuid:user_id>/', demote_to_regular, name='demote_to_regular'),
    path('demote_to_agent/<uuid:user_id>/', demote_to_agent, name='demote_to_agent'),
    path('delete_user/<uuid:user_id>/', delete_user, name='delete_user'),    
]
