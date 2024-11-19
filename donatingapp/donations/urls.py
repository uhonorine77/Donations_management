from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
    path('add/', views.add_donation, name='add_donation'),
    path('edit/<int:donation_id>/', views.edit_donation, name='edit_donation'),
    path('delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('analytics/', views.analytics_view, name='analytics'),
]
