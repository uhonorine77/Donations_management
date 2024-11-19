from django.urls import path # type: ignore
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='auth'),
    # path('analytics/', views.analytics_view, name='analytics'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_list/', views.user_list, name='user_list'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]