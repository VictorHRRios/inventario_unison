from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('delete_user/<int:user_id>/', user_views.delete_user, name="delete_user"),
    path('update_user/<int:user_id>/', user_views.update_user, name="update_user"),
    path('register/', user_views.register, name='register'),
    path('', user_views.manage_users, name='manage_users'),
]
