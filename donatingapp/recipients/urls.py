from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.add_request, name='add_request'),
    path('list/', views.recipient_list, name='recipient_list'),
    path('decision/<int:request_id>/', views.handle_decision, name='handle_decision'),
    path('dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('donations/reject/<int:pk>/', views.reject_request, name='reject_request'),
]
