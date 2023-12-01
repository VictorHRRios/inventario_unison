from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('display_profile/<int:user_id>/', user_views.display_profile, name="display_profile"),
    path('activate_user/<int:user_id>/', user_views.activate_user, name="activate_user"),
    path('deactivate_user/<int:user_id>/', user_views.deactivate_user, name="deactivate_user"),
    path('update_user/<int:user_id>/', user_views.update_user, name="update_user"),
    path('register/', user_views.register, name='register'),
    path('', user_views.manage_users, name='manage_users'),
]
