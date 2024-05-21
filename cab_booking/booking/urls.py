from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/register/', views.customer_register, name='customer_register'),
    path('driver/register/', views.driver_register, name='driver_register'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('driver/login/', views.driver_login, name='driver_login'),
    path('customer/book_cab/', views.book_cab, name='book_cab'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('generate-ride-request/', views.generate_ride_request, name='generate_ride_request'),
    path('waiting-page/', views.waiting_page, name='waiting_page'),
    path('accept-ride-request/<int:ride_request_id>/', views.accept_ride_request, name='accept_ride_request'),
    path('reject-ride-request/<int:ride_request_id>/', views.reject_ride_request, name='reject_ride_request'),
    path('accepted-page/', views.accepted_page, name='accepted_page'),
    path('rejected-page/', views.rejected_page, name='rejected_page'),
    path('accepted/<int:ride_request_id>/', views.accepted, name='accepted'),
]